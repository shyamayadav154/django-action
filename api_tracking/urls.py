
from django.urls import include, path
from . import views

urlpatterns = [
     path('<uuid:access_id>/date/<str:date>/', views.TrackingDetailsRetrieveView.as_view(), name='api_tracking_by_date'),
                               # date should be of format = ddmmyyyy 
     path('<uuid:access_id>/month/<str:date2>/', views.TrackingDetailsRetrieveView.as_view(), name='api_tracking_by_month'),
                               # date2 should be of format = mmyyyy
     path('<uuid:access_id>/', views.TrackingDetailsRetrieveView.as_view(), name='api_tracking_by_accessid'),
     
     path('emp/<uuid:user_id>/', views.EmployerHistoryRetrieveView.as_view(), name='employer_history_tracking_by_userid'),

     # path('emp-test/<uuid:user_id>/', views.EmployerHistoryRetrieveView.as_view(), name='employertest_history_tracking_by_userid'),

]

