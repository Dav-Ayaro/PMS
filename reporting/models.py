from django.db import models

class Report(models.Model):
    TYPE_CHOICES = (
        ('engagement', 'Engagement'),
        ('payment', 'Payment'),
        ('academic', 'Academic'),
        ('complaint', 'Complaint'),
    )
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    generated_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()