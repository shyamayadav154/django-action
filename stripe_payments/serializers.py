from rest_framework import serializers
from . models import SubscriptionDetails
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubscriptionDetails
        fields='__all__'