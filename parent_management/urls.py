from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('onboarding/', include('onboarding.urls')),
    path('communication/', include('communication.urls')),
    path('fees/', include('fees.urls')),
    path('complaints/', include('complaints.urls')),
    path('reporting/', include('reporting.urls')),
    path('', include('users.urls')),
]