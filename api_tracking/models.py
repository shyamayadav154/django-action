from django.db import models
import datetime
# Create your models here.
class Tracking(models.Model):
    user_id=models.CharField(max_length = 50,blank=True,null=True)
    email=models.EmailField()
    username=models.CharField(max_length = 50,blank=True,null=True)
    company_name=models.CharField(max_length = 50,blank=True,null=True)
    job_title=models.CharField(max_length = 80,blank=True,null=True)
    access_id=models.CharField(max_length = 50,blank=True,null=True)
    shortcode_url=models.CharField(max_length = 100,blank=True,null=True,default="")
    view=models.CharField(max_length = 50,blank=True,null=True)
    counter=models.IntegerField(default='0')
    date=models.DateField()
    created_time = models.TimeField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)
 