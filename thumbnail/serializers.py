from rest_framework.serializers import ModelSerializer
from .models import Image, ExpiringLink


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ExpiringLinkSerializer(ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = '__all__'
