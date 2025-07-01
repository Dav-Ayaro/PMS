from django.db import models
from users.models import CustomUser
from onboarding.models import Parent

class Message(models.Model):
    TYPE_CHOICES = (
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('chat', 'In-App Chat'),
    )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Parent, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:50]