from django.urls import path
from . import views
from django.views.generic import RedirectView

# urlpatterns = [
#     path('ZY9J3y/', RedirectView.as_view(url='https://www.facebook.com'))
# ]
urlpatterns = [
    path('shorten/', views.makeshorturl),
    path('CustomShorten/<accessid>/', views.createCustomcode), ## Create Custom code by passing access_id as url parameter
    path('CustomShorten/get/<shortcode>/', views.getCustomCode), ## Get Custom code by passing customcode as url parameter
    path('getCustomCode/', views.getCustomCodeByAccessid), ## Get Custom code by ppassing access_id as payload
    path('<str:shorturl>', views.redirectUrl,name="redirectt"),
    # path('ZY9J3y/', RedirectView.as_view(url='https://www.facebook.com'))
]