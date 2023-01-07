from rest_framework import permissions, viewsets
from .models import CandidateResume
from .serializers import ResumeSerializer

from . import serializers


# class CandidateResumeViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `LIST`, `CREATE`, `RETRIEVE`,
#     `UPDATE` and `DESTROY` actions.
#     """

#     serializer_class = serializers.ResumeSerializer
#     permission_classes = (permissions.AllowAny,)
#     queryset = CandidateResume.objects.all()

class SchemaViewSet(viewsets.ModelViewSet):
    queryset = CandidateResume.objects.all()
    serializer_class = serializers.ResumeSerializer
    lookup_field = "user_id"
    lookup_value_regex = "[^/]+"