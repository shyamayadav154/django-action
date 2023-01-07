from django.urls import include, path
from . import views
from . import routers
from . import recommender

urlpatterns = [
     path("create/<uuid:user_id>/", views.EmployerDetailsCreateView.as_view(), name="employer-details"),
     path('<uuid:user_id>/', views.EmployerDetailsRetrieveView.as_view(), name='employer-retrieve'),
     path('del/<uuid:user_id>/', views.EmployerDetailsDeleteView.as_view(), name='employer-del'),
     path('edit/<uuid:user_id>/', views.EmployerDetailsEdit.as_view(), name='employer-edit'),
     path('employer_template/', include(routers.router.urls)),
     path('industry/', views.Industry_list, name='industry'),
     path('template/recomm/<int:t_id>/',recommender.recommender,name="recomm"),
     # URLS FOR EMPPLOYER TEMPLATE=>
     # 1> GET -> employer_template/ ==> TO GET THE DATA FOR LOGGED IN / AUTHORISED USER
     # 2> POST -> employer_template/ ==> TO CREATE A TEMPLATE FOR THAT PARTICULAR LOGGED IN USER ONLY
     # 3> PUT -> employer_template/<id> ==> TO UPDATE THE VALUE FOR THAT PARTICULAR USER FOR THAT <ID> 
     # 4> PATCH -> employer_template/<id> ==> TO PARTIALLY UPDATE THE VALUE FOR THAT PARTICULAR USER FOR THAT <ID>
     # 5> DELETE -> employer_template/<id> ==> TO DELETE THE PARTICULAR <ID> FOR THAT LOGGED IN USER

]