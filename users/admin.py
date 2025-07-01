from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields to show in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')

    # Optional filters in the sidebar
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')

    # Fields to search by
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Ordering in admin
    ordering = ('username',)

    # Optional: Add 'role' and 'otp' to the user edit form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'otp')}),
    )

    # Optional: Include in user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'otp')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
