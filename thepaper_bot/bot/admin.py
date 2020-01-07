from django.contrib import admin
from .models import MessageLog

# Register your models here.
class MessageLogAdmin(admin.ModelAdmin):
    date_hierarchy = "query_time"
    list_filter = ['query_time']
    empty_value_display = ""
    list_display = ('name', 'username', 'text', 'query_time')

admin.site.register(MessageLog, MessageLogAdmin)