from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save    
# Create your models here.
class Userprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
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
    role = models.CharField(max_length=20 , default='customer')
    city = models.CharField(max_length=255)
    image= models.ImageField(upload_to='user_images/%Y/%m/%d/')
    profession=models.TextField(max_length=50)
    fixed_salary=models.CharField(max_length=5)
    id_image= models.ImageField(upload_to='id_images/%Y/%m/%d/')



    def __str__(self):
        return self.username