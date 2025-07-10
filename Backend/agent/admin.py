from django.contrib import admin
from .models import Message, Request

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'sender', 'short_content', 'timestamp', 'intent', 'status', 'request']
    list_filter = ['sender', 'status', 'intent', 'timestamp']
    search_fields = ['content', 'user__username', 'intent']
    readonly_fields = ['id', 'timestamp']

    def short_content(self, obj):
        return obj.content[:50]
    short_content.short_description = 'Content'

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'intent', 'status', 'created_at', 'completed_at', 'message']
    list_filter = ['status', 'intent', 'created_at']
    search_fields = ['intent', 'user__username', 'parameters', 'result']
    readonly_fields = ['id', 'created_at', 'completed_at']
