# serializers.py

from rest_framework import serializers
from .models import Avatar, Eye

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['avatar_url', 'sunglasses_image']

class EyeSerializer(serializers.Serializer):
    class Meta:
        model = Eye
        fields = ['avatar_url', 'left_eye', 'right_eye']
