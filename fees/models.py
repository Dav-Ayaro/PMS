from django.db import models
from onboarding.models import Parent

class Invoice(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    receipt = models.CharField(max_length=100, unique=True)