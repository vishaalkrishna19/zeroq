from django.db import models
from django.conf import settings

class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_requests')
    intent = models.CharField(max_length=255)
    parameters = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    result = models.JSONField(blank=True, null=True)
    # message FK added after Message model

    def __str__(self):
        return f"{self.user} - {self.intent} ({self.status})"

class Message(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('agent', 'Agent'),
    ]
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('error', 'Error'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, blank=True, null=True, related_name='messages')
    intent = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.sender.title()} ({self.user}): {self.content[:40]}"
    
# Add message_id to Request (optional, can be blank)
Request.add_to_class('message', models.ForeignKey(
    Message, on_delete=models.SET_NULL, blank=True, null=True, related_name='originating_requests'
))
