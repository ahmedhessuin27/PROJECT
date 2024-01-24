from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Userprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    password = models.CharField(max_length=255)  
    address = models.TextField(max_length=255)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20 , default='customer')
    city = models.CharField(max_length=255)
    image= models.ImageField(upload_to='user_images/%Y/%m/%d/')

    def __str__(self):
        return self.username
