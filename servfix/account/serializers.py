from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import Userprofile

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = ('username','email', 'password','phone','address','city',)

        extra_kwargs = {
            'email' : {'required':True ,'allow_blank':False},
            'username': {'required':True ,'allow_blank':False},
            'password' : {'required':True ,'allow_blank':False, 'min_length':8},
            'phone' : {'required':True ,'allow_blank':False},
             'city' : {'required':True ,'allow_blank':False},
            'address' : {'required':True ,'allow_blank':False},
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = "__all__"
