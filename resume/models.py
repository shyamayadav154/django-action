from email.errors import MisplacedEnvelopeHeaderDefect
from django.db import models
from accounts.models import Candidate, CustomUser
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from partial_date import PartialDateField
from django.core.validators import RegexValidator


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class Open_to(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name        
class Status(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name
class Job_Title(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name
class Skills(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name
    
class Sub_Skills(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name

class Current_city(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name

class Degree(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name

class Resp_Title(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name


class CandidateResume(models.Model): #Basic resume change the name of this class
    user = models.OneToOneField(Candidate, on_delete=models.CASCADE, null=False, blank=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    declared=models.BooleanField(default=False,blank=True,null=True)
    last_updated= models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Timeline(models.Model):

    start_date=PartialDateField(null=True,blank=True)
    end_date=PartialDateField(null=True,blank=True)
    present=models.BooleanField(default=False,blank=True,null=True)
    job_title = models.TextField(max_length=100, null=True, blank=True)#models.ForeignKey(Job_Title,on_delete=models.CASCADE,blank=True,null=True)    
    company_name = models.TextField(max_length=100, null=True, blank=True)

class MiscDetail(models.Model):

    job_title=models.TextField(max_length=200,blank=True,null=True)
    email=models.CharField(max_length=200,null=True, blank=True)
    open_to = models.ForeignKey(Open_to,on_delete=models.CASCADE,blank=True,null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,blank=True,null=True)
    areas = models.TextField(blank=True,null=True)
    workplace_type = models.TextField(blank=True,null=True)
    locations = models.TextField(blank=True,null=True)
    # current_city = models.ForeignKey(Current_city,on_delete=models.CASCADE,null=True)
    currently_city=models.CharField(max_length=100,null=True, blank=True)
    current_employer=models.TextField(max_length=200,null=True, blank=True)
    image = models.URLField(max_length=200,null=True, blank=True)
    access = models.OneToOneField(CandidateResume, on_delete=models.CASCADE, null=False, blank=True, unique=True)
    github = models.URLField(max_length=200,null=True, blank=True)
    linkedin = models.URLField(max_length=200,null=True, blank=True)
    twitter = models.URLField(max_length=200,null=True, blank=True)
    timeline= models.ManyToManyField(Timeline, blank=True)

    def __str__(self):
        return str(self.access)


class CandidateEducation(models.Model):
    college_name = models.TextField(max_length=100,null=True,blank=True)
    degree= models.ForeignKey(Degree, on_delete=models.CASCADE, null=True, blank=True)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    present=models.BooleanField(default=False,blank=True,null=True)
    # layout=models.CharField(max_length=200,null=True, blank=True)
    access = models.ForeignKey(CandidateResume, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return str(self.access)

class WorkDetail(models.Model): 
    company_name = models.TextField(max_length=100, null=True, blank=True)
    company_logo = models.URLField(max_length=200,null=True, blank=True)
    company_duration = models.IntegerField(null=True, blank=True) # No of months / Years candidate has worked here
    project_name = models.TextField(max_length=60,null=True, blank=True)
    team_count = models.IntegerField(null=True, blank=True)
    resp_title =  models.ForeignKey(Resp_Title, on_delete=models.CASCADE, null=True, blank=True)# get list of title from database or frontend
    my_tasks = models.TextField(max_length=1000, null=True, blank=True) # 
    layout=models.IntegerField(null=True, blank=True)
    objective = models.TextField(max_length=120, blank=True) # 
    challenges = models.TextField(max_length=300, blank=True) # big text field only add this if it's applicable
    outcome = models.TextField(max_length=120, blank=True)
    learnings = models.TextField(max_length=300, blank=True)
    skills=models.ManyToManyField(Skills, blank=True)
    sub_skills=models.ManyToManyField(Sub_Skills,blank=True)
    ext_links = models.TextField(max_length=500,blank=True,null=True) # links for projects github, linkedIN, website etc
    access = models.ForeignKey(CandidateResume, on_delete=models.CASCADE, blank=True,null=False)
 
    def __str__(self):
        return str(self.access)
class CandidatePrivateData(models.Model):
    name = models.TextField(max_length=230, blank=True)
    phone_no = models.BigIntegerField(null=True,blank=True,validators=[
            MaxValueValidator(999999999999),
            MinValueValidator(999999999)
        ])
    currency=models.CharField(max_length=50,null=True, blank=True)   
    current_salary = models.IntegerField(null=True, blank=True)
    expected_salary = models.IntegerField(null=True, blank=True)
    total_experience= models.IntegerField(null=True, blank=True)
    notice_time = models.IntegerField(null=True, blank=True) #
    access = models.OneToOneField(CandidateResume, on_delete=models.CASCADE, null=False, blank=True, unique=True)
    
    def __str__(self):
        return str(self.name)

class Certifications(models.Model):
    institution_name= models.TextField(max_length=100, null=True, blank=True)
    certificate_name=models.TextField(max_length=100, null=True, blank=True)
    issue_date=models.TextField(max_length=100, null=True, blank=True)
    access = models.ForeignKey(CandidateResume, on_delete=models.CASCADE, null=True, blank=True)
    external_links = models.TextField(max_length=500,blank=True,null=True) # links for projects github, linkedIN, website etc

    def __str__(self):
        return str(self.certificate_name)


class SearchResume(models.Model):
    access=models.OneToOneField(CandidateResume, on_delete=models.CASCADE, blank=True,null=True,default=1)
    misc_detail=models.ForeignKey(MiscDetail, on_delete=models.CASCADE, blank=True,null=True,default=1)
    education=models.ForeignKey(CandidateEducation, on_delete=models.CASCADE, blank=True,null=True,default=1)
    work_detail=models.ForeignKey(WorkDetail, on_delete=models.CASCADE, blank=True,null=True,default=1)
    private_data=models.ForeignKey(CandidatePrivateData, on_delete=models.CASCADE, blank=True,null=True,default=1)
   
    def get_misc_detail(self):
         q=MiscDetail.objects.all()
         q.save()


class Elastic_demo(models.Model):
    name = models.TextField(max_length=230, blank=True)
    age = models.TextField(max_length=230, blank=True)
    school= models.TextField(max_length=230, blank=True)
    location= models.TextField(max_length=230, blank=True)

# class Job_Task_Suggesstions(models.Model):
#     job_title=models.CharField(max_length=200,null=True, blank=True)
#     # job_title=models.ForeignKey(Job_Title, related_name='job_titiles',on_delete=models.DO_NOTHING)
#     suggessted_tasks= models.TextField(null=True, blank=True)

class Job_Task_Suggesstion(models.Model):
    job_title=models.TextField(null=True, blank=True)
    # job_title=models.ForeignKey(Job_Title, related_name='job_titiles',on_delete=models.DO_NOTHING)
    suggessted_tasks= models.TextField(null=True, blank=True)
