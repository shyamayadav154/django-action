from django.contrib import admin
from .models import SubscriptionDetails,PlanDetails
# Register your models here.

class SubAdmin(admin.ModelAdmin):
    list_display=['id','subscription_id','user','payment_gateway','period_end','status','updated_at']
    list_filter=['payment_gateway','status','plan_type','updated_at','created_at']

admin.site.register(SubscriptionDetails,SubAdmin)

class PlanAdmin(admin.ModelAdmin):
    list_display=['plan_id','payment_gateway','plan_type','is_active','plan_amount']
    list_filter=['payment_gateway','plan_type','is_active','plan_amount']
admin.site.register(PlanDetails,PlanAdmin)