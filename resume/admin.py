from django.contrib import admin
from .models import CandidateResume, CandidatePrivateData, Current_city, Degree, Elastic_demo, Job_Title, Open_to, Resp_Title, SearchResume, Skills, Status, Sub_Skills, Timeline, WorkDetail, CandidateEducation, MiscDetail,Job_Task_Suggesstion,Certifications
# Register your models here.
class CandidateResumeAdmin(admin.ModelAdmin):
    list_display=['id','user_id','get_email','created_at','last_updated']
    list_filter=['created_at','last_updated']
    search_fields=['id',"user__email","user__id"]
    ordering = ('-created_at','last_updated','-id')                                                                                                                                                                                                            

    def get_email(self, user):
        return user.user.email

    get_email.short_description = 'User_Email'
admin.site.register(CandidateResume,CandidateResumeAdmin)
class PrivateAdmin(admin.ModelAdmin):
    list_display=['id','access_id','name',]
    search_fields=['email','id','user_id']

# @admin.register(models.CustomUser)
# class UserAdmin(admin.ModelAdmin):
#     list_display=['id','email','type']
#     list_filter=['type']
#     search_fields=['email','id']

admin.site.register(CandidatePrivateData,PrivateAdmin)
admin.site.register(WorkDetail)
admin.site.register(CandidateEducation)
admin.site.register(MiscDetail)
admin.site.register(Open_to)
admin.site.register(Status)
admin.site.register(SearchResume)
admin.site.register(Job_Title)
admin.site.register(Current_city)
admin.site.register(Skills)
admin.site.register(Sub_Skills)
admin.site.register(Degree)
admin.site.register(Resp_Title)
admin.site.register(Elastic_demo)
admin.site.register(Timeline)
# admin.site.register(Job_Title)
admin.site.register(Job_Task_Suggesstion)
admin.site.register(Certifications)