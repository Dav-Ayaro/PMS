from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class CustomUser(AbstractUser):
           
           ROLE_CHOICES = (
               ('admin', 'Admin'),
               ('teacher', 'Teacher'),
               ('receptionist', 'Receptionist'),
             ('accountant', 'Accountant'),
              ('it_support', 'IT Support'),
          )
           role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receptionist')
           otp = models.CharField(max_length=6, blank=True, null=True)

           def save(self, *args, **kwargs):
                super().save(*args, **kwargs)
                group_name = self.role
                group, _ = Group.objects.get_or_create(name=group_name)
                self.groups.add(group)