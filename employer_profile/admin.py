from django.contrib import admin
from . import models 
# Register your models here.
class EmployerDetailsAdmin(admin.ModelAdmin):
    search_fields = ['user_email','company_name', 'job_title','sub_plan']
    list_filter=['sub_plan','company_name']
admin.site.register(models.EmployerDetails)
admin.site.register(models.Employer_Template)
# admin.site.register(models.Industry)
