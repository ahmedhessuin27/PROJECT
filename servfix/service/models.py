from django.db import models

class Service(models.Model): 

    name= models.CharField(max_length=255)
    description = models.TextField(1000)
    image =models.ImageField(upload_to='photos/%Y/%m/%d/')

    def __str__(self):
        return self.name
