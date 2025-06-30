from django.urls import path
from . import views

urlpatterns = [
    path('parent/', views.onboard_parent, name='onboard_parent'),
]