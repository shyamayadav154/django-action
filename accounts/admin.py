from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','email','type','is_verified']
    list_filter=['type','is_verified']
    search_fields=['email','id']

from rest_framework_simplejwt import token_blacklist

class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)

# admin.site.register(models.Nps_Survey)