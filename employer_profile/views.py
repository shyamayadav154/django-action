from django.shortcuts import render
from rest_framework import generics, permissions
from . import serializers
from .models import EmployerDetails, Industry
from rest_framework.permissions import AllowAny
from .viewsets import UserWritePermission
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
class EmployerDetailsCreateView(generics.CreateAPIView):
    
    permission_classes = [UserWritePermission]
    # permission_classes = [AllowAny]
    model = EmployerDetails
    serializer_class = serializers.EmployeeSerializer
    queryset = EmployerDetails.objects.all()
    lookup_field = "user_id"
    
class EmployerDetailsRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [UserWritePermission]
    queryset = EmployerDetails.objects.all()
    serializer_class = serializers.EmployeeSerializer
    lookup_field = 'user_id'

class EmployerDetailsDeleteView(generics.DestroyAPIView):
    # permission_classes = [AllowAny]
    permission_class = [UserWritePermission]
    queryset = EmployerDetails.objects.all()
    serializer_class = serializers.EmployerDetailsSerializer
    lookup_field = 'user_id'

class EmployerDetailsEdit(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [UserWritePermission]
    queryset = EmployerDetails.objects.all()
    serializer_class = serializers.EmployeeSerializer
    lookup_field = 'user_id'

@api_view(['GET'])
def Industry_list(request):
    name = list(Industry.objects.values_list('name', flat=True))
    return Response({"name":name})