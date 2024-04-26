from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import Userprofile,Providerprofile , Review , Work , IMage

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
        fields = ('username','email', 'password','phone','image','address','city','id','user')


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
        fields = ('phone','username','password','email','fixed_salary','image','ratings','city','address','id','user','profession','service_id')




class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"



class GetprovidersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Providerprofile
        fields = ('phone','username','password','email','fixed_salary','image','ratings','city','address','id','user','profession','service_id')


class ProviderFavourite(serializers.ModelSerializer):
    
    class Meta:
        model = Providerprofile
        fields = ('phone','username','password','email','fixed_salary','image','ratings','city','address','id','user','profession','service_id')  
        
        
class GetallFavourites(serializers.ModelSerializer):
    
    provider_favourite = ProviderFavourite(source='provider_favourites',many=True,read_only=True)
    
    class Meta:
        model = Userprofile
        fields = ('provider_favourite',)    


class AddTowork(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(),write_only=True)
    class Meta:
        model = Work
        fields = ('images','provider_id')      
    def create(self, validated_data):
        images_data = validated_data.pop('images',None)
        work = Work.objects.create(provider_id=validated_data['provider_id'])
        for image_data in images_data:
            image = IMage.objects.create(image=image_data)
            work.images.add(image)
        return work    
    
    
class SelectedProvider(serializers.ModelSerializer):
    class Meta:
        model = Providerprofile
        fields = ('phone','username','password','email','fixed_salary','image','ratings','city','address','id','user','profession','service_id')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IMage
        fields = ('id', 'image')



class AllWork(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    
    class Meta:
        model = Work
        fields = ('images',)
                  


class PasswordSerializer(serializers.Serializer): 
    password = serializers.CharField(max_length=100)
