from django.shortcuts import render
from . import serializers
from .models import Tracking
from rest_framework import generics, permissions,status
from rest_framework.response import Response
import datetime
from rest_condition import And, Or, Not
from resume.models import CandidateResume
from accounts.models import CustomUser
from resume.views import CandidatePermission
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from django.db.models import Subquery, OuterRef
class CandidatePermission(permissions.BasePermission):
    message = "Only candidate are allowed.."

    def has_permission(self, request, view):
        # print(request.user.type)
        if request.user.is_authenticated:
            # print(request.user and request.user.type == "CANDIDATE")
            return request.user and request.user.type == "CANDIDATE"
        return False

    def has_object_permission(self, request, view, obj):
        return True

class EmployerPermission(permissions.BasePermission):
    message = "Only employer are allowed.."

    def has_permission(self, request, view):
        # print(request.user.type)
        if request.user.is_authenticated:
            # print(request.user and request.user.type == "EMPLOYER")
            return request.user and request.user.type == "EMPLOYER"
        return False

    def has_object_permission(self, request, view, obj):
        return True

class TrackingDetailsRetrieveView(generics.RetrieveAPIView):
    permission_classes = [CandidatePermission]
    # permission_classes = [UserWritePermission]
    # queryset = Tracking.objects.all()
    serializer_class = serializers.TrackingSerializer
    lookup_field = 'access_id'

  
    def get(self, request, access_id=None,date=None,date2=None,format=None):
        if request.user.is_authenticated:
            try:
                user=CandidateResume.objects.get(user=self.request.user)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # print(a.id)
            if user.id==access_id:
                if date==None:
                    queryset = Tracking.objects.filter(access_id__exact=access_id).distinct('user_id')
                    count=queryset.count()

                elif date2!=None:
                    date22=datetime.datetime.strptime(date2, '%m%Y').date()
                    month=date22.strftime("%m")
                    queryset = Tracking.objects.filter(access_id__exact=access_id,date__month=month).distinct('user_id')
                    count=queryset.count()

                else:
                    date1=datetime.datetime.strptime(date, '%d%m%Y').date()
                    queryset = Tracking.objects.filter(access_id__exact=access_id,date__contains=date1).distinct('user_id')
                    count=queryset.count()

                serializer = serializers.TrackingSerializer(queryset, many=True)
                data={
                    'count':count,
                    'data':serializer.data
                }
                return Response(data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class EmployerHistoryRetrieveView(generics.RetrieveAPIView,PageNumberPagination):
    permission_classes = [EmployerPermission]
    serializer_class = serializers.EmployerHistoryTrackingSerializer
    lookup_field = 'user_id'
    pagination_class=PageNumberPagination
    # number of items per page by default
    page_size = 5
    # max number of items per page
    max_page_size = 5

    def get_queryset(self):
        user=CustomUser.objects.get(id=self.request.user.id)
        user_id=self.kwargs['user_id']
        # print(user_id)
        if user.id==user_id:
            queryset=Tracking.objects.filter(user_id=user_id,date__lte=datetime.datetime.today(), date__gt=datetime.datetime.today()-datetime.timedelta(days=30)).order_by('access_id','-date').distinct('access_id')
            # queryset.order_by('date')
            return self.paginate_queryset(queryset)

        raise Http404  
    
    def get(self, request,user_id=None,format=None):
        user=CustomUser.objects.get(id=self.request.user.id)
        if user.id==user_id:
            # queryset=Tracking.objects.filter(user_id=user_id).order_by('-date','-updated_time')
            queryset=self.get_queryset()
            # count=queryset.count()
            serializer = serializers.EmployerHistoryTrackingSerializer(queryset, many=True) 
            return self.get_paginated_response(serializer.data)
        raise Http404
        # raise APIException400(request, {'details': "Bad Request"})