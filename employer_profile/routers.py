from rest_framework import routers
from django.urls import path,include

from . import viewsets

router = routers.DefaultRouter()
router.register('', viewsets.CandidateTemplateViewSet, basename='candidate_template')
# urlpatterns = router.urls
# urlpatterns =[

#     path('employer_template/', include(router.urls)),
# ]