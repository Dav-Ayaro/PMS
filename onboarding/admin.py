from django.contrib import admin

# Register your models here.

from .models import Parent, Student

admin.site.register(Parent)
admin.site.register(Student)
