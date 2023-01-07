from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from . import managers
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
class CustomUser(AbstractUser):
    """
    A User model that uses `email` as it's default identifier instead of
    username.
    """
    class Types(models.TextChoices):
        CANDIDATE = "CANDIDATE", "Candidate"
        EMPLOYER = "EMPLOYER", "Employer"

    base_type = Types.CANDIDATE
    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    username = models.CharField(max_length=50,null=True,blank=True,default=None)
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField()
    gender = models.CharField(
        max_length=140,
        null=True,
        choices=(
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        )
    )
    birth_date = models.DateField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_verified=models.BooleanField(default=False)
    nps =  models.IntegerField(blank=True,null=True)
    pmf =  models.CharField(max_length=140,
        null=True,
        # choices=(
        #     ('M', 'M'),
        #     ('F', 'F'),
        #     ('O', 'O')
        # ),
        blank=True
    )
    Lastlogin1= models.DateTimeField(null=True,blank=True)
    feedback  = models.TextField(max_length=250,blank=True)
    # is_pro=models.BooleanField(default=False)
    # email_verification_token=models.CharField(max_length=200,null=True,blank=True)
    # is_pro=models.ForeignKey(Pro_User, on_delete=models.CASCADE, null=True, blank=True)
    # print(type)
    # if type== Types.EMPLOYER:
    # company_name=models.CharField(max_length=50,null=True,blank=True)
    subscription_id=models.CharField(max_length=60,blank=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.CustomUserManager()

    def __str__(self):
        return self.email
    @classmethod
    def _check_model(cls):
        errors = []
        return errors
class CandidateManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.CANDIDATE)


class EmployerManager(models.Manager):
    
    # company_name=models.CharField(max_length=50,null=True,blank=True)
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.EMPLOYER)


class Candidate(CustomUser):
    base_type = CustomUser.Types.CANDIDATE
    objects = CandidateManager()

    class Meta:
        proxy = True

# class Employer(CustomUser):
#     base_type = CustomUser.Types.EMPLOYER
#     # company_name=models.CharField(max_length=50,null=True,blank=True)
#     objects = EmployerManager()

#     class Meta:
#         proxy = True
class Employer(CustomUser):
    base_type = CustomUser.Types.EMPLOYER
    objects = EmployerManager()

    @property
    def details(self):
        return self.employerdetails

    class Meta:
        proxy = True

# class Nps_Survey(models.Model):
    
#     user=  models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=None,null=True,unique=True)
#     Nps =  models.IntegerField(blank=True,null=True)
#     Pmf =  models.CharField(max_length=140,
#         null=True,
#         # choices=(
#         #     ('M', 'M'),
#         #     ('F', 'F'),
#         #     ('O', 'O')
#         # ),
#         blank=True
#     )
#     Last_login= models.DateTimeField(null=True,blank=True)
#     Feedback  = models.TextField(max_length=250,blank=True)





    # def __str__(self):
    #     return self.user
# class EmployerDetails(models.Model):
# 	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
# 	company_name = models.CharField(max_length=60)


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

#     email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "anirbanchakraborty967@gmail.com",
#         # to:
#         [reset_password_token.user.email]
#     )
         