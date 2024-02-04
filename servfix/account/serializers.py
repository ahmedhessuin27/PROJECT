from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import Userprofile


class SingUpSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False)
    username = serializers.CharField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)
    phone = serializers.CharField(allow_blank=False)
    city = serializers.CharField(allow_blank=False)
    address = serializers.CharField(allow_blank=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = "__all__"


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False)
