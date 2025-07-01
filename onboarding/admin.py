from django.contrib import admin
from .models import Parent, Student

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'get_parents')
    search_fields = ('name',)
    list_filter = ('created_at',)

    def get_parents(self, obj):
        return ", ".join([parent.name for parent in obj.parents.all()])
    get_parents.short_description = 'Parents'
