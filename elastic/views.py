from django.views.generic.list import ListView 
from django.shortcuts import render
from .documents import *
from .serializers import *
from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from django.http import HttpResponse
from elasticsearch_dsl import Q
from .serializers import CandidateEducationSerializer
from .documents import CandidateEducationDocument

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_EXCLUDE,
    SUGGESTER_COMPLETION
)
import json
from resume.views import EmployerPermission
from django.conf import settings
# Create your views here.

class CandidateEducationDocumentView(DocumentViewSet):
    permission_classes=(EmployerPermission,)
    document = CandidateEducationDocument
    serializer_class = CandidateEducationSerializer
    # lookup_field = 'id'
    fielddata=True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
        SuggesterFilterBackend
        
    ]
   
    search_fields = (
        'college_name',
        'degree',
    )
    multi_match_search_fields = (
       'college_name',
        'degree',
    )
    filter_fields = {
        "id": {"field": "id", "lookups": [LOOKUP_QUERY_IN,LOOKUP_FILTER_RANGE]},
        'college_name' : 'college_name',
        'degree' : 'degree',
        # 'start_year':'start_year',
        # 'end_year':'end_year',
        'start_year':{
            'field': 'start_year',
            "lookups": [LOOKUP_QUERY_IN,LOOKUP_FILTER_RANGE]
        },
        'end_year':{
            'field': 'end_year',
            "lookups": [LOOKUP_QUERY_IN,LOOKUP_FILTER_RANGE]
        }
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ( 'id' ,)


class PrivateDataDocumentView(DocumentViewSet):
    permission_classes=(EmployerPermission,)
    document = PrivateDataDocument
    serializer_class = PrivateDataSerializer
    # lookup_field = 'id'
    fielddata=True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
        SuggesterFilterBackend
        
    ]
   
    search_fields = (
        'name',
    )
    multi_match_search_fields = (
       'name',
    )
    filter_fields = {
        "id": {"field": "id", "lookups": [LOOKUP_QUERY_IN,LOOKUP_FILTER_RANGE]},
        'name' : 'name',
        # 'phone_no':{
        #     'field': 'phone_no',
        #     "lookups": [LOOKUP_QUERY_IN,LOOKUP_FILTER_RANGE]
        # },
        'current_salary':{
            'field': 'current_salary',
            "lookups": [LOOKUP_QUERY_IN,LOOKUP_FILTER_RANGE]
        },
        'expected_salary':{
            'field': 'expected_salary',
            "lookups": [LOOKUP_QUERY_IN,LOOKUP_FILTER_RANGE]
        }
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ( 'id' ,)

class WorkDetailDocumentView(DocumentViewSet):
    permission_classes=(EmployerPermission,)
    document = OnlySearchWorkdetailDocument
    serializer_class = WorkDetailSerializer1
    # lookup_field = 'id'
    fielddata=True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
        SuggesterFilterBackend
        # SearchFilterBackend,
        # SuggesterFilterBackend,
    ]
   
    search_fields = (
        'skills.name',
        'sub_skills.name',
        'resp_title.name',
        'company_name',
    )
    multi_match_search_fields = (
       'skills.name',
       'sub_skills.name',
       'resp_title.name',
       'company_name'
    )
    filter_fields = {
        "id": {"field": "id", "lookups": [LOOKUP_QUERY_IN]},
        'skills':'skills.name.raw',
        # 'skills':{
        #     'field': 'skills.name.raw',
        #     'lookups': [
        #         LOOKUP_FILTER_TERMS,
        #         LOOKUP_FILTER_PREFIX,
        #         LOOKUP_FILTER_WILDCARD,
        #         LOOKUP_QUERY_IN,
        #         LOOKUP_QUERY_EXCLUDE,
        #     ],
        # },
        'sub_skills':'sub_skills.name.raw',
        'resp_title':'resp_title.name.raw',
        'company_name':'company_name'
    }

    suggester_fields = {
        "resp_title_suggest": {"field": "resp_title.name.suggest", "suggesters": [SUGGESTER_COMPLETION]}
    }

    ordering_fields = {
        'id': None,
    }
    ordering = ( 'id' ,)


class MiscDetailElasticSearch(APIView, LimitOffsetPagination):
    permission_classes=(EmployerPermission,)
    serializer_class = MiscDetailSerializer1
    document_class = MiscdetailDocument

    def get(self, request):
        search_term = request.GET.get('search_term', 'DEV')
        # print(search_term)
        q = Q(
            "multi_match", 
            query=search_term,
            fields=[
                'job_title.name.raw',
                # 'open_to.name',
                # "status.name",
                # "access",
                # "locations",
                # "current_city.name.raw"
                # In reality here I have more fields
            ], 
            fuzziness='auto',
            )
        search = self.document_class.search().query(q)
        response = search.execute()
        results = self.paginate_queryset(response, request, view=self)
        serializer = self.serializer_class(results, many=True)
        return self.get_paginated_response(serializer.data)
        # return Response(self.serializer_class(search.to_queryset(), many=True).data)

        # # search = search().query(q)
        # response = search.execute()
        # return HttpResponse(search)



class OnlySearchWorkdetails(APIView, LimitOffsetPagination):
    permission_classes=(EmployerPermission,)
    productinvetory_serializer = WorkDetailSerializer1
    search_document = OnlySearchWorkdetailDocument

    def post(self, request, query="dev"):
        # print(query)
        
        try:
            q=Q(
                'multi_match',
                query=query,
                fields=[
                    'sub_skills.name',
                    'company_name',
                    'resp_title.name.raw',
                    'my_tasks'
                    # 'sub_skills.name.raw',
                ]
                #,minimum_should_match=2,
                ,fuzziness='auto'
               ) | Q(
               #Q('match', skills__name__raw="DJANGO"),
            #    Q(
                'bool',
                    should=[
                        Q('match', skills__name__raw=""),
                        Q('match', job_title__raw=""),
                        Q('match', open_to__raw=""),
                        Q('match', current_city__raw=""),
                    ],
                    # filter= [
                    #     Q( "term" { "email"= "joe@bloggs.com" })
                    #  ]
                 )
            search = self.search_document.search().query(q)
            skills_filter=request.data.get('skills',None)
            if skills_filter:
                qq=Q('match', skills__name__raw=skills_filter)
                search=search.post_filter(qq)
            # print(search.to_dict())
            response = search.execute()
            # re=response.to_dict()
            # print(re)
            # for hit in response:
            #     print(hit)
            # q = Q("range", **{"price_range_from.SGD":{"gte": 0.0, "lte": 100.0}})
            # search=search.post_filter(q)

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.productinvetory_serializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            return HttpResponse(e, status=500)

    # def post(self,request,query):
    #     data = request.data.get('que'," ")
    #     # print(data)
    #     return HttpResponse(data, status=200)


from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from rest_framework.decorators import api_view
from rest_framework.response import Response
from elasticsearch_dsl.query import MultiMatch

@api_view(['POST'])
def search(request):
    
    # client = Elasticsearch([{'host': '34.131.132.43', 'port': 9200, 'url_prefix': 'en', 'use_ssl': False},])
    # client=Elasticsearch()
    client=Elasticsearch("http://34.131.132.42:9200")
    min_sal = request.data.get('min_sal', None)
    max_sal = request.data.get('max_sal', None)
    query = request.data.get('query', None)
    skills_filter=request.data.get('skills',None)
    
    flag=True
    if not min_sal and  not max_sal:
        flag=False
    if not min_sal:
        min_sal="1"
    if not max_sal:
        max_sal="999999999999"

    # print(min_sal)
    # print(max_sal)

    sal = Q("range", **{"expected_salary":{"gte": min_sal, "lte": max_sal}})
    ss = Search(using=client, index='private_data').query(sal)
    response = ss.execute()
    access_ids=[]
    for hit in response:
        access_ids.append(hit.access.id)
    # print(access_ids)
    # print(flag)
    # print(qqq_body)
    # access_ids=[]


    # s.post_filter('match', skills__name__raw='html') 

    res=Search(using=client, index='*') \
        .query('bool', must=[(Q('multi_match', 
                       type = "cross_fields", 
                       query = query, 
                       fields = ['sub_skills.name.raw', 'company_name',
                                 'resp_title.name.raw', 'my_tasks','degree.name',
                                 'open_to.name.raw','job_title.name.raw','access.id']))]) 
    
    if isinstance(access_ids, list) and flag:
        # print("in")
        qq=Q('terms', access__id=access_ids)
        res = res.post_filter(qq)

    if skills_filter:
                # print("innn")
                qq=Q('terms', skills__name__raw=skills_filter) | Q('terms', sub_skills__name__raw=skills_filter) 
                res=res.post_filter(qq)
    resp1=res.execute()
    # print(resp1.to_dict())
    a=json.dumps(resp1.to_dict())
    # print(resp1.hits.total.value)
    return HttpResponse(a, content_type="application/json")




    # qqq_body={  
    #         #   "size":2, 
    #             # "from":0,
    #             "query": {
    #                 "bool" : {
    #                     "must" : [
    #                         {
    #                             "multi_match": {
    #                                 "query": query,
    #                                 "fields": ['sub_skills.name.raw', 'company_name', 
    #                                            'resp_title.name.raw', 'my_tasks','degree.name',
    #                                            'open_to.name.raw','job_title.name.raw','access.id'],
    #                             }
    #                         }, 
    #                         {
    #                             "bool": {
    #                                 "must": [
    #                                     {
    #                                         "terms": {
    #                                             "access.id": access_ids
                                                
    #                                         }

    #                                     },
                                       
                                        
    #                                 ]
    #                             }
    #                         },
                        
    #                         # {'bool': {'filter': [{'terms': {'skills.name.raw':skills_filter}}]}}
                    
    #                     ]
    #                 },
                    
    #             },
    #             "post_filter": { 
    #                 "terms": { "skills.name.raw":skills_filter }
    #             }
    #         }

    
    # # print(resp1.hits.hits)
    # # for hit in resp1:
    # #         print(hit.hits)
    # # return HttpResponse(json.dumps(resp1.hits.hits), content_type="application/json")

    
    
    # s=client.search(index="*", body=qqq_body) 
    
    
    
    
    # return Response(s)

    # print(s.to_dict())
    
    # print(response.hits.total.value)
    # r={}
    # re=response.to_dict()
    # print(re)
    # access_ids=[]
    # for hit in response:
    #    access_ids.append(hit.access.id)
    #    print(hit.access.id)
    # print(access_ids)
    # print(response.to_dict().get("hits", {}))

# qq=Q("terms",{"skills__name__raw" : skills_filter )
    # ss1 = Search(using=client, index='work_detail')
    # ss1 = ss1.filter("terms", skills__name__raw=["django","php","python"])
    # print(ss1.to_dict())
    # response1 = ss1.execute()

# query1 = MultiMatch(query="kkk", fields=['name','skills','sub_skills'], fuzziness='AUTO')
    # query="frontend at google"
    # qq=Q(
    #             'multi_match',
    #             query=query,
    #             fields=[
    #                 'sub_skills.name.raw',
    #                 'company_name',
    #                 'resp_title.name.raw',
    #                 'my_tasks'
    #                 # 'sub_skills.name.raw',
    #             ]
    #             #,minimum_should_match=2,
    #             # ,fuzziness='2'
    #            )
    # s = search_document.search().query(q)
    # print(s.to_dict())
    # q={'multi_match': {'query': 'frontend at google', 
    #                              'fields': ['sub_skills.name.raw', 'company_name', 
    #                              'resp_title.name.raw', 'my_tasks','current_salary','expected_salary'],
    #                              "range":{
    #                                     "current_salary":{
    #                                         "gte":10
    #                                     }
    #                                     # "expected_salary":{
    #                                     #     "lte":51
    #                                     # }
    #                              }
    #
    #                               }}
    
    
    # q_body={
    #     "query": {
    #       "bool": {
    #         # "filter": [
    #         #   {
    #         #     "multi_match": {
    #         #       "query": "frontend at google",
    #         #       "fields": ['sub_skills.name.raw', 'company_name', 
    #         #                      'resp_title.name.raw', 'my_tasks'],
    #         #     }
    #         #   },],
    #           "must":[
    #           {
    #             "range": {
    #               "expected_salary": { 
    #                 "gte":1,
    #                 "lte": 501
    #                 }
    #             }
    #           }
    #         ]
            
    #       }
    #     },
        
    #   }

#     qq_body={
#     "query": {
#         "bool" : {
#             "should" : [
#                 {
#                     "multi_match": {
#                         "query": query,
#                         "fields": ['sub_skills.name.raw', 'company_name', 
#                                   'resp_title.name.raw', 'my_tasks','degree.name','open_to.name.raw','job_title.name.raw',],
#                     }
#                 }, 
#                 {
#                     "bool": {
#                         "must": [
#                             {
#                                 "bool": {
#                                     "must": [
#                                         {
#                                              "range": {
#                                                 "expected_salary": { 
#                                                     "gte":1,
#                                                     "lte": 501
#                                                     }
#                                                 }
#                                         },
#                                         {
#                                             "term": {
#                                                 "_index": {
#                                                 "value": "private_data"
#                                                 }
#                                             }
#                                         }
#                                         # {
#                                         #     "range": {
#                                         #         "publish_until": {
#                                         #             "gt" : "now"
#                                         #         }
#                                         #     }
#                                         # }
#                                     ]
#                                 }
#                             },
#                             # {
#                             #     "bool": {
#                             #         "must": [
#                             #             {
#                             #                 "terms": {
#                             #                     "access.id": access_ids
                                                
#                             #                 }

#                             #             }
#                             #             # {
#                             #             #     "exists": {
#                             #             #         "field": "expected_salary"
#                             #             #     }
#                             #             # },
#                             #             # {
#                             #             #     "exists": {
#                             #             #         "field": "publish_until"
#                             #             #     }
#                             #             # }
#                             #         ]
#                             #     }
#                             # }
#                         ]
#                     }
#                 }
#             ]
#         }
#     }
# }
    
 # {
                                        #     "terms": {
                                        #         "skills.name.raw": ["Django","python"]
                                        #         # "boost":0.5
                                        #     }
                                        # },
                                        # {
                                        # "bool": {
                                        #     "filter": [
                                        #         {
                                        #           "terms": {
                                        #                 "skills.name.raw": ["Django","php"],
                                        #                 "boost": 1.0
                                        #             }
                                        #         },

                                        #     ]
                                        #   }
                                        # },



                                        # {
                                        #     "terms": {
                                        #         "skills.name.raw": ["Django","php"]
                                        #     }
                                        # },
                                        # {
                                        #  "bool": {
                                        #     "must": [
                                        #                 {
                                        #                     "match": {
                                        #                     "current_city.name.raw": "DELHI"
                                        #                     }
                                        #                 },
                                        #                 {
                                        #                     "term": {
                                        #                         "_index": {
                                        #                         "value": "misc_detail"
                                        #                         }
                                        #                     }
                                        #                 }
                                        #     ]
                                        #  }
                                        # }

# res=Search() \
#         .query('bool', must=[(Q('multi_match', 
#                        type = "cross_fields", 
#                        query = "frontend", 
#                        fields = ['sub_skills.name.raw', 'company_name', 
#                                                'resp_title.name.raw', 'my_tasks','degree.name',
#                                                'open_to.name.raw','job_title.name.raw','access.id'])) & (Q("terms", access__id=access_ids))]) \
        # .query('multi_match', 
        #                type = "cross_fields", 
        #                query = "frontend", 
        #                fields = ['sub_skills.name.raw', 'company_name', 
        #                                        'resp_title.name.raw', 'my_tasks','degree.name',
        #                                        'open_to.name.raw','job_title.name.raw','access.id']) \
        # .filter("terms", country="United Kingdom") \
        
        # .query('bool', filter=[(Q("match", industry='Automobile')) | (~Q("exists", field='industry'))]) 