from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import Userprofile,Providerprofile

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


class ProviderSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Providerprofile
        fields = ('username','email', 'password','phone','address','city','profession','fixed_salary','id_image')

        extra_kwargs = {
            'email' : {'required':True ,'allow_blank':False},
            'username': {'required':True ,'allow_blank':False},
            'password' : {'required':True ,'allow_blank':False, 'min_length':8},
            'phone' : {'required':True ,'allow_blank':False},
             'city' : {'required':True ,'allow_blank':False},
            'address' : {'required':True ,'allow_blank':False},
            'profession' : {'required':True ,'allow_blank':False},
            'fixed_salary' : {'required':True ,'allow_blank':False},
            'id_image' : {'required':True},  
        }
