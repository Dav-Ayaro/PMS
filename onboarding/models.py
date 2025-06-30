from django.db import models
from users.models import CustomUser

class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

class Student(models.Model):
    name = models.CharField(max_length=100)
    parents = models.ManyToManyField(Parent, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)