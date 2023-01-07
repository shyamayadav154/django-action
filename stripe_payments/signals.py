# from django.db.models.signals import post_save, pre_delete
# from django.dispatch import receiver
# from employer_profile.models import EmployerDetails
# from drf_stripe.models import Subscription
# from .models import SubscriptionDetails
# from datetime import datetime

# @receiver(post_save, sender=Subscription)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         # print("yess")
#         # print(instance)
#         date=datetime.today().strftime("%Y-%m-%d")

#         # print(instance.stripe_user.user)
#         try:
#            queryset=SubscriptionDetails.objects.get(subscription_id=instance.subscription_id)
#         except:
#             queryset=None
#         if not queryset:
#             SubscriptionDetails.objects.create(
#                 user=instance.stripe_user.user,
#                 payment_gateway="Stripe",
#                 subscription_id= instance.subscription_id,
#                 customer_id= instance.stripe_user.customer_id,
#                 period_start=instance.period_start,
#                 period_end=instance.period_end,
#                 status=instance.status, 
#                 created_at=date          
#                     )
#         else:
#                 queryset.period_start=instance.period_start,
#                 queryset.period_end=instance.period_end,
#                 queryset.status=instance.status, 
#                 queryset.updated_at=date
#                 queryset.update()

    
