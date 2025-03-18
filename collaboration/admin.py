from django.contrib import admin
from .models import Forum, Message

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('forum', 'sender', 'text', 'created_at', 'file')
    search_fields = ('text',)

