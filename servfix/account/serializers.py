from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import Userprofile,Providerprofile , Review

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = ('username','email', 'password','phone','address','city',)

        extra_kwargs = {
            'email' : {'required':True ,'allow_blank':False},
            'username': {'required':True ,'allow_blank':False},
            'password' : {'required':True ,'allow_blank':False, 'min_length':8},
            'phone' : {'required':True ,'allow_blank':False,'min_length':11,'max_length':11},
             'city' : {'required':True ,'allow_blank':False},
            'address' : {'required':True ,'allow_blank':False},
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = ('username','email', 'password','phone','address','city','image')


class ProviderSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Providerprofile
        fields = ('username','email', 'password','phone','address','city','profession','fixed_salary','id_image')

        extra_kwargs = {
            'email' : {'required':True ,'allow_blank':False},
            'username': {'required':True ,'allow_blank':False},
            'password' : {'required':True ,'allow_blank':False, 'min_length':8},
            'phone' : {'required':True ,'allow_blank':False, 'min_length':11,'max_length':11},
             'city' : {'required':True ,'allow_blank':False},
            'address' : {'required':True ,'allow_blank':False},
            'profession' : {'required':True ,'allow_blank':False},
            'fixed_salary' : {'required':True ,'allow_blank':False},
            'id_image' : {'required':True},  
        }


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Providerprofile
        fields = ('phone','address','city','username','password','email','id_image','profession','fixed_salary','image','ratings')




class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"