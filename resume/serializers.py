from typing_extensions import Required
from django.contrib.auth import get_user_model
from django.http import Http404
# from rest_framework import serializers, validators
from serializer_permissions  import serializers,relations
from serializer_permissions.relations import SlugRelatedField
from .models import ( 
    CandidateResume,
    Current_city,
    Degree,
    Job_Title,
    Open_to,
    Resp_Title,
    SearchResume,
    Skills,
    Status,
    Sub_Skills,
    Timeline, 
    WorkDetail, 
    CandidatePrivateData,
    CandidateEducation,
    MiscDetail,
    Job_Task_Suggesstion,
    Certifications)
from rest_framework.permissions import IsAuthenticated,AllowAny
# from rest_framework_serializer_field_permissions import fields                                      # <--
# from rest_framework_serializer_field_permissions.serializers import FieldPermissionSerializerMixin  # <--
# from rest_framework_serializer_field_permissions.permissions import IsAuthenticated,AllowAny
from drf_writable_nested import WritableNestedModelSerializer
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from  django.utils.encoding import smart_text

# CUSTOM SLUGFIELDRELATEDFIELD TO ADD NEW VALUES TO A MANY TO MANY FIELD
# SLUGRELATEDFIELD IS USED TO GET THE VALUES IN A SINGLE LIST
class CreatableSlugRelatedField(relations.SlugRelatedField):
    
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')

# class CreatableSlugRelatedField(serializers.SlugRelatedField):
#     def to_internal_value(self, data):
#         try:
#             return self.get_queryset().get(**{self.slug_field: data})
#         except ObjectDoesNotExist:
#             return self.get_queryset().create(**{self.slug_field: data})  # to create the object
#         except (TypeError, ValueError):
#             self.fail('invalid')

class Open_toSeraializer(serializers.Serializer):
    # name=serializers.SerializerMethodField('get_name')
    name=serializers.CharField()
    class Meta:
        model=Open_to
        fields=['name']

    # def get_name(self, instance):
    #     print("yes")
    #     print(instance.name.all())
    #     return [item.name for item in instance.name]

class StatusSeraializer(serializers.ModelSerializer):
    class Meta:
        model=Status
        fields=['name']

class SkillsSeraializer(serializers.ModelSerializer):
    class Meta:
        model=Skills
        fields=['name']
    
class Sub_SkillsSeraializer(serializers.ModelSerializer):
    class Meta:
        model=Sub_Skills
        fields=['name']

class CurrentCitySeraializer(serializers.ModelSerializer):
    class Meta:
        model=Current_city
        fields=['name']
        depth=1

class Resp_TitleSeraializer(serializers.ModelSerializer):
    class Meta:
        model=Resp_Title
        fields=['name']

class Job_TitleSeraializer(serializers.ModelSerializer):
    class Meta:
        model=Job_Title
        fields=['name']

class DegreeSeraializer(serializers.ModelSerializer):
    class Meta:
        model=Degree
        fields=['name']

class TimelineSeraializer(serializers.ModelSerializer):
    class Meta:
        model=Timeline
        fields='__all__'


class ResumeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateResume
        fields = '__all__'  # ('user',)

    def validate(self, attrs):
        # print("yes")
        user = self.context['request'].user
        # print(user.id)
        # print(attrs['user'].id)
        if attrs['user'].id !=  user.id:
             raise ValidationError('Permission Denied')
        return attrs

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateResume
        fields = '__all__'  # ('job_title','user_id')
        lookup_field = "user_id"

    # def validate(self, attrs):
    #     user = self.context['request'].user
    #     print(user.id)
    #     print(attrs['user'].id)
    #     if attrs['user'].id !=  user.id:
    #          raise ValidationError('Permission Denied')
    #     return attrs

    

class PrivateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidatePrivateData
        fields = '__all__'
        lookup_field = "access"

    def validate(self, attrs):
        user = self.context['request'].user
        url_access=self.context.get('request').parser_context.get('kwargs').get('access') # Access taken from url or lookup field
        try:
            q2=CandidateResume.objects.get(id__exact=url_access)
        except:
            q2=None
        if q2:
            id=q2.user.id
        else:
            id=None
        body_access=self.initial_data.get('access')
        if body_access:
            try:
                q=CandidateResume.objects.get(id__exact=body_access)
            except:
                q=None
            if q:
                acc=q.user.id
            else:
                acc=None
        if body_access:
            if acc != user.id and user.id != id:
                raise ValidationError('Permission Denied')
        else:
            if id !=  user.id :
                raise ValidationError('Permission Denied')
        return attrs

class PrivateUnAuthorisedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CandidatePrivateData
        # fields = '__all__'
        exclude=['current_salary','phone_no','expected_salary','notice_time','currency']
        lookup_field = "access"

class EducationSerializer(serializers.ModelSerializer):
    # degree=DegreeSeraializer( many=True)
    degree= CreatableSlugRelatedField(
        # permissions=(IsAuthenticated, ),
        queryset=Degree.objects.all(),
        many=False,
        slug_field='name',
        allow_null=True,
        hide=True,
        required=False
     )
    class Meta:
        model = CandidateEducation
        fields = '__all__'


    def validate(self, attrs):
        user = self.context['request'].user
        url_access=self.context.get('request').parser_context.get('kwargs').get('access') # Access taken from url or lookup field
        try:
            q2=CandidateResume.objects.get(id__exact=url_access)
        except:
            q2=None
        if q2:
            uid=q2.user.id
        else:
            uid=None
        body_access=self.initial_data.get('access')
        if body_access:
            if body_access == url_access: 
                if user.id == uid:
                    return attrs
                else:
                    raise ValidationError('Permission Denied')
            else:
                raise ValidationError('Permission Denied')     
        else:
            if uid !=  user.id :
                raise ValidationError('Permission Denied')
        return attrs

class WorkDetailSerializer(serializers.ModelSerializer):
    queryset = WorkDetail.objects.all()
    # resp_title=Resp_TitleSeraializer( many=True)
    # skills=SkillsSeraializer( many=True)
    skills= CreatableSlugRelatedField(
        # permissions=(IsAuthenticated, ),
        queryset=Skills.objects.all(),
        many=True,
        slug_field='name',
        allow_null=True,
        # required=False
        # hide=True,
     )
    sub_skills= CreatableSlugRelatedField(
        # permissions=(IsAuthenticated, ),
        queryset=Sub_Skills.objects.all(),
        many=True,
        slug_field='name',
        allow_null=True,
        # required=False
        # hide=True,
     )

    resp_title= CreatableSlugRelatedField(
        # permissions=(IsAuthenticated, ),
        queryset=Resp_Title.objects.all(),
        many=False,
        slug_field='name',
        allow_null=True,
        # required=False
        # hide=True,
     )
    
    # timeline=CreatableSlugRelatedField(
    #     queryset=Timeline.objects.all(), 
    #     slug_field="company_name",
    #     # permission_classes=[IsAuthenticated], 
    #     hide=True,
    #     many=False)
  
    # timeline = TimelineSeraializer(many=False)
    
    class Meta:
        model = WorkDetail
        fields = '__all__'
        # depth=1

    def to_internal_value(self, data):
        if data.get('company_duration') == '':
            data['company_duration'] = 0
        if data.get('team_count') == '':
            data['team_count'] = 0
        if data.get('layout') == '':
            data['layout'] = 0

        return super(WorkDetailSerializer, self).to_internal_value(data)


    def validate(self, attrs):
        user = self.context['request'].user
        url_access=self.context.get('request').parser_context.get('kwargs').get('access') # Access taken from url or lookup field
        try:
            q2=CandidateResume.objects.get(id__exact=url_access)
        except:
            q2=None
        if q2:
            id=q2.user.id
        else:
            id=None
        body_access=self.initial_data.get('access')
        if body_access:
            try:
                q=CandidateResume.objects.get(id__exact=body_access)
            except:
                q=None
            if q:
                acc=q.user.id
            else:
                acc=None
        if body_access:
            if acc != user.id and user.id != id:
                raise ValidationError('Permission Denied')
        else:
            if id !=  user.id :
                raise ValidationError('Permission Denied')
        return attrs

class WorkDetailAnySerializer(serializers.ModelSerializer):
    queryset = WorkDetail.objects.all()
    skills= CreatableSlugRelatedField(
        # permissions=(IsAuthenticated, ),
        queryset=Skills.objects.all(),
        many=True,
        slug_field='name',
        allow_null=True,
        # required=False
        # hide=True,
     )
    sub_skills= CreatableSlugRelatedField(
        # permissions=(IsAuthenticated, ),
        queryset=Sub_Skills.objects.all(),
        many=True,
        slug_field='name',
        allow_null=True,
        # required=False
        # hide=True,
     )

    resp_title= CreatableSlugRelatedField(
        # permissions=(IsAuthenticated, ),
        queryset=Resp_Title.objects.all(),
        many=False,
        slug_field='name',
        allow_null=True,
        # hide=True,
     )

    # timeline = TimelineSeraializer(many=False)

    # timeline=CreatableSlugRelatedField(
    #         queryset=Timeline.objects.all(), 
    #         slug_field="company_name",
    #         # permission_classes=[IsAuthenticated], 
    #         hide=True,
    #         many=False)

    # job_title=CreatableSlugRelatedField(
    #     queryset=Job_Title.objects.all(), 
    #     slug_field="name",
    #     # permission_classes=[IsAuthenticated], 
    #     hide=True,
    #     many=False)
    class Meta:
        model = WorkDetail
        exclude = ['company_name','project_name','objective']
        # depth=1

class WorkCreateSerializer(serializers.ModelSerializer):
    queryset = WorkDetail.objects.all()
    skills= CreatableSlugRelatedField(
        queryset=Skills.objects.all(),
        many=True,
        slug_field='name',
        allow_null=True,
        required=False

     )
    sub_skills= CreatableSlugRelatedField(
        queryset=Sub_Skills.objects.all(),
        many=True,
        slug_field='name',
        allow_null=True,
        required=False

     )

    resp_title= CreatableSlugRelatedField(
        queryset=Resp_Title.objects.all(),
        many=False,
        slug_field='name',
        allow_null=True,
        required=False
     )

    # company_duration=serializers.IntegerField(allow_null=True,required=False,default='')
    # team_count=serializers.IntegerField(allow_null=True,required=False,default='')
    # timeline = TimelineSeraializer(many=False)
    # timeline=CreatableSlugRelatedField(
    #     queryset=Timeline.objects.all(), 
    #     slug_field="company_name",
    #     # permission_classes=[IsAuthenticated], 
    #     hide=True,
    #     many=False)


    # job_title=CreatableSlugRelatedField(
    #     queryset=Job_Title.objects.all(), 
    #     slug_field="name",
    #     # permission_classes=[IsAuthenticated], 
    #     hide=True,
    #     many=False)
    class Meta:
        model = WorkDetail
        fields = '__all__'
        # depth=1
    def to_internal_value(self, data):
        if data.get('company_duration') == '':
            data['company_duration'] = 0
        if data.get('team_count') == '':
            data['team_count'] = 0
        if data.get('layout') == '':
            data['layout'] = 0

        return super(WorkCreateSerializer, self).to_internal_value(data)

    def validate(self, attrs):
        user = self.context['request'].user
        url_access=self.context.get('request').parser_context.get('kwargs').get('access') # Access taken from url or lookup field
        try:
            q2=CandidateResume.objects.get(id__exact=url_access)
        except:
            q2=None
        if q2:
            id=q2.user.id
        else:
            id=None
        body_access=self.initial_data.get('access')
        if body_access:
            try:
                q=CandidateResume.objects.get(id__exact=body_access)
            except:
                q=None
            if q:
                acc=q.user.id
            else:
                acc=None
        if body_access:
            if acc != user.id and user.id != id:
                # print(acc,user.id,id)
                # print("1")
                raise ValidationError('Permission Denied')
        else:
            # print("2")
            if id !=  user.id :
                raise ValidationError('Permission Denied')
        return attrs

class MiscSerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    
    image=serializers.URLField(permission_classes=(IsAuthenticated,), hide=True,allow_blank=True)
    open_to = CreatableSlugRelatedField(
        # permissions=(IsAuthenticated, ),
        permission_classes=(IsAuthenticated,), 
        queryset=Open_to.objects.all(),
        many=False,
        slug_field='name',
        hide=True,
        allow_null=True
    )
    status = CreatableSlugRelatedField(
        # permissions=(IsAuthenticated, ),
        permission_classes=(IsAuthenticated,),         
        queryset=Status.objects.all(),
        many=False,
        slug_field='name',
        hide=True,
        allow_null=True
     )
    # status = serializers.ManyRelatedField(source='status')
    # status=serializers.StringRelatedField(many=True,permissions=(IsAuthenticated, ), hide=True)
    # open_to = serializers.PrimaryKeyRelatedField(queryset=Open_to.objects.all(), many=True)
    # current_city=CreatableSlugRelatedField(
    #     queryset=Current_city.objects.all(), 
    #     slug_field="name",
    #     # permission_classes=[IsAuthenticated], 
    #     hide=True,
    #     many=False,
    #     allow_null=True
    #     )

    # job_title=CreatableSlugRelatedField(
    #     queryset=Job_Title.objects.all(), 
    #     slug_field="name",
    #     # permission_classes=[IsAuthenticated], 
    #     hide=True,
    #     many=False)

    timeline = TimelineSeraializer(many=True,allow_null=True)
    class Meta:
        model = MiscDetail
        fields = '__all__'
        lookup_field = "access"

    def validate(self,attrs):
        user = self.context['request'].user
        # print(user)
        url_access=self.context.get('request').parser_context.get('kwargs').get('access') # Access taken from url or lookup field
        try:
            q=CandidateResume.objects.get(id__exact=url_access)
        except:
            q=None
        if q:
            acc=q.user.id
        else:
            acc=None
        if attrs['access'].user.id !=  user.id and user.id != acc:
             raise ValidationError('Permission Denied')
        return attrs

class MiscUnAuthorisedSerializer(serializers.ModelSerializer):
    # job_title=relations.SlugRelatedField(
    #     queryset=Job_Title.objects.all(), 
    #     slug_field="name",
    #     # permission_classes=[IsAuthenticated], 
    #     hide=True,
    #     many=False)
    # current_city=relations.SlugRelatedField(
    #     queryset=Current_city.objects.all(), 
    #     slug_field="name",
    #     # permission_classes=[IsAuthenticated], 
    #     hide=True,
    #     many=False,
    #     allow_null=True
    #     )
    
    open_to = CreatableSlugRelatedField(
        # permissions=(IsAuthenticated, ),
        # permission_classes=(IsAuthenticated,), 
        queryset=Open_to.objects.all(),
        many=False,
        slug_field='name',
        hide=True,
        allow_null=True
    )
    status = CreatableSlugRelatedField(
        # permissions=(IsAuthenticated, ),
        # permission_classes=(IsAuthenticated,),         
        queryset=Status.objects.all(),
        many=False,
        slug_field='name',
        hide=True,
        allow_null=True
    )
    
    timeline = TimelineSeraializer(many=True,allow_null=True)
    image=serializers.URLField(hide=True,allow_blank=True)
    class Meta:
        model = MiscDetail
        fields = '__all__'
        # exclude=['open_to','status']
        lookup_field = "access"

class SearchResumeSerializer(serializers.ModelSerializer):
    access = ResumeSerializer()
    misc_detail = MiscSerializer()
    education = EducationSerializer()
    work_detail= WorkDetailSerializer()
    private_data= PrivateSerializer()
    queryset=SearchResume.objects.all()
    class Meta:
        model = SearchResume
        fields = ['access','misc_detail','education','work_detail','private_data']
        depth = 2
        
#         # lookup_field="misc_detail__acess"
# from django.db import models
# class VocabListSerializer(serializers.ListSerializer):

#     def to_representation(self, data):
#         iterable = data.all() if isinstance(data, models.Manager) else data
#         return {
#             job_title: super().to_representation(Job_Task_Suggesstions.objects.filter(job_title=job_title))
#             for job_title in Job_Task_Suggesstions.objects.all()
#         }

class Job_sugesstions_serializer(serializers.ModelSerializer):

    # job_title=Job_TitleSeraializer(many=True)
    class Meta:
        model=Job_Task_Suggesstion
        fields='__all__'
    
class CertificationsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Certifications
        fields='__all__'




# class job(serializers.Serializer):

#     class Meta:
#         list_serializer_class=VocabListSerializer

# class DictionarySerializer(serializers.ModelSerializer):
#     job = serializers.SerializerMethodField()
#     job_title=Job_TitleSeraializer()
#     suggessted_tasks=serializers.CharField()

#     def get_job(self, instance):
#         return DictionarySerializer(instance.job_title.filter(job_title=instance.job_title), many=True).data

#     # def get_group_b(self, instance):
#     #     return Job_TitleSeraializer(instance.job_titiles.filter(job_title='b'), many=True).data

#     class Meta:
#         model = Job_Task_Suggesstions
#         fields = ('job','job_title','suggessted_tasks')