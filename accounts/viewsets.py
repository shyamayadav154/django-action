from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_condition import Or
from rest_framework.pagination import PageNumberPagination
from . import serializers

CustomUser = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    # max_page_size = 1000

class CustomUserModelViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `LIST`, `CREATE`, `RETRIEVE`,
    `UPDATE` and `DESTROY` actions.
    """

    serializer_class = serializers.CustomUserTestSerializer
    permission_classes = (Or(permissions.IsAdminUser,permissions.IsAuthenticated),)
    pagination_class = StandardResultsSetPagination
    queryset = CustomUser.objects.all()
    http_method_names = ['get', 'head','put','patch','delete']

    # def perform_create(self, serializer):
    #     """
    #     When the instance is created, the raw password is saved to the
    #     database instead of the hashed one. This method is implemented
    #     to correct that.
    #     """
    #     # 
    #     return False