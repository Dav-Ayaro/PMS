from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'parent_name',
        'short_description',
        'status',
        'assigned_to',
        'submitted_at',
        'resolved_at',
    )
    list_filter = ('status', 'submitted_at', 'resolved_at')
    search_fields = ('description', 'parent__name', 'assigned_to__username')
    ordering = ('-submitted_at',)

    def parent_name(self, obj):
        return obj.parent.name
    parent_name.short_description = 'Parent'

    def short_description(self, obj):
        return (obj.description[:50] + '...') if len(obj.description) > 50 else obj.description
    short_description.short_description = 'Description'
