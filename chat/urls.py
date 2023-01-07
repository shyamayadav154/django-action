from django.urls import include, path,re_path
from .views import Email

urlpatterns = [
    path('email-chat/', Email),
]