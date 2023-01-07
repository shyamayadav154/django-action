from rest_framework import serializers
from .models import Tracking


class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        # fields = '__all__'  # ('job_title','user_id')
        exclude=['email','user_id','counter','view','created_time','username']
        lookup_field = "access_id"

class EmployerHistoryTrackingSerializer(serializers.ModelSerializer):
    access_id=serializers.UUIDField(required=False)
    shortcode_url=serializers.CharField(required=False)
    date= serializers.DateField(required=False)
    class Meta:
        model = Tracking
        # fields = '__all__'  # ('job_title','user_id')
        exclude=['counter','view','email','username','company_name']
        lookup_field = "user_id"


