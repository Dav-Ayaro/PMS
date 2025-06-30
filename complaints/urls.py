#### complaints/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('assign/<int:complaint_id>/', views.assign_complaint, name='assign_complaint'),
    path('resolve/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),
]
