from django.contrib import admin
from .models import Availability, MentoringSession, Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_editable = ('is_active',)

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'get_day_of_week_display', 'start_time', 'end_time', 'is_recurring')
    list_filter = ('day_of_week', 'is_recurring', 'created_at')
    search_fields = ('mentor__user__email', 'mentor__user__first_name', 'mentor__user__last_name')
    ordering = ('day_of_week', 'start_time')

@admin.register(MentoringSession)
class MentoringSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor', 'student', 'date', 'start_time', 'end_time', 'status', 'rating')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('title', 'mentor__user__email', 'student__user__email', 'description')
    list_editable = ('status',)
    ordering = ('-date', '-start_time')
    
    fieldsets = (
        ('Informations de la session', {
            'fields': ('title', 'description', 'mentor', 'student')
        }),
        ('Planning', {
            'fields': ('date', 'start_time', 'end_time', 'status', 'meeting_link')
        }),
        ('Feedback', {
            'fields': ('notes', 'rating', 'feedback')
        }),
    )
