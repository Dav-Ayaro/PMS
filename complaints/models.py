from django.db import models
from users.models import CustomUser
from onboarding.models import Parent

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    resolved_at = models.DateTimeField(null=True, blank=True)