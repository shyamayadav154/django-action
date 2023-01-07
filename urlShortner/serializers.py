from rest_framework.serializers import ModelSerializer
from .models import urlShortener

class urlShortenerSerializer(ModelSerializer):
    class Meta:
        model = urlShortener
        fields = '__all__'