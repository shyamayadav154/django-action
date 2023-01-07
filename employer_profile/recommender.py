from nltk.corpus import stopwords
import re
import string
import nltk
import os
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Employer_Template
from resume.models import WorkDetail,MiscDetail,CandidatePrivateData


nltk.data.path.append('Recomm/tmp/nltk')
if not (os.path.exists("Recomm/tmp/nltk")):
#   nltk.download('all', download_dir='/tmp/nltk')
    nltk.download('punkt', download_dir='Recomm/tmp/nltk')
    nltk.download('stopwords', download_dir='Recomm/tmp/nltk')
    nltk.download('wordnet', download_dir='Recomm/tmp/nltk')
    nltk.download('averaged_perceptron_tagger', download_dir='Recomm/tmp/nltk')
    nltk.download('omw-1.4', download_dir='Recomm/tmp/nltk')

from sklearn.feature_extraction.text import TfidfVectorizer
# from resume.views import export


stop = stopwords.words('english')
stop_words_ = set(stopwords.words('english'))
wn = WordNetLemmatizer()

def black_txt(token):
    return  token not in stop_words_ and token not in list(string.punctuation)  and len(token)>2   
  
def clean_txt(text):
  clean_text = []
  clean_text2 = []
  text = re.sub("'", "",text)
  text=re.sub("(\\d|\\W)+"," ",text) 
  text = text.replace("nbsp", "")
  text = text.replace("None", "") 
  clean_text = [ wn.lemmatize(word, pos="v") for word in word_tokenize(text.lower()) if black_txt(word)]
  clean_text2 = [word for word in clean_text if black_txt(word)]
  return " ".join(clean_text2)

def get_recommendation(top, df_cand2, scores):

        recommendation = pd.DataFrame(columns = ['access','score'])
        count = 0
        for i in top:
            recommendation.at[count, 'access'] = df_cand2['access'][i]
            # recommendation.at[count, 'job_title'] = df_cand2['job_title'][i]
            recommendation.at[count, 'score'] =  scores[count]
            count += 1

        return recommendation


# This [ArrayAgg] For getting manytomany values as a list ex:- skills, sub_skills   ==> only for postgres db 
from django.contrib.postgres.aggregates.general import ArrayAgg
def export():
    try:
        queryset1=MiscDetail.objects.all().values('access','job_title','locations')
        queryset2=WorkDetail.objects.annotate(skill=ArrayAgg('skills__name'),sub_skill=ArrayAgg('sub_skills__name')).values('access','resp_title__name','my_tasks','skill','sub_skill')

        # misc=pd.read_json("input.json").to_excel("output.xlsx")
        df1 = pd.DataFrame(list(queryset1))
        df1.to_csv('Recomm/miscdetail.csv', index = False, encoding='utf-8') # False: not include index

        df2 = pd.DataFrame(list(queryset2))
        df2.to_csv('Recomm/workdetail.csv', index = False, encoding='utf-8') # False: not include index

        m1 = pd.read_csv("Recomm/miscdetail.csv")
        w1 = pd.read_csv("Recomm/workdetail.csv")

        # merging the files
        f3 = m1[["access",'job_title','locations'
                ]].merge(w1[['access','resp_title__name','my_tasks',
                            'skill','sub_skill']], 
                                            on = "access", 
                                            how = "left")

        # creating a new file
        f3.to_csv("Recomm/misc+exp.csv", index = False)

        private=CandidatePrivateData.objects.all().values("access","current_salary","total_experience")
        df_priv = pd.DataFrame(list(private))
        # print(type(df_priv))
        df_priv['current_salary'] = df_priv['current_salary'].fillna(0).astype('int')
        df_priv.to_csv('Recomm/private.csv', index = False, encoding='utf-8')

        p1 = pd.read_csv("Recomm/misc+exp.csv")
        # print(type(p1['access']))
        pr = pd.read_csv("Recomm/private.csv")
        # print(type(pr['access']))

        results_final=p1[["access",'job_title','locations','resp_title__name','my_tasks',
                'skill','sub_skill']].merge(
            pr[["access","current_salary","total_experience"]],
                on = "access", 
                how = "inner"
        )  
        # print(results_final)
        results_final.to_csv("Recomm/Test-data.csv", index = False)
        return True
    except:
        return True
    


@api_view(['GET'])
@permission_classes([AllowAny])
def recommender(request,t_id):

    status=export()
    if status:

        # FOR GETTING EMPLOYER TEMPLATE DATA

        template=Employer_Template.objects.filter(id=t_id).values('user__id','job_title','job_description','skills','subskills','location','salary_offered')
        df_template = pd.DataFrame(list(template))

        # CLEANING THE MISSING VALUES
        df_template2 = df_template[['user__id','job_title','job_description','skills','subskills','location']]
        df_template2 = df_template2.fillna(" ")

        df_template2["text"] = df_template2["job_title"] + " " + df_template2["job_description"] +" "+ df_template2["skills"]+ " "+df_template2['subskills']+" "+df_template2['location']
        df_template2['text'] = df_template2['text'].apply(clean_txt)
        # print(df_template2.head())
        
        # salary_query=Employer_Template.objects.filter(id=t_id).values("id","salary_offered")
        if template:
            for i in template:
                salary=i['salary_offered']
        else:
            salary=None
        int_salary=int(salary)
            
        # FOR ALL CANDIATES DATA
        df_cand = pd.read_csv("Recomm/Test-data.csv")

        # CLEANING THE MISSING VALUES
        df_cand2 = df_cand[['access','job_title','locations','resp_title__name','my_tasks','skill','sub_skill','current_salary']]
        df_cand2 = df_cand2.fillna(" ")
        
        # print(df_cand2['current_salary'].dtypes)
        # print(df_cand2.head(10))
        if not int_salary <=0:
            df_cand2=df_cand2[df_cand2['current_salary'] < int_salary]
            df_cand2 = df_cand2.sort_index(ignore_index=True)
        # print(df_cand2.head(10))
        df_cand2["text"] = df_cand2["job_title"].map(str) + " " + df_cand2["my_tasks"] +" "+ df_cand2["skill"]+ " "+df_cand2['sub_skill']+" "+df_cand2['locations']
    
        df_cand2['text'] = df_cand2['text'].apply(clean_txt)
        # df_cand2.to_csv("Recomm/cleaned-data.csv", index = False)
        
        try:
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_jobid = tfidf_vectorizer.fit_transform((df_cand2['text'])) #fitting and transforming the vector
            # print(tfidf_jobid)
        except:
            pass
        
        user_q = df_template2.iloc[[0]]

        from sklearn.metrics.pairwise import cosine_similarity
        user_tfidf = tfidf_vectorizer.transform(user_q['text'])
        cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf, x),tfidf_jobid)
        output2=list(cos_similarity_tfidf)


        top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:10]

        list_scores = [output2[i][0][0] for i in top]

        recom=get_recommendation(top,df_cand2, list_scores)
        # out = recom.to_json(orient='records', lines=True)
        out2=recom.to_dict(orient='records')

        return Response({"status":out2,"res":recom})

    else:
        return Response({"status":"error"})



