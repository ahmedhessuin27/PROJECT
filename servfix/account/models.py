from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    address = models.TextField(max_length=255)
    phone = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    role = models.CharField(max_length=20, default="customer")
    city = models.CharField(max_length=255)
    image = models.ImageField(upload_to="user_images/%Y/%m/%d/", null=True, blank=True)

    def __str__(self):
        return self.user.email
