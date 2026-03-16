"""
URLs du dashboard MentorXHub
"""
from django.urls import path
from .views.dashboard import dashboard, mentor_dashboard, student_dashboard
from .views.profile import profile_view, profile_edit, profile_update, complete_profile
from .views import notifications
from .views import analytics
from .views import sessions
from .views import settings
from .views import messages
from .views import courses
from .views import payments
from .views import support

app_name = 'dashboard'

urlpatterns = [
    # Dashboard principal (redirige selon le rôle)
    path('', dashboard, name='dashboard'),
    
    # Page d'accueil du dashboard
    path('home/', dashboard, name='home'),
    
    # Module Profil
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/update/', profile_update, name='profile_update'),
    path('profile/complete/', complete_profile, name='complete_profile'),
    
    # Module Notifications
    path('notifications/', notifications.notifications_list, name='notifications'),
    path('notifications/<int:notification_id>/read/', notifications.notification_mark_read, name='notification_mark_read'),
    path('notifications/mark-all-read/', notifications.notifications_mark_all_read, name='notifications_mark_all_read'),
    path('notifications/count/', notifications.notifications_count, name='notifications_count'),
    
    # Module Analytics
    path('analytics/', analytics.analytics_view, name='analytics'),
    path('analytics/data/', analytics.analytics_data, name='analytics_data'),
    path('analytics/kpis/', analytics.kpis_data, name='kpis_data'),
    
    # Module Sessions
    path('sessions/calendar/', sessions.sessions_calendar, name='sessions_calendar'),
    path('sessions/events/', sessions.sessions_events, name='sessions_events'),
    path('sessions/<int:session_id>/', sessions.session_detail, name='session_detail'),
    path('sessions/<int:session_id>/update-date/', sessions.session_update_date, name='session_update_date'),
    path('sessions/<int:session_id>/video/', sessions.session_video_room, name='session_video_room'),
    
    # Module Paramètres
    path('settings/', settings.settings_view, name='settings'),
    path('settings/general/', settings.settings_general, name='settings_general'),
    path('settings/security/', settings.settings_security, name='settings_security'),
    path('settings/notifications/', settings.settings_notifications, name='settings_notifications'),
    path('settings/theme/', settings.settings_theme, name='settings_theme'),
    
    # Module Messagerie
    path('messages/', messages.messages_list, name='messages_list'),
    path('messages/<uuid:conversation_id>/', messages.conversation_detail, name='conversation_detail'),
    path('messages/create/', messages.conversation_create, name='conversation_create'),
    path('messages/<uuid:conversation_id>/send/', messages.message_send, name='message_send'),
    path('messages/unread-count/', messages.messages_unread_count, name='messages_unread_count'),
    path('messages/poll/', messages.messages_poll, name='messages_poll'),
    
    # Module Cours
    path('courses/', courses.courses_list, name='courses_list'),
    path('courses/create/', courses.course_create, name='course_create'),
    path('courses/<uuid:course_id>/', courses.course_detail, name='course_detail'),
    path('courses/<uuid:course_id>/edit/', courses.course_edit, name='course_edit'),
    path('courses/<uuid:course_id>/lessons/create/', courses.lesson_create, name='lesson_create'),
    path('courses/<uuid:course_id>/lessons/<uuid:lesson_id>/', courses.lesson_detail, name='lesson_detail'),
    path('courses/<uuid:course_id>/lessons/<uuid:lesson_id>/complete/', courses.lesson_complete, name='lesson_complete'),
    
    # Module Paiements
    path('payments/', payments.payments_list, name='payments_list'),
    path('payments/create/', payments.payment_create, name='payment_create'),
    path('payments/<uuid:payment_id>/', payments.payment_detail, name='payment_detail'),
    path('payments/<uuid:payment_id>/invoice/', payments.payment_invoice, name='payment_invoice'),
    path('payments/stats/', payments.payments_stats, name='payments_stats'),
    
    # Module Support
    path('support/', support.support_tickets_list, name='support_tickets_list'),
    path('support/create/', support.support_ticket_create, name='support_ticket_create'),
    path('support/tickets/<uuid:ticket_id>/', support.support_ticket_detail, name='support_ticket_detail'),
    path('support/tickets/<uuid:ticket_id>/reply/', support.support_ticket_reply, name='support_ticket_reply'),
    path('support/tickets/<uuid:ticket_id>/close/', support.support_ticket_close, name='support_ticket_close'),
    path('support/faq/', support.support_faq, name='support_faq'),
]
