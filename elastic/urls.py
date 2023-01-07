from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

from .views import WorkDetailDocumentView

router = DefaultRouter()
router.register("work_detail", WorkDetailDocumentView, basename="work_detail")
router.register("cand_edu", CandidateEducationDocumentView, basename="cand_edu")
router.register("private_data", PrivateDataDocumentView, basename="private_data")

urlpatterns = [
    # path('search/' , CandidateEducationDocumentView.as_view({'get': 'list'})),
    path('search-w/' , WorkDetailDocumentView.as_view({'get': 'list'})),
    path('search1/<str:query>' , OnlySearchWorkdetails.as_view()),
    path('misc/' , MiscDetailElasticSearch.as_view()),
    path('search/',search, name='search'),

]
urlpatterns += router.urls

# FOR SEARCHING IN ALL FIELDS
# http://127.0.0.1:8000/search/private_data/?current_salary__range=0__5000000
# search/work_detail/$ [name='work_detail-list']
# search/work_detail\.(?P<format>[a-z0-9]+)/?$ [name='work_detail-list']
# search/work_detail/functional_suggest/$ [name='work_detail-functional-suggest']
# search/work_detail/functional_suggest\.(?P<format>[a-z0-9]+)/?$ [name='work_detail-functional-suggest']
# search/work_detail/suggest/$ [name='work_detail-suggest']
# search/work_detail/suggest\.(?P<format>[a-z0-9]+)/?$ [name='work_detail-suggest']
# search/work_detail/(?P<pk>[^/.]+)/$ [name='work_detail-detail']
# search/work_detail/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='work_detail-detail']

# http://127.0.0.1:8000/search/search-w/?search=TEXT_TO_SEARCH
# http://127.0.0.1:8000/search/search/?search=TEXT_TO_SEARCH

# http://127.0.0.1:8000/search/private_data/?current_salary__range=0__5000000
