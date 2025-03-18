from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Forum(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forums')
    created_at = models.DateTimeField(auto_now_add=True)
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='moderated_forums')
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('closed', 'Closed')], default='active')
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(blank=True)
    file = models.FileField(upload_to="uploads/messages/", blank=True, null=True)  # File upload
    created_at = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender.username}: {self.text[:50]}"


