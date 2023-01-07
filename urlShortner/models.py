from django.db import models

# Create your models here.
class urlShortener(models.Model):
    longurl = models.CharField(max_length=255,null=True,blank=True)
    shorturl = models.CharField(max_length=50,null=True,blank=True, unique=True)
    access_id= models.CharField(max_length=50,null=True,blank=True, unique=True)

    def __str__(self):
        return self.shorturl