from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from accounts.models import CustomUser
from .models import urlShortener
from .serializers import urlShortenerSerializer
from django.conf import settings
import random
from rest_framework import status
from resume.models import CandidateResume
import re


@api_view(['POST'])
def makeshorturl(request):
    data = request.data
    s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    shorturl = ("".join(random.sample(s, 6)))
    longurl = data['longurl']
    try:
        queryset= urlShortener.objects.get(longurl=longurl)
    except:
        queryset=None
    if not queryset:
        urlShortener.objects.create(
            longurl=data['longurl'],
            shorturl=shorturl
        )
    else:
        shorturl=queryset.shorturl
    full_shorturl = settings.FRONTEND_BASE_URL+shorturl
    return Response({'longurl': longurl, 'full_shorturl':full_shorturl,'shorturl':shorturl})

@api_view(['POST'])
@permission_classes([AllowAny])
def createCustomcode(request,accessid):

    if request.method=="POST":
        if request.user.is_authenticated:
            data = request.data
            shorturl=data['shortcode']
            access_id = accessid
            # a=re.sub('[^A-Za-z0-9' ']+', '', shorturl)
            # print(a)
            # print(len(a))
            # print(shorturl.isalnum())
            # shortcode=''.join(e for e in shorturl if e.isalnum())
            if not shorturl.isalnum():
                return Response({"error":"White-spaces and special characters are not allowed"},status=status.HTTP_403_FORBIDDEN)
            
            try:
                short= urlShortener.objects.get(shorturl=shorturl)
            except:
                short=None

            if short:
                return Response({"error":"Custom code already in use"},status=status.HTTP_403_FORBIDDEN)

            try:
                queryset= urlShortener.objects.get(access_id=access_id)
            except:
                queryset=None
            
            if queryset:
                if queryset.shorturl==shorturl:
                        return Response({'shorturl':shorturl,'access_id':access_id},status=status.HTTP_200_OK)        
                else:
                    urlShortener.objects.filter(access_id=access_id).update(shorturl=shorturl)
            else:
                queryset=urlShortener.objects.create(
                    access_id=access_id,
                    shorturl=shorturl
                )
                access_id=queryset.access_id
            # full_shorturl = settings.FRONTEND_BASE_URL+shorturl
            return Response({'shorcode':shorturl,'access_id':access_id},status=status.HTTP_200_OK)
        return Response({'error':"Not Authenticated"},status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def getCustomCode(request,shortcode):
    if request.method=="GET":      
        try:
            queryset= urlShortener.objects.get(shorturl=shortcode)
            # print("8")
        except:
            # print("5")
            queryset=None
        
        if queryset:
            # print("6")
            return Response({"access_id":queryset.access_id,"shortcode":queryset.shorturl},status=status.HTTP_200_OK)

        return Response({"details":"Not found"},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def getCustomCodeByAccessid(request):
    if request.method=="POST": 
        data = request.data
        accessid=data['access_id']     
        try:
            queryset= urlShortener.objects.get(access_id=accessid)
            # print("8")
        except:
            # print("5")
            queryset=None
        
        if queryset:
            # print("6")
            return Response({"shortcode":queryset.shorturl},status=status.HTTP_200_OK)

        return Response({"details":"Not found"},status=status.HTTP_404_NOT_FOUND)


def redirectUrl(request, shorturl):
    try:
        obj = urlShortener.objects.get(shorturl=shorturl)
    except urlShortener.DoesNotExist:
        obj = None

    if obj is not None:
        return redirect(obj.longurl)
    else:
        return redirect('https://mevvit.com/404')
