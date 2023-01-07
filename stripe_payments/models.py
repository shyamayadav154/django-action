from django.db import models
from accounts.models import CustomUser
from datetime import datetime
# Create your models here.

class SubscriptionDetails(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    email=models.EmailField(blank=True,null=True)
    payment_method=models.CharField(max_length=60,null=True,blank=True)
    card_id=models.CharField(max_length=60,null=True,blank=True)
    card_type=models.CharField(max_length=60,null=True,blank=True)
    card_network=models.CharField(max_length=60,null=True,blank=True)
    card_expiry_month=models.CharField(max_length=60,null=True,blank=True)
    card_expiry_year=models.CharField(max_length=60,null=True,blank=True)
    card_last_4=models.CharField(max_length=60,null=True,blank=True)
    card_name=models.CharField(max_length=60,null=True,blank=True)
    invoice_id=models.CharField(max_length=60,null=True,blank=True)
    invoice_pdf=models.CharField(max_length=200,null=True,blank=True)
    payment_gateway= models.CharField(max_length=60,null=True,blank=True)
    subscription_id = models.CharField(max_length=60,null=True,blank=True)
    customer_id = models.CharField(max_length=60,null=True,blank=True)
    plan_id=models.CharField(max_length=60,null=True,blank=True)
    period_start = models.DateTimeField(null=True, blank=True)
    period_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=64,null=True,blank=True)
    billing_frequency=models.CharField(max_length=60,null=True,blank=True)
    plan_type=models.CharField(max_length=60,null=True,blank=True)
    plan_name=models.CharField(max_length=80,null=True,blank=True)
    amount=models.CharField(max_length=60,null=True,blank=True)
    payment_status= models.CharField(max_length=60,null=True,blank=True)
    billing_reason=models.CharField(max_length=60,null=True,blank=True)
    cancel_at_period_end=models.BooleanField(default=False,null=True,blank=True)
    cancel_at=models.DateField(null=True,blank=True)
    created_at = models.DateField(null=True,blank=True)
    updated_at = models.DateField(null=True,blank=True)
   
    class Meta:
        verbose_name="Subscription"
        verbose_name_plural="Subscriptions"

class PlanDetails(models.Model):
    plan_id=models.CharField(max_length=60,null=True,blank=True)
    payment_gateway= models.CharField(max_length=60)
    plan_type=models.CharField(max_length=60,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    plan_created=models.DateTimeField(blank=True,null=True)
    plan_amount=models.CharField(max_length=60)
    billing_frequency=models.CharField(max_length=60,null=True,blank=True)
    currency=models.CharField(max_length=60,null=True,blank=True)

