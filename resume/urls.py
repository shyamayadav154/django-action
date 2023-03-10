
from django.urls import include, path
from .views import (
    Current_city_list,
    Degree_list,
    Get_Suggesstions_for_jobtasks,
    Job_Title_list,
    Open_to_list,
    Resp_title_list,
    ResumeView, 
    ResumeEdit, 
    ResumeCreateView,
    EducationView,
    SearchResumeListView,
    Skills_list,
    Status_list,
    Sub_skills_list,
    UpdateEducationView, 
    WorkDetailView,
    WorkDetailViewset,
    WorkDetailUpdateView, 
    PvtDataView,
    PvtDataUpdateView,
    PvtDataCreateView,
    WorkCreateView,
    CreateEducationView,
    MiscDetailView,
    ResumeDeleteView,
    MiscRUDView,
    MiscCreateView,
    JlistView,CerticationsCreateView,
    CerticationsEditView,
    CerticationsView
    )

urlpatterns = [
path('create/', ResumeCreateView.as_view(), name='resumecreate'),
path('del/<uuid:user_id>/', ResumeDeleteView.as_view(), name='resumedelete'),
path('<uuid:user_id>/', ResumeView.as_view(), name='resume_view'),
path('edit/<uuid:user_id>/', ResumeEdit.as_view(), name='resumeidedit'),
path('pvt/<uuid:access>/', PvtDataView.as_view(), name='pvt'),
path('crpvt/<uuid:access>/', PvtDataCreateView.as_view(), name='pvtcr'),
path('udpvt/<uuid:access>/', PvtDataUpdateView.as_view(), name='udpvt'),
#path('finder/<int:pk>/', ExpFinderView.as_view(), name='finder'),
path('exp/<access>/', WorkDetailView.as_view(), name='workdetail'),
#path('expv/<access>/', WorkDetailViewset.as_view({'get': 'list'}), name='workd'),
path('uexp/<access>/<int:pk>/', WorkDetailUpdateView.as_view(), name='workdetailedit'),
path('cexp/<access>/', WorkCreateView.as_view(), name='workcreate'),
path('edu/<access>/', EducationView.as_view(), name='education'),
path('uedu/<access>/<int:pk>/', UpdateEducationView.as_view(), name='education'),
path('educr/<access>/', CreateEducationView.as_view(), name='educationcreate'),
path('misc/<uuid:access>/', MiscDetailView.as_view(), name='misc'),
path('mirc/<access>/', MiscCreateView.as_view(), name='misccreate'),
path('umisc/<access>/', MiscRUDView.as_view(), name='miscupdate'),
path('search/<access>/', SearchResumeListView.as_view(), name='search'),
path('jlist/', JlistView.as_view()),
path('open_to/', Open_to_list, name='open_to'),
path('status/', Status_list, name='status'),
path('job_title/', Job_Title_list, name='job_title'),
path('skills/', Skills_list, name='skills'),
path('sub_skills/', Sub_skills_list, name='sub_skills'),
path('degree/', Degree_list, name='degree'),
path('resp_title/', Resp_title_list, name='resp_title'),
path('current_city/', Current_city_list, name='current_city'),
path('getJobTaskSuggesstions/', Get_Suggesstions_for_jobtasks, name='suggesstions'),
path("cert/<uuid:access>/",CerticationsView.as_view(), name="certification-details"),
path("certcr/<uuid:access>/",CerticationsCreateView.as_view(), name="certification-create"),
path('ucert/<uuid:access>/<int:pk>/',CerticationsEditView.as_view(), name='certification-update'),


#path('details/<int:owner_id>/', WorkDetailView.as_view(), name='detail'),

#path('orbit/<uuid:user_id>/', ResumeOrbitView.as_view(), name='orbit')
]
#<int:pk>/
