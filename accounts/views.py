from asyncio import exceptions
from django.contrib.auth import get_user_model
from requests import request
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login

# from accounts.models import Nps_Survey
from .utils import get_tokens_for_user
from rest_framework import status
from . import serializers
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.shortcuts import redirect
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.linkedin_oauth2.views import LinkedInOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter

from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from .renderers import UserRenderer
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from employer_profile.models import EmployerDetails

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponsePermanentRedirect
import os
from rest_framework.decorators import api_view
from anymail.message import AnymailMessage 
import json
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime
from django.contrib.auth.models import update_last_login



CustomUser = get_user_model()

@api_view(['POST'])
def Send_account_verify_email(request,to_email=None):
    if to_email is None:
        received_json_data=json.loads(request.body)
        to_email=received_json_data['to_email']
        # to_email=request.POST.get("to_email")
    # print(to_email)
    # print(request.POST['to_email'])
    # print(request.body)
    # print("yessssss")
    try:
        user = CustomUser.objects.get(email=to_email)
        token = RefreshToken.for_user(user).access_token
        current_site="api.mevvit.com"
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.email +"\n"+ 'Welcome To Mevvit' \
            ' Use the link below to verify your email : \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your Mevvit email',"link":absurl}
        html_body = render_to_string("email-verify.html",data)
    except exceptions as e:
        status_code = status.HTTP_404_NOT_FOUND
        return Response(status=status_code)
    try:
            headers = {'Reply-To': "no-reply@mevvit.com"}
            message = AnymailMessage(
            subject=data['email_subject'],#"Hurray! Message from {s}".format(s=from1),
            body=html_body,
            to=[data['to_email']],
            headers=headers#abhishek@appwharf.co
            # tags=["Onboarding"],  # Anymail extra in constructor
            )
            message.content_subtype = "html"
            message.from_email = "no-reply@mevvit.com"
            message.send()

            # send_mail(data['email_subject'],data['email_body'], 'anirbanchakraborty967@gmail.com',[data['to_email']])
    except exceptions as e:
        status_code = status.HTTP_404_NOT_FOUND
        return Response(status=status_code)
    status_code = status.HTTP_200_OK
    return Response(status=status_code)
    # send_mail(email_subject,email_body, 'anirbanchakraborty967@gmail.com',to_email)

class CustomRedirect(HttpResponsePermanentRedirect):
    # print(os.environ.get('APP_SCHEME'))
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'https']

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    **GET:** List details for a ``CustomUser``.
    **PUT:** Update details of a ``CustomUser``.
    **DELETE:** Delete a specific ``CustomUser``.
    This view can be used to retrieve data for the current logged in user.
    """

    queryset = CustomUser.objects.all()
    serializer_class = serializers.CustomUserRetrieveSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
        
class AuthUserRegistrationView(APIView):
    serializer_class = serializers.CustomUserSerializer
    permission_classes = (AllowAny, )
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        company_name=request.data.get('company_name',' ')
        job_title=request.data.get('job_title',' ')
        business_pan_number=request.data.get('business_pan_number',' ')
        business_contact_number=request.data.get('business_contact_number',' ')
        if company_name==None:
            company_name=""
        if valid:
            serializer.save()
            user_data = serializer.data
            user = CustomUser.objects.get(email=user_data['email'])
            if user.type=='EMPLOYER':
                employee=EmployerDetails.objects.create(user=user,company_name=company_name,job_title=job_title,business_pan_number=business_pan_number,business_contact_number=business_contact_number)
                employee.save()
            token = RefreshToken.for_user(user).access_token
            # current_site = get_current_site(request).domain
            current_site="api.mevvit.com"
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            # email_body = 'Hi '+user.email +'\n' + 'Welcome To Mevvit' \
            #     'Use the link below to verify your email \n' + absurl
            data = {'to_email': user.email,
                    'email_subject': 'Verify your Mevvit email',"link":absurl}
            html_body = render_to_string("email-verify.html",data)
            plain_message = strip_tags(html_body)

            try:
                    headers = {'Reply-To': "no-reply@mevvit.com"}
                    message = AnymailMessage(
                    subject=data['email_subject'],#"Hurray! Message from {s}".format(s=from1),
                    body=html_body,
                    to=[data['to_email']],
                    headers=headers#abhishek@appwharf.co
                    # tags=["Onboarding"],  # Anymail extra in constructor
                    )
                    message.content_subtype = "html"
                    message.from_email = "no-reply@mevvit.com"
                    message.send()

            except exceptions as e:
                pass
            # send_mail(data['email_subject'],data['email_body'], 'anirbanchakraborty967@gmail.com',[data['to_email']])
            Send_account_verify_email(self.request._request,user.email)
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

class VerifyEmail(APIView):
    serializer_class = serializers.EmailVerificationSerializer

    def get(self, request):
        
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return redirect('https://www.mevvit.com/')
            else:
                return redirect('https://mevvit.com/')

            return Response({'status':'verified','email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
                return redirect('https://mevvit.com/404')
            # return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return redirect('https://mevvit.com/404')
            # return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class AuthUserLoginView(APIView):

    serializer_class = serializers.UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            try:
                user1=CustomUser.objects.get(email=serializer.data['email'])
            except:
                user1 = None
            update_last_login(None, user1)
            if user1:
                user1.Lastlogin1=datetime.datetime.now()
                user1.save()
            # try:
            #    nps=Nps_Survey.objects.get(user=user1)
            # except:
            #     nps=None
            # if nps:
            #     Nps_Survey.objects.filter(user=user1).update(Last_login=datetime.datetime.now())
            # else:
            #     last_login=Nps_Survey.objects.create(user=user1,Last_login=datetime.datetime.now())
            #     last_login.save()
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'user':{
                        'access': serializer.data['access'],
                        'refresh': serializer.data['refresh'],
                        'id': serializer.data['id'],
                        'first_name':serializer.data['first_name'],
                        'last_name':serializer.data['last_name'],
                        'email': serializer.data['email'],
                        'type': serializer.data['type'],
                }
            }
            # print(f' 2nd function time: {time.time() - startT}ms')
            return Response(response, status=status_code)

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = serializers.ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(SocialLoginView):
    # disable authentication, make sure to override `allowed origins` in settings.py in production!
    authentication_classes = []
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"  # frontend application url
    client_class = OAuth2Client

class GoogleLoginView2(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class LinkedinLoginView(SocialLoginView):
    # disable authentication, make sure to override `allowed origins` in settings.py in production!
    authentication_classes = []
    adapter_class = LinkedInOAuth2Adapter
    callback_url = "http://localhost:3000"  # frontend application url
    client_class = OAuth2Client

class GithubLoginView(SocialLoginView):
    # disable authentication, make sure to override `allowed origins` in settings.py in production!
    authentication_classes = []
    adapter_class = GitHubOAuth2Adapter
    # callback_url = "http://localhost:3000"  # frontend application url
    client_class = OAuth2Client


# class ForgotPassword(APIView):
#     serializer_class = serializers.ForgotPasswordSerializer
#     permission_classes = (AllowAny, )
#     # renderer_classes = (UserRenderer,)

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         valid = serializer.is_valid(raise_exception=True)

#         if valid:
#             # serializer.save()
#             user_data = serializer.data
#             try:
#                 user = CustomUser.objects.get(email=user_data['email'])
#             except CustomUser.DoesNotExist:
#                 user = None
#                 return Response({'error':'email doesnot exist'})
#             token = RefreshToken.for_user(user).access_token
#             current_site = "127.0.0.1:8000"# get_current_site(request).domain
#             relativeLink = reverse('forgot-password')
#             absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
#             email_body = 'Hi '+user.email + \
#                 ' Use the link below to reset your password \n' + absurl
#             data = {'email_body': email_body, 'to_email': user.email,
#                     'email_subject': 'Reset Your Mevvit Password'}
#             # Util.send_email(data)
#             # EmailMessage(
#             # subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
#             try:
#                     headers = {'Reply-To': "no-reply@mevvit.com"}
#                     message = AnymailMessage(
#                     subject=data['email_subject'],#"Hurray! Message from {s}".format(s=from1),
#                     body=data['email_body'],
#                     to=[data['to_email']],
#                     headers=headers#abhishek@appwharf.co
#                     # tags=["Onboarding"],  # Anymail extra in constructor
#                     )
#                     message.from_email = "no-reply@mevvit.com"
#                     message.send()

#             except exceptions as e:
#                 pass
#             # send_mail(data['email_subject'],data['email_body'], 'anirbanchakraborty967@gmail.com',[data['to_email']])
#             # print(email_body)
#             status_code = status.HTTP_200_OK

#             response = {
#                 'success': True,
#                 'statusCode': status_code,
#                 'message': 'Password reset link has been sent!',
#                 # 'user': serializer.data
#             }
#             return Response(response, status=status_code)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordEmailRequestSerializer
    permission_classes=(AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')
        try:
                user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
                user = None
                return Response({'error':'email doesnot exist'}, status=status.HTTP_400_BAD_REQUEST)

        
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = "api.mevvit.com" #get_current_site(request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            # redirect_url = request.data.get('redirect_url', '')
            # redirect_url=settings.RESET_REDIRECT_URL
            absurl = 'http://'+current_site + relativeLink
            # email_body = 'Hello, \n Use link below to reset your password  \n' + \
            #     absurl
            data = {'to_email': user.email,
                    'email_subject': 'Reset your Mevvit passsword',"link":absurl}
            html_body = render_to_string("reset-password.html",data)
            try:
                headers = {'Reply-To': "no-reply@mevvit.com"}
                message = AnymailMessage(
                subject=data['email_subject'],#"Hurray! Message from {s}".format(s=from1),
                body=html_body,
                to=[data['to_email']],
                headers=headers#abhishek@appwharf.co
                # tags=["Onboarding"],  # Anymail extra in constructor
                )
                message.content_subtype = "html"
                message.from_email = "no-reply@mevvit.com"
                message.send()

            except exceptions as e:
                pass
        else:
            return Response({'error': 'Email-id is not valid or not registered with mevvit.'}, status=status.HTTP_400_BAD_REQUEST)

            # send_mail(data['email_subject'],data['email_body'], 'anirbanchakraborty967@gmail.com',[data['to_email']])
            # Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = serializers.SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        # redirect_url = request.GET.get('redirect_url')
        # print("1")
        # print(redirect_url)
        redirect_url=settings.RESET_REDIRECT_URL
        # print(redirect_url)
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            # print(id)
            user = CustomUser.objects.get(id=id)
            # print(user)
            # print(user.id)
            # print(PasswordResetTokenGenerator().check_token(user, token))
            if not PasswordResetTokenGenerator().check_token(user, token):
                # print("2")
                if len(redirect_url) > 3:
                    # print("3")
                    # return Response({'error': 'Email-id is not valid or not registered with mevvit.'}, status=status.HTTP_400_BAD_REQUEST)
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    # print("4")
                    # return Response({'error': 'Email-id is not valid or not registered with mevvit.'}, status=status.HTTP_400_BAD_REQUEST)
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                # print("5")
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                # print("6")
                return Response({'error': 'Email-id is not valid or not registered with mevvit.'}, status=status.HTTP_400_BAD_REQUEST)
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                # print("7")
                if not PasswordResetTokenGenerator().check_token(user):
                    # print("8")
                    # return Response({'error': 'Email-id is not valid or not registered with mevvit.'}, status=status.HTTP_400_BAD_REQUEST)
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(generics.GenericAPIView):
    permission_classes=[AllowAny]
    serializer_class = serializers.SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

from rest_framework_simplejwt.tokens import RefreshToken

class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('access'))
        #print(token)
        token.blacklist()
        return Response("Success")


