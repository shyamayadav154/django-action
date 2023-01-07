import json
from resume.models import CandidateEducation,MiscDetail

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *


class CandidateEducationSerializer(DocumentSerializer):

    class Meta(object):
        """Meta options."""
        # model = CandidateEducation
        document = CandidateEducationDocument
        fields = [
            "id",
            'degree',
            'college_name',
            'start_year',
            'end_year',
            'access'
        ]
        # def get_location(self, obj):
        #     """Represent location value."""
        #     try:
        #         return obj.location.to_dict()
        #     except:
        #         return {}

class WorkDetailSerializer1(DocumentSerializer):

    class Meta(object):
        """Meta options."""
        # model = CandidateEducation
        document = OnlySearchWorkdetailDocument
        fields = [
            "id",
            "sub_skills",
            "skills",
            "resp_title",
            "access",
            "company_name",
            "my_tasks"
           
        ]

class MiscDetailSerializer1(DocumentSerializer):

    class Meta(object):
        """Meta options."""
        # model = CandidateEducation
        document = MiscdetailDocument
        fields = [
            "id",
            "job_title",
            "open_to",
            "status",
            "access",
            "locations",
            "current_city"
           
        ]

class PrivateDataSerializer(DocumentSerializer):
    class Meta(object):
        """Meta options."""
        # model = CandidateEducation
        document = PrivateDataDocument
        fields = [
            "id",
            "name",
            # "phone_no",
            "current_salary",
            "expected_salary",
            "notice_time",
            "access",
        ]