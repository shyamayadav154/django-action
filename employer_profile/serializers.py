from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from stripe import Customer
from accounts.models import CustomUser, Employer
from .models import Employer_Template, EmployerDetails, Industry


class IndustrySeraializer(serializers.ModelSerializer):
    class Meta:
        model=Industry
        fields=['name']
        
class EmployerDetailsSerializer(serializers.ModelSerializer):
    user=serializers.CharField()
    company_name=serializers.CharField(max_length=100)
    # industry=IndustrySeraializer(many=False,allow_null=True)
    class Meta:
        model = EmployerDetails
        fields = '__all__'
        # lookup_field='user_email'
    
class EmployeeSerializer(serializers.ModelSerializer):
    # industry=IndustrySeraializer(many=False,allow_null=True)
    class Meta:
        model = EmployerDetails
        fields = '__all__'  # ('job_title','user_id')
        lookup_field = "user_id"

    def validate(self, attrs):
        user = self.context['request'].user
        # print(user.id)
        # print("hello")
        url_user_id=self.context.get('request').parser_context.get('kwargs').get('user_id') # Access taken from url or lookup field
        # print(url_user_id)
        try:
            q2=CustomUser.objects.get(id__exact=url_user_id)
        except:
            q2=None
        if q2:
            id=q2.id
        else:
            id=None
        body_access=self.initial_data.get('user')
        if body_access:
            try:
                q=CustomUser.objects.get(id__exact=body_access)
            except:
                q=None
            if q:
                acc=q.id
            else:
                acc=None
        if body_access:
            if acc != user.id and user.id != id:
                raise ValidationError('Permission Denied')
        else:
            if id !=  user.id :
                raise ValidationError('Permission Denied')
        return attrs
        
class EmployerTemplateSerializer(serializers.ModelSerializer):

     class Meta:
        model = Employer_Template
        fields = '__all__'

        def validate(self, attrs):
            user = self.context['request'].user
            # print(user)
            # print("hello")
            # url_access=self.context.get('request').parser_context.get('kwargs').get('access') # Access taken from url or lookup field
            body_userid=self.initial_data.get('user')
            try:
                q=Employer.objects.get(id__exact=body_userid)
            except:
                q=None
            
            if user.id != q:
                raise ValidationError('Permission Denied')
            return attrs

        def create(self, validated_data):
            user = self.context['request'].user
            # print(user)
            # print("hello")
            # url_access=self.context.get('request').parser_context.get('kwargs').get('access') # Access taken from url or lookup field
            body_userid=self.initial_data.get('user')
            try:
                q=Employer.objects.get(id__exact=body_userid)
            except:
                q=None
            
            if user.id != q:
                raise ValidationError('Permission Denied')
            else:
                user = Employer_Template(**validated_data)
                # user.set_password(password)
                user.save()
            return user
            # password = validated_data.pop('password')
            # user = CustomUser(**validated_data)
            # user.set_password(password)
            # user.save()
            # return user