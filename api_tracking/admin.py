from django.contrib import admin
from .models import Tracking

# Register your models here.
class TrackingAdmin(admin.ModelAdmin):
    list_display=['id','user_id','access_id','view','counter','date']
    list_filter=['date']
    search_fields=['user_id','access_id']
admin.site.register(Tracking,TrackingAdmin)