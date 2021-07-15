from home.models import Setting
from django.contrib import admin
from home.models  import *
# Register your models here.
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['title','company', 'update_at','status']

#check message được gửi từ contact trong admin
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']




admin.site.register(Setting, SettingsAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)