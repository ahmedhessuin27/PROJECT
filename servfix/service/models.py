from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # يستخرج الامتداد من اسم الملف
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension. Only JPG and PNG are allowed.'))
    
class Service(models.Model): 

    name= models.CharField(max_length=255)
    description = models.TextField(1000)
    image =models.ImageField(upload_to='photos/%Y/%m/%d/',validators=[validate_image_extension])

    def __str__(self):
        return self.name
