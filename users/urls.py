from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('otp/', views.verify_otp, name='verify_otp'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
