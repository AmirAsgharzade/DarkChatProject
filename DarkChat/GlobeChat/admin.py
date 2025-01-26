from django.contrib import admin
from .models import GlobeHistory

class GlobeHistoryAdmin(admin.ModelAdmin):
    list_display = ['username','timestamp','color']
    search_fields = ['username','timestamp']

admin.site.register(GlobeHistory,GlobeHistoryAdmin)
# Register your models here.
