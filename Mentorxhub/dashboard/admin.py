"""
Configuration admin pour le dashboard
"""
from django.contrib import admin
from .models import (
    UserProfile, DashboardSettings, Activity, Conversation, Message,
    Course, Lesson, CourseProgress, Payment, SupportTicket, TicketReply,
    Notification
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'country', 'city', 'total_hours', 'average_rating', 'created_at')
    list_filter = ('role', 'country', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'bio')
    readonly_fields = ('created_at', 'updated_at', 'last_active')


@admin.register(DashboardSettings)
class DashboardSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'language', 'sidebar_collapsed', 'email_notifications')
    list_filter = ('theme', 'language', 'email_notifications')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'description', 'ip_address', 'created_at')
    list_filter = ('action_type', 'created_at')
    search_fields = ('user__email', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'is_archived', 'created_at', 'updated_at')
    list_filter = ('is_archived', 'created_at')
    search_fields = ('subject', 'participants__email')
    filter_horizontal = ('participants',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'status', 'is_read', 'created_at')
    list_filter = ('status', 'is_read', 'created_at')
    search_fields = ('sender__email', 'content')
    readonly_fields = ('created_at', 'updated_at', 'read_at')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor', 'difficulty', 'price', 'is_published', 'students_count', 'average_rating')
    list_filter = ('difficulty', 'is_published', 'is_free', 'created_at')
    search_fields = ('title', 'description', 'mentor__email')
    readonly_fields = ('created_at', 'updated_at', 'students_count', 'average_rating')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'duration_minutes', 'is_free')
    list_filter = ('is_free', 'course')
    search_fields = ('title', 'description', 'course__title')
    ordering = ('course', 'order')


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'progress_percentage', 'started_at', 'completed_at')
    list_filter = ('course', 'started_at', 'completed_at')
    search_fields = ('student__email', 'course__title')
    readonly_fields = ('started_at', 'last_accessed')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_type', 'amount', 'currency', 'status', 'transaction_id', 'created_at')
    list_filter = ('payment_type', 'status', 'currency', 'created_at')
    search_fields = ('user__email', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    date_hierarchy = 'created_at'


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'category', 'priority', 'status', 'created_at')
    list_filter = ('category', 'priority', 'status', 'created_at')
    search_fields = ('subject', 'description', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'resolved_at')
    date_hierarchy = 'created_at'


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'author', 'is_internal', 'created_at')
    list_filter = ('is_internal', 'created_at')
    search_fields = ('content', 'ticket__subject', 'author__email')
    readonly_fields = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'title', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('user__email', 'title', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Marquer les notifications sélectionnées comme lues"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Marquer les notifications sélectionnées comme non lues"
