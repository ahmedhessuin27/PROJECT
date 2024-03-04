from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save  
from service.models import Service
# from .models import Providerprofile
# Create your models here.

    
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50,default="",blank=True)
    reset_password_expire = models.DateTimeField(null=True,blank=True)

 
@receiver(post_save, sender=User)
def save_profile(sender,instance, created, **kwargs):

    print('instance',instance)
    user = instance

    if created:
        profile = Profile(user = user)
        profile.save()    




class Providerprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=False , null=True)
    email = models.EmailField(max_length=255, unique=True, blank=False, null=True)
    password = models.CharField(max_length=255,null=True )  
    address = models.TextField(max_length=255)
    phone = models.CharField(max_length=15)
    ratings = models.DecimalField(max_digits=3,decimal_places=2,default=0)
    role = models.CharField(max_length=20 , default='service_provider')
    city = models.CharField(max_length=255)
    image= models.ImageField(upload_to='user_images/%Y/%m/%d/')
    profession=models.TextField(max_length=50)
    fixed_salary=models.CharField(max_length=5)
    id_image= models.ImageField(upload_to='id_images/%Y/%m/%d/')
    service_id=models.ForeignKey(Service,on_delete=models.CASCADE,null=True)



    def __str__(self):
        return self.username
    
class Userprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    provider_favourites=models.ManyToManyField(Providerprofile)
    username = models.CharField(max_length=255, blank=False , null=True)
    email = models.EmailField(max_length=255, unique=True, blank=False, null=True)
    password = models.CharField(max_length=255,null=True )  
    address = models.TextField(max_length=255)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20 , default='customer')
    city = models.CharField(max_length=255)
    image= models.ImageField(upload_to='user_images/%Y/%m/%d/')

    def __str__(self):
        return self.username    


class Review(models.Model):
    provider = models.ForeignKey(Providerprofile, null=True, on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.comment
    



class Work(models.Model): 

    image =models.ImageField(upload_to='work_images/%Y/%m/%d/')    
    provider_id=models.ForeignKey(Providerprofile,on_delete=models.CASCADE,null=True)
