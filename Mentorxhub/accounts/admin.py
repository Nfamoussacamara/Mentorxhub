from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from mentoring.models import MentorProfile, StudentProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'bio', 'profile_picture')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'first_name', 'last_name', 'is_staff', 'is_active'),
        }),
    )

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'years_of_experience', 'hourly_rate', 'rating', 'is_available', 'total_sessions')
    list_filter = ('is_available', 'expertise', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'expertise')
    list_editable = ('is_available',)
    ordering = ('-rating', '-total_sessions')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'get_interests_display', 'total_sessions', 'created_at')
    list_filter = ('level', 'interests', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    filter_horizontal = ('interests',)  # Permet de sélectionner facilement les matières
    ordering = ('-created_at',)
    
    def get_interests_display(self, obj):
        """Affiche les matières d'intérêt sous forme de liste"""
        return ", ".join([subject.name for subject in obj.interests.all()[:3]])
    get_interests_display.short_description = "Centres d'intérêt"
