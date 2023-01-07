from django.http import Http404
from django.core.exceptions import ValidationError
from requests import Response
from rest_framework import permissions, viewsets,status
from rest_framework.response import Response
from accounts.models import Employer
from . import serializers
from .models import Employer_Template

class UserWritePermission():
    message = 'Permission Denied'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # print("n")
            return request.user and request.user.is_authenticated and request.user.type=='EMPLOYER'
            

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id 
        # if request.data:
            # print(type(obj.user.id))
            # print(type(request.user.id))
            # print(request.data['user'] == request.user.id)
        #     return request.data['user'] == request.user.id
            
        # else:
        #     print("no")
            # print(obj.user.id)
            

class CandidateTemplateViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `LIST`, `CREATE`, `RETRIEVE`,
    `UPDATE` and `DESTROY` actions.
    """

    serializer_class = serializers.EmployerTemplateSerializer
    permission_classes = (UserWritePermission,)
    http_method_names = ['get', 'head','put','patch','delete','post']

    def get_queryset(self):
        return Employer_Template.objects.filter(user__id=self.request.user.id)

    def create(self, request):
            body_userid=request.data['user']
            user=self.request.user
            # print(body_userid)
            # print(user.id)
            try:
                q=Employer.objects.get(id__exact=body_userid)
            except:
                q=None
            if q:
                # print("0")
                if user.id != q.id:
                    # print("1")
                    raise Http404
                else:
                    serializer = serializers.EmployerTemplateSerializer(data=request.data)
                    if serializer.is_valid(): 
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # print("2")
                raise  Http404

    
           