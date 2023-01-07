from django.db import models
from accounts.models import CustomUser, Employer
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
# INDUSTRY=(
#     ("Full-time", "Full-time"),
#     ("Part-time", "Part-time"),
#     ("Contract", "Contract"),
#     ("Internship", "Internship"),
#     ("Open to work", "Open to work"),
# )
class Industry(models.Model):
    name=models.CharField(max_length=60,blank=True,null=True)

    def __str__(self):
        return self.name

class EmployerDetails(models.Model):
        user = models.OneToOneField(Employer, on_delete=models.CASCADE)
        company_name = models.CharField(max_length=60)
        job_title = models.CharField(max_length=100,default="HR")
        legal_business_name = models.CharField(max_length=60,blank=True,null=True)
        business_pan_number = models.CharField(max_length=60)
        company_identificiation_number = models.CharField(max_length=60,blank=True,null=True)
        industry = models.TextField(max_length = 100,blank=True,null=True)
        # industry=models.ForeignKey(Industry,on_delete=models.CASCADE,blank=True,null=True)
        business_contact_number = models.BigIntegerField(validators=[
                    MaxValueValidator(9999999999999999),
                    MinValueValidator(999999999)
                ])
        website_url = models.CharField(max_length=100,null=True, blank=True)
        company_logo = models.URLField(max_length=200,null=True, blank=True)
        company_address = models.CharField(max_length=200,null=True, blank=True)
        sub_plan = models.CharField(
            max_length=140,
            null=True,
            choices=(
                ('FREE', 'FREE'),
                ('STANDARD', 'STANDARD'),
                ('PREMIUM', 'PREMIUM')
            ),
            default='FREE',
                
            )
        current_subscription_id = models.CharField(max_length=255,null=True, blank=True)

    # stripeCustomerId = models.ForeignKey(StripeUser,on_delete=models.CASCADE,null=True,blank=True)

class Employer_Template(models.Model):
    
    user =models.ForeignKey(Employer, on_delete=models.CASCADE,null=False,blank=True)
    job_title =models.CharField(max_length=100)
    job_description =models.CharField(max_length=100)
    job_type =models.CharField(max_length=100,null=True,blank=True)
    skills =models.CharField(max_length=100)
    subskills =models.CharField(max_length=100,null=True,blank=True)
    experience =models.CharField(max_length=100,null=True,blank=True)
    location =models.CharField(max_length=100,null=True,blank=True)
    notice_time =models.CharField(max_length=100,null=True,blank=True)
    salary_offered =models.CharField(max_length=100,null=True,blank=True)
    is_draft =models.BooleanField(default='1')
     
    
	
    # stripeSubscriptionId = models.CharField(max_length=255)

	# subscription=models.choi

