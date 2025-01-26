from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display= ['username','color','is_staff']
    search_fields  = ['username']

admin.site.register(CustomUser,CustomUserAdmin)
# Register your models here.
