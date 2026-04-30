from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'is_student',
                    'institution_name', 'student_id', 'is_verified']
    list_filter = ['is_student', 'is_verified']
    search_fields = ['user__username', 'user__email',
                     'institution_name', 'student_id']
    list_editable = ['is_verified']

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone')
        }),
        ('Student Information', {
            'fields': ('is_student', 'institution_name', 'student_id', 'is_verified'),
            'classes': ('collapse',)
        }),
    )
