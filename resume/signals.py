from django.db.models.signals import post_save,post_delete
	#I have used django user model to use post save, post delete.
# from django.contrib.auth.models import User
from django.dispatch import receiver
from . models import CandidateResume,MiscDetail,CandidateEducation,CandidatePrivateData,WorkDetail
from urlShortner.models import urlShortener

@receiver(post_delete,sender=CandidateResume)
def delete_shortcode(sender,instance,*args,**kwargs):
    # Automatically delete shortcode once related resume is deleted.
    if instance:
        try:
            # print("2")
            query=urlShortener.objects.get(access_id=instance.id)
        except:
            # print("3")
            query=None
        if query:
            # print("4")
            query.delete()

# @receiver(post_save,sender=CandidateResume)
@receiver(post_save,sender=CandidateEducation)
@receiver(post_save,sender=CandidatePrivateData)
@receiver(post_save,sender=MiscDetail)
@receiver(post_save,sender=WorkDetail)
def last_updated_resume(sender,update_fields, created,instance,*args,**kwargs):
    
    try:
        resume=CandidateResume.objects.get(id=instance.access.id)
    except:
        resume=None
    if resume:
        resume.save()




# @receiver(post_save,sender=User)
# def create_profile(sender,instance,created,**kwargs):
#     if created:
#         #write your logic here
#         print("User Profile Created")