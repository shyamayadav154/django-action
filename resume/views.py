from django.http import Http404, JsonResponse
from rest_framework import generics,filters
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .throttle import  BaseEmployerThrottle2
from rest_framework import mixins, viewsets,status
from django_filters.rest_framework import DjangoFilterBackend
from drf_multiple_model.views import ObjectMultipleModelAPIView
from django.views.generic import UpdateView
from rest_condition import And, Or, Not
from django.core.cache.backends import locmem
from itertools import islice
from collections import OrderedDict
from api_tracking.models import Tracking
from datetime import date, timedelta
import datetime
from .serializers import (
    MiscUnAuthorisedSerializer,
    Open_toSeraializer,
    PrivateUnAuthorisedSerializer,
    ResumeSerializer, 
    ResumeCreateSerializer,
    SearchResumeSerializer, 
    WorkDetailSerializer,
    WorkDetailAnySerializer, 
    PrivateSerializer,
    EducationSerializer,
    WorkCreateSerializer,
    MiscSerializer,
    Job_sugesstions_serializer,
    CertificationsSerializer
    )

from .models import (
    CandidateResume,
    Current_city,
    Degree,
    Job_Task_Suggesstion,
    Job_Title,
    Open_to,
    Resp_Title,
    SearchResume,
    Skills,
    Status,
    Sub_Skills, 
    WorkDetail,
    CandidatePrivateData,
    CandidateEducation,
    MiscDetail,
    Certifications
    )

from drf_multiple_model.views import ObjectMultipleModelAPIView
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from accounts.models import CustomUser, Employer
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from stripe_payments.models import SubscriptionDetails
from itertools import groupby
from operator import itemgetter
from rest_framework.response import Response
import json
from django.db.models.query import QuerySet
from django.db.models import Count
# from rest_framework import serializers
import pandas as pd
# from django.core import serializers
from urlShortner.models import urlShortener
from django.conf import settings


def checkSubs(user):
    try:
        queryset=SubscriptionDetails.objects.filter(user=user,status="active").latest('created_at')
    except:
        queryset=None

    if queryset:
        if queryset.plan_type=="STANDARD":
            return 7
        elif queryset.plan_type=="PREMIUM":
            return 10
        else:
            return 5
        
    return 5

class UserWritePermission():
    message = 'Permission Denied'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # print("hello")
            return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # print(request.user)
        return obj.access.user == request.user

class CandidatePermission():
    message = "Only candidate are allowed.."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
           return request.user and request.user.type == "CANDIDATE"

    def has_object_permission(self, request, view, obj):
        return obj.access.user == request.user

class EmployerPermission():
    # message = "You cannot view this candidate.."
    message = "Only employers are allowed.."
    def has_permission(self, request, view):
        # print(request.user.type)
        if request.user.is_authenticated:
           return request.user and request.user.type == "EMPLOYER"

    def has_object_permission(self, request, view, obj):
        return obj.access.user == request.user

class DualPermission():
    message = "You cannot view this candidate.."

    def has_permission(self, request, view):
        # print(request.user.type)
        if request.user.is_authenticated:
            return request.user and request.user.type == "EMPLOYER" or "CANDIDATE"

    def has_object_permission(self, request, view, obj):
        return obj.access.user == request.user
        # return obj.user == request.user
      

class ResumeCreateView(generics.CreateAPIView):
    permission_classes = [CandidatePermission]  # add authentications
    queryset = CandidateResume.objects.all()
    serializer_class = ResumeCreateSerializer

class ResumeView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [ResumeWritePermission]
    queryset = CandidateResume.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = 'user_id'
    # throttle_classes = [BaseEmployerThrottle]
    # throttle_emp_classes =[]

    # def get_throttles(self):
    #     if self.request.user.is_authenticated:
    #         if  self.request.user.type=='EMPLOYER':
    #             return super().get_throttles()
    #         else:
    #             return self.throttle_emp_classes
    #     return self.throttle_emp_classes   
    def get(self, request, user_id, format=None):
        if self.request.user.is_authenticated:
            if self.request.user.id==user_id:
                try:
                    queryset=CandidateResume.objects.get(user__id=user_id)
                except:
                    queryset=None
                if queryset:
                    serializer = ResumeSerializer(queryset, many=False)
                    return Response(serializer.data)
                else:
                    raise Http404
            else:
                return JsonResponse(status=status.HTTP_401_UNAUTHORIZED,data="Permission Denied",safe=False)
        else:
            raise Http404

class ResumeDeleteView(generics.DestroyAPIView):
    # permission_class = [ResumeWritePermission]
    queryset = CandidateResume.objects.all()
    serializer_class = ResumeCreateSerializer
    lookup_field = 'user_id'

    def delete(self, request, user_id, format=None):
        """Remove a unit instance."""
        if self.request.user.is_authenticated:
            
            if self.request.user.id==user_id:
                try:              
                    obj = CandidateResume.objects.get(user__id=user_id)
                except:
                    obj=None
                if obj:
                    obj.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    raise Http404 
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED,data="Permission Denied",safe=False)
        else:
            raise Http404
            
class ResumeEdit(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [ResumeWritePermission]
    queryset = CandidateResume.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = 'user_id'

    def patch(self, request, user_id):
    
        if self.request.user.is_authenticated:
            # print("next")
            # print(user_id)
            # print(self.request.user.id)
            if self.request.user.id==user_id:
                try:
                   queryset=CandidateResume.objects.get(user__id=user_id)
                except:
                    queryset=None
                if queryset:
                   serializer = ResumeSerializer(queryset, data=request.data, partial=True) # set partial=True to update a data partially
                   if serializer.is_valid():
                        serializer.save()
                        return Response(data=serializer.data) 
                   else:
                       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                else:
                   raise Http404                
            else:
                return JsonResponse(status=status.HTTP_401_UNAUTHORIZED,data="Permission Denied",safe=False)
        else:
            raise Http404
    def put(self, request, user_id):

        if self.request.user.is_authenticated:
            if self.request.user.id==user_id:
                try:
                   queryset=CandidateResume.objects.get(user__id=user_id)
                except:
                    queryset=None
                if queryset:
                   serializer = ResumeSerializer(queryset, data=request.data,partial=False)
                   if serializer.is_valid():
                        serializer.save()
                        return Response(data=serializer.data) 
                   else:
                       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                else:
                    raise Http404 # RETURNS NOT FOUND ==> BEST TO USE
            else:
                return JsonResponse(status=status.HTTP_401_UNAUTHORIZED,data="Permission Denied",safe=False)
        else:
            raise Http404
class PvtDataCreateView(generics.CreateAPIView):
    permission_classes = [UserWritePermission]
    model = CandidatePrivateData
    serializer_class = PrivateSerializer
    queryset = CandidatePrivateData.objects.all()
    lookup_field = "access"

class PvtDataUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [UserWritePermission]
    model = CandidatePrivateData
    serializer_class = PrivateSerializer
    queryset = CandidatePrivateData.objects.all()
    lookup_field = "access"


class PvtDataView(generics.RetrieveAPIView):
    
    permission_classes = [Or(EmployerPermission, IsAuthenticatedOrReadOnly)]
    model = CandidatePrivateData
    serializer_class = PrivateSerializer
    serializer_anonymous_class=PrivateUnAuthorisedSerializer
    queryset = CandidatePrivateData.objects.all()
    lookup_field = "access"
    throttle_classes = [BaseEmployerThrottle2]
    throttle_emp_classes =[]
    # filter_backends = [DjangoFilterBackend]
    # name="SEARCH"
    # search_fields = ['^misc_detail__open_to']
    # filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    # filter_fields=('misc_detail__open_to',)

    def get_throttles(self):
        if self.request.user.is_authenticated:
            if  self.request.user.type=='EMPLOYER':
                access=str(self.request.resolver_match.kwargs.get('access'))
                user=self.request.user.pk
                userr=self.request.user  # print(user)
                emp=Employer.objects.get(id=user)
                username=emp.first_name +" "+  emp.last_name  # print(emp.details.company_name)
                datee = date.today() # print(datee)
                shortcode=urlShortener.objects.filter(access_id=access) # Fetching custom shortcode for that user
               
                if shortcode:
                    shortcode_url= settings.FRONTEND_BASE_URL+"urlShort/"+shortcode.shorturl   # full url using shortcode
                else:
                    shortcode_url="" 

                query=Tracking.objects.filter(user_id=user,date__contains=datee)# print(query.count())# print(checkSubs(userr))
                if query.count() < checkSubs(userr):#5:
                    # print("1")
                    # print(super().get_throttles())
                    if query.count()==0:
                        queryset=Tracking.objects.create(user_id=user,email=emp.email,access_id=access,shortcode_url=shortcode_url,view="private",counter=1,date=datee,username=username,company_name=emp.details.company_name,job_title=emp.details.job_title)
                        queryset.save()
                    else:
                        try:
                            query1=Tracking.objects.get(user_id=user,access_id=access,date__contains=datee)                   
                        except:
                            query1=False
                        if query1:
                            # print("2")
                            query1.counter=query1.counter+1
                            query1.updated_time=datetime.datetime.now().strftime('%H:%M:%S')
                            query1.save()
                            return self.throttle_emp_classes
                        else:
                            # print("3")
                            queryset=Tracking.objects.create(user_id=user,email=emp.email,access_id=access,shortcode_url=shortcode_url,view="private",counter=1,date=datee,username=username,company_name=emp.details.company_name,job_title=emp.details.job_title)
                            queryset.save()
                            return self.throttle_emp_classes
                try:
                    
                    query1=Tracking.objects.get(user_id=user,access_id=access,date__contains=datee)                   
                except:
                    
                    query1=False
                if query1:
                        
                        query1.counter=query1.counter+1
                        query1.updated_time=datetime.datetime.now().strftime('%H:%M:%S')
                        query1.save()
                        return self.throttle_emp_classes
                else:
                    # i think needed create.tracking
                    # queryset=Tracking.objects.create(user_id=user,access_id=access,view="private",counter=1,date=datee)
                    # queryset.save()
                    # print("99999")
                    # print(super().get_throttles())
                    return super().get_throttles()

            else: # if user is not employer i.e it  is a candidate 
                return self.throttle_emp_classes
        
        # query=Tracking.objects.filter(user_id=user,date__contains=datee)
        # queryset=Tracking.objects.create(user_id=user,email=emp.email,access_id=access,view="private",counter=1,date=datee,username=username,company_name=emp.details.company_name,job_title=emp.details.job_title)
        return self.throttle_emp_classes  # if user is not authenticated i.e it is a anonymous user

    def get_serializer_class(self):
            # print("yes")
            # print(self.request.user.type)
            if not self.request.user.is_authenticated or self.request.user.type=="CANDIDATE":
                return self.serializer_anonymous_class
            elif self.request.user.type=="EMPLOYER":
                return super().get_serializer_class()
            return super().get_serializer_class()

    def get(self, request, access, format=None):

        queryset = CandidatePrivateData.objects.filter(access__exact=access)
        # print(request.user.id)
        if request.user.is_authenticated:
            # print("1")
            if request.user.type=='CANDIDATE':
                queryset2 = CandidatePrivateData.objects.filter(access__exact=access,access__user=request.user)
                # print(queryset2)
                if queryset2:
                    # print("2")
                    serializer = PrivateSerializer(queryset2, many=True)
                    return Response(serializer.data)
                else:
                    # print("3")
                    serializer = PrivateUnAuthorisedSerializer(queryset, many=True)
                    return Response(serializer.data)
            else:
                # print("4")
                serializer = PrivateSerializer(queryset, many=True)
                return Response(serializer.data)
        else:
            # print("5")
            serializer = PrivateUnAuthorisedSerializer(queryset, many=True)
            return Response(serializer.data)

class CreateEducationView(generics.CreateAPIView):
    permission_classes = [UserWritePermission]  # add authentications
    model = CandidateEducation
    serializer_class = EducationSerializer
    queryset = CandidateEducation.objects.all()
    lookup_field = "access"

class UpdateEducationView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [UserWritePermission]
    model = CandidateEducation
    serializer_class = EducationSerializer
    queryset = CandidateEducation.objects.all()
    lookup_field = "pk"
    
class EducationView(generics.RetrieveAPIView):
    permission_classes = [Or(UserWritePermission,IsAuthenticatedOrReadOnly)]
    serializer_class=EducationSerializer
    # model = CandidateEducation
    lookup_field="access"
    queryset = CandidateEducation.objects.all()

    def get(self, request, access, format=None):
        queryset = CandidateEducation.objects.filter(access__exact=access)
        # print(request.user.id)
        # print(access)
        serializer = EducationSerializer(queryset, many=True)
        return Response(serializer.data)


class WorkDetailView(APIView):

    def get(self, request, access, format=None):

        queryset = WorkDetail.objects.filter(access__exact=access)
        # print(request.user.id)
        if request.user.is_authenticated:
            # print("1")
            if request.user.type=='CANDIDATE':
                queryset2 = WorkDetail.objects.filter(access__exact=access,access__user=request.user)
                # print(queryset2)
                if queryset2:
                    # print("2")
                    serializer = WorkDetailSerializer(queryset2, many=True)
                    return Response(serializer.data)
                else:
                    # print("3")
                    serializer = WorkDetailAnySerializer(queryset, many=True)
                    return Response(serializer.data)
            else:
                # print("4")
                serializer = WorkDetailSerializer(queryset, many=True)
                return Response(serializer.data)
        else:
            # print("5")
            serializer = WorkDetailAnySerializer(queryset, many=True)
            return Response(serializer.data)

class MiscCreateView(generics.CreateAPIView):
    # authentication_classes = (JWTAuthentication,)
    # permission_classes = [UserWritePermission]
    model = MiscDetail
    serializer_class = MiscSerializer
    queryset = MiscDetail.objects.all()
    lookup_field = "access"

class MiscDetailView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # authentication_classes = (JWTAuthentication,)
    # permission_classes = [UserWritePermission]
    model = MiscDetail
    serializer_class = MiscSerializer
    queryset = MiscDetail.objects.all()
    lookup_field = "access"
    # throttle_classes = [BaseEmployerThrottle]
    # throttle_emp_classes =[]
    def get(self, request, access, format=None):

            queryset = MiscDetail.objects.filter(access__exact=access)
            # print(request.user.id)
            if request.user.is_authenticated:
                # print("1")
                if request.user.type=='CANDIDATE':
                    queryset2 = MiscDetail.objects.filter(access__exact=access,access__user=request.user)
                    # print(queryset2)
                    if queryset2:
                        # print("2")
                        serializer = MiscSerializer(queryset2, many=True)
                        return Response(serializer.data)
                    else:
                        # print("3")
                        serializer = MiscUnAuthorisedSerializer(queryset, many=True)
                        return Response(serializer.data)
                else:
                    # print("4")
                    serializer = MiscSerializer(queryset, many=True)
                    return Response(serializer.data)
            else:
                # print("5")
                serializer = MiscUnAuthorisedSerializer(queryset, many=True)
                return Response(serializer.data)

class MiscRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [UserWritePermission]
    model = MiscDetail
    serializer_class = MiscSerializer
    queryset = MiscDetail.objects.all()
    lookup_field = "access"
   
# USER BASED API RESPONSE WILL ONLY RETURN DATA FOR THE CURRENT SIGNED IN USER
    # def get_queryset(self):
    #     user = self.request.user
    #     return WorkDetail.objects.filter(user=user)

# PERMISSION BASED SERIALIZER SWITCH
    # serializer_class = WorkDetailSerializer
    # def get_queryset(self):
    #     queryset = WorkDetail.objects.all()
    #     access = self.request.query_params.get('access')
    #     if access is not None:
    #         queryset = queryset.filter(access=access)
    #     return queryset
    

    # def get_serializer_class(self):
    #     if self.request.user.type == "CANDIDATE":
    #         return WorkDetailSerializer
    #     return WorkDetailAnySerializer

class WorkDetailViewset(viewsets.ModelViewSet):
    queryset = WorkDetail.objects.all()
    serializer = WorkDetailSerializer(queryset, many=True)

    def get_queryset(self,access): #  access == added by me- anirban
        user = self.request.user
        return WorkDetail.objects.filter(access__exact=access)

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.base_type == "CANDIDATE" or "EMPLOYER":
                return WorkDetailSerializer
        else:
            return WorkDetailAnySerializer
            
class WorkDetailUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [UserWritePermission]
    model = WorkDetail
    serializer_class = WorkCreateSerializer
    queryset = WorkDetail.objects.all()
    
class WorkCreateView(generics.CreateAPIView):
    permission_classes = [UserWritePermission]
    model = WorkDetail
    serializer_class = WorkCreateSerializer
    queryset = WorkDetail.objects.all()

class SearchResumeListView(generics.RetrieveAPIView):
    # queryset = SearchResume.objects.all()
    # serializer_class = SearchResumeSerializer(queryset,many=True)
    model = SearchResume
    serializer_class = SearchResumeSerializer
    queryset = SearchResume.objects.all()
    lookup_field = "access"
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # name="SEARCH"
    # search_fields = ['^misc_detail__open_to']
    # filter_backends = (filters.SearchFilter,django_filters.rest_framework.DjangoFilterBackend)
    # filter_fields=('misc_detail__open_to',)

class JlistView(ObjectMultipleModelAPIView):

    # def get_querylist(self, *args, **kwargs):
        # access = self.kwargs.get('access')        
    querylist = [
            # {'queryset': CandidateResume.objects.all(),
            #  'serializer_class': ResumeSerializer },
            # {'queryset': MiscDetail.objects.all(),
            #  'serializer_class': MiscSerializer },
            {'queryset': CandidateEducation.objects.all(),
             'serializer_class': EducationSerializer },
            # {'queryset': WorkDetail.objects.all(),
            #  'serializer_class': WorkDetailSerializer },
            # {'queryset': CandidatePrivateData.objects.all(),
            #  'serializer_class': PrivateSerializer },
        ]
        # return queryset
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^degree__name',)

@api_view(['GET'])
def Open_to_list(request):
    name = list(Open_to.objects.values_list('name', flat=True))
    return Response({"name":name})

@api_view(['GET'])
def Status_list(request):
    name = list(Status.objects.values_list('name', flat=True))
    return Response({"name":name})

@api_view(['GET'])
def Current_city_list(request):
    name = list(Current_city.objects.values_list('name', flat=True))
    return Response({"name":name})

@api_view(['GET'])
def Skills_list(request):
    name = list(Skills.objects.values_list('name', flat=True))
    return Response({"name":name})

@api_view(['GET'])
def Sub_skills_list(request):
    name = list(Sub_Skills.objects.values_list('name', flat=True))
    return Response({"name":name})

@api_view(['GET'])
def Job_Title_list(request):
    name = list(Job_Title.objects.values_list('name', flat=True))
    return Response({"name":name})

@api_view(['GET'])
def Degree_list(request):
    name = list(Degree.objects.values_list('name', flat=True))
    return Response({"name":name})

@api_view(['GET'])
def Resp_title_list(request):
    name = list(Resp_Title.objects.values_list('name', flat=True))
    return Response({"name":name})


@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def Get_Suggesstions_for_jobtasks(request):

    if request.method=="POST":
        job_title=request.data.get('job_title',None)
        task=request.data.get('task',None)

        if job_title:
            try:
                query=Job_Task_Suggesstion.objects.filter(job_title__icontains=job_title)
            except:
                query=None
            if query:
                serializer = Job_sugesstions_serializer(query,many=True)
                return Response(serializer.data)
            
        if task:
            try:
                query=Job_Task_Suggesstion.objects.filter(suggessted_tasks__icontains=task)
            except:
                query=None
            if query:
                serializer = Job_sugesstions_serializer(query,many=True)
                return Response(serializer.data)
        return Response({"details":"Not found"},status=status.HTTP_404_NOT_FOUND)

    if request.method=="GET":
        try:
                query=Job_Task_Suggesstion.objects.all()
        except:
                query=None
        if query:
            items = Job_Task_Suggesstion.objects.values('job_title','suggessted_tasks').order_by('job_title')
            rows = groupby(items, itemgetter('job_title'))
            # print({c_title:[i['suggessted_tasks'] for i in items ]  for c_title, items in rows })
            return Response({c_title:[i['suggessted_tasks'] for i in items ]  for c_title, items in rows })
            # return Response({c_title: list(items) for c_title, items in rows})

        return Response({"details":"not found"})
        # tasks=[{"a":"abc"},{"b":"abc"}]
            # print(tasks[0])
            # for c_title, items in rows:
            #     print(c_title)
            #     a=list(items)
            #     for i in a:
            #         print(i['suggessted_tasks'])
                # print(a[1])
                # print("A %s is a %s." % (list(items['suggessted_tasks']), c_title))


class CerticationsCreateView(generics.CreateAPIView):
    
    # permission_classes = [UserWritePermission]
    # permission_classes = [AllowAny]
    model = Certifications
    serializer_class =CertificationsSerializer
    queryset = Certifications.objects.all()
    lookup_field = "access"


class CerticationsEditView(generics.RetrieveUpdateDestroyAPIView):
    
    model = Certifications
    serializer_class =CertificationsSerializer
    queryset = Certifications.objects.all()
    lookup_field = "pk"
    
class CerticationsView(generics.RetrieveAPIView):
   
    model = Certifications
    serializer_class =CertificationsSerializer
    queryset = Certifications.objects.all()
    lookup_field = "access"

    def get(self, request, access, format=None):
        queryset = Certifications.objects.filter(access__exact=access)
        serializer = CertificationsSerializer(queryset, many=True)
        return Response(serializer.data)


