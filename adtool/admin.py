from django.contrib import admin
from .models import Advertisement, AdvertisementLog, Website
# Register your models here.

admin.site.register(Advertisement)
admin.site.register(AdvertisementLog)
admin.site.register(Website)
