from django.urls import include, path
from . import routers, views,viewsets
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import GithubLoginView, GoogleLoginView, LinkedinLoginView
from allauth.socialaccount.providers.github import views as github_views

import uuid
# account_list = viewsets.CustomUserModelViewSet{
#     'get': 'list',
#     'post': 'create'
# })
urlpatterns = [
    path('data/', views.UserRetrieveUpdateDestroyAPIView.as_view(),
         name='user-data'),  # get data for the currently logged in user
    path('getData/', include(routers.router.urls)),  # provides a few default
#     path("upd/",account_list, name='update')
    # views that we can use for our CRUD operations.
    path('register/', views.AuthUserRegistrationView.as_view(),name="register"),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('send_email_verify/', views.Send_account_verify_email, name="send_email_verify"),
#     path('forgot-password/', views.ForgotPassword.as_view(), name="forgot-password"),
#     path('reset-password/', views.ResetPassword.as_view(), name="reset-password"),
    path('change_pass/', views.ChangePasswordView.as_view(),name="change-pass"),
    path('login/', views.AuthUserLoginView.as_view(),name="login"),
    path('login/refresh/',TokenRefreshView.as_view(),name="login-refresh"),
    path("google/", GoogleLoginView.as_view(), name="google"),
    path("linkedin/", LinkedinLoginView.as_view(), name="linkedin"),
    path("github/", GithubLoginView.as_view(), name="github"),
    # path("employer_details/", EmployerDetailsCreateView.as_view(), name="employer-details"),
    # path('employer_details/<uuid:user_id>/', EmployerDetailsRetrieveView.as_view(), name='employer-retrieve'),

    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('logout/', views.BlacklistRefreshView.as_view(), name="logout"),

    # path('password_reset_api/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # path("accounts-new/", include('allauth.urls'), name="google"),  
]
