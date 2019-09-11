from rest_framework import serializers
from .models import HighScore
from django.contrib.auth.models import User

class HighScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighScore
        fields = ("id", "user", "value")

        def update(self, instance, validated_data):
            instance.value = validated_data.get("value", instance.value)
            instance.user = validated_data.get("user", instance.user)
            instance.save()
            return instance

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
