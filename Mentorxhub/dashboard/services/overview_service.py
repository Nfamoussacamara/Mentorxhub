"""
Service de statistiques et données pour le Dashboard
Extrait toute la logique métier des vues pour la rendre réutilisable et testable
"""
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from mentoring.models import MentorProfile, StudentProfile, MentoringSession
from dashboard.models import Notification, Message, Activity, Course, CourseProgress
import json


def get_mentor_stats(mentor_profile, user):
    """
    Calcule toutes les statistiques pour un mentor
    
    Args:
        mentor_profile: Instance de MentorProfile
        user: Instance de CustomUser
    
    Returns:
        dict: Dictionnaire contenant stats, charts, leaderboard, et autres données
    """
    today = timezone.now().date()
    current_month_start = today.replace(day=1)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = current_month_start - timedelta(days=1)
    
    # Sessions à venir (ordonnées par date) - Optimisé avec select_related
    upcoming_sessions = MentoringSession.objects.filter(
        mentor=mentor_profile,
        date__gte=today,
        status__in=['pending', 'scheduled', 'in_progress']
    ).select_related('student', 'student__user', 'mentor', 'mentor__user').order_by('date', 'start_time')[:5]
    
    # 1. Sessions créées ce mois vs mois dernier
    sessions_created_this_month = MentoringSession.objects.filter(
        mentor=mentor_profile,
        created_at__date__gte=current_month_start
    ).count()
    
    sessions_created_last_month = MentoringSession.objects.filter(
        mentor=mentor_profile,
        created_at__date__gte=last_month_start,
        created_at__date__lte=last_month_end
    ).count()
    
    sessions_created_change = 0
    if sessions_created_last_month > 0:
        sessions_created_change = ((sessions_created_this_month - sessions_created_last_month) / sessions_created_last_month) * 100
    
    # 2. Sessions ouvertes (scheduled + in_progress)
    sessions_open = MentoringSession.objects.filter(
        mentor=mentor_profile,
        status__in=['pending', 'scheduled', 'in_progress'],
        date__gte=today
    ).count()
    
    sessions_open_last_month = MentoringSession.objects.filter(
        mentor=mentor_profile,
        status__in=['pending', 'scheduled', 'in_progress'],
        date__gte=last_month_start,
        date__lte=last_month_end
    ).count()
    
    sessions_open_change = 0
    if sessions_open_last_month > 0:
        sessions_open_change = ((sessions_open - sessions_open_last_month) / sessions_open_last_month) * 100
    
    # 3. Revenus actifs (sessions complétées ce mois)
    completed_sessions_this_month = MentoringSession.objects.filter(
        mentor=mentor_profile,
        date__gte=current_month_start,
        date__lte=today,
        status='completed'
    )
    
    active_earnings = 0
    for session in completed_sessions_this_month:
        hours = session.duration() / 60
        active_earnings += hours * float(mentor_profile.hourly_rate)
    
    completed_sessions_last_month = MentoringSession.objects.filter(
        mentor=mentor_profile,
        date__gte=last_month_start,
        date__lte=last_month_end,
        status='completed'
    )
    
    last_month_earnings = 0
    for session in completed_sessions_last_month:
        hours = session.duration() / 60
        last_month_earnings += hours * float(mentor_profile.hourly_rate)
    
    active_earnings_change = 0
    if last_month_earnings > 0:
        active_earnings_change = ((active_earnings - last_month_earnings) / last_month_earnings) * 100
    
    # 4. Étudiants actifs (étudiants avec sessions ce mois)
    active_students = MentoringSession.objects.filter(
        mentor=mentor_profile,
        date__gte=current_month_start,
        date__lte=today
    ).values('student').distinct().count()
    
    active_students_last_month = MentoringSession.objects.filter(
        mentor=mentor_profile,
        date__gte=last_month_start,
        date__lte=last_month_end
    ).values('student').distinct().count()
    
    active_students_change = 0
    if active_students_last_month > 0:
        active_students_change = ((active_students - active_students_last_month) / active_students_last_month) * 100
    
    # Données pour les graphiques
    # Graphique 1: Revenus par mois (6 derniers mois)
    chart_revenue_data = []
    chart_revenue_labels = []
    for i in range(5, -1, -1):
        month_date = (current_month_start - timedelta(days=30*i)).replace(day=1)
        month_end = (month_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_sessions = MentoringSession.objects.filter(
            mentor=mentor_profile,
            date__gte=month_date,
            date__lte=month_end,
            status='completed'
        )
        
        month_revenue = 0
        for session in month_sessions:
            hours = session.duration() / 60
            month_revenue += hours * float(mentor_profile.hourly_rate)
        
        chart_revenue_data.append(float(month_revenue))
        chart_revenue_labels.append(month_date.strftime('%b'))
    
    # Graphique 2: Sessions par statut
    chart_sessions_data = {
        'scheduled': MentoringSession.objects.filter(mentor=mentor_profile, status='scheduled').count(),
        'in_progress': MentoringSession.objects.filter(mentor=mentor_profile, status='in_progress').count(),
        'completed': MentoringSession.objects.filter(mentor=mentor_profile, status='completed').count(),
        'cancelled': MentoringSession.objects.filter(mentor=mentor_profile, status='cancelled').count(),
    }
    
    # Calculer le total des sessions pour le template
    chart_sessions_total = sum(chart_sessions_data.values())
    
    # Leaderboard: Top mentors (par nombre de sessions complétées)
    top_mentors = MentorProfile.objects.annotate(
        completed_count=Count('mentoring_sessions', filter=Q(mentoring_sessions__status='completed'))
    ).order_by('-completed_count', '-rating')[:5]
    
    leaderboard_data = []
    for idx, mentor in enumerate(top_mentors, 1):
        total_sessions = mentor.mentoring_sessions.count()
        completed_sessions = mentor.mentoring_sessions.filter(status='completed').count()
        # Calculer la valeur totale (revenus estimés)
        total_value = completed_sessions * float(mentor.hourly_rate) if mentor.hourly_rate else 0
        
        leaderboard_data.append({
            'rank': idx,
            'mentor': mentor,
            'user': mentor.user,
            'total_sessions': total_sessions,
            'completed_sessions': completed_sessions,
            'total_value': total_value,
        })
    
    stats = {
        'sessions_created': sessions_created_this_month,
        'sessions_created_change': round(sessions_created_change, 1),
        'sessions_created_change_abs': round(abs(sessions_created_change), 1),
        'sessions_created_last_month': sessions_created_last_month,
        'sessions_open': sessions_open,
        'sessions_open_change': round(sessions_open_change, 1),
        'sessions_open_change_abs': round(abs(sessions_open_change), 1),
        'sessions_open_last_month': sessions_open_last_month,
        'active_earnings': round(active_earnings, 2),
        'active_earnings_change': round(active_earnings_change, 1),
        'active_earnings_change_abs': round(abs(active_earnings_change), 1),
        'active_earnings_last_month': round(last_month_earnings, 2),
        'active_students': active_students,
        'active_students_change': round(active_students_change, 1),
        'active_students_change_abs': round(abs(active_students_change), 1),
        'active_students_last_month': active_students_last_month,
        'avg_rating': float(mentor_profile.rating),
    }
    
    # Déterminer le moment de la journée pour le message de bienvenue
    current_hour = timezone.now().hour
    if 5 <= current_hour < 12:
        greeting_time = 'morning'
    elif 12 <= current_hour < 18:
        greeting_time = 'afternoon'
    elif 18 <= current_hour < 22:
        greeting_time = 'evening'
    else:
        greeting_time = 'night'
    
    # Nouvelles données de la base de données
    # 1. Notifications récentes
    recent_notifications = Notification.objects.filter(user=user).order_by('-created_at')[:3]
    
    # 2. Nombre de messages non lus
    unread_messages_count = Message.objects.filter(
        conversation__participants=user
    ).exclude(sender=user).filter(is_read=False).count()
    
    # 3. Cours créés récemment
    recent_courses = Course.objects.filter(mentor=user).order_by('-created_at')[:3]
    
    # 4. Activités récentes
    recent_activities = Activity.objects.filter(user=user).order_by('-created_at')[:5]
    
    return {
        'stats': stats,
        'upcoming_sessions': upcoming_sessions,
        'user_role': 'mentor',
        'chart_revenue_data': chart_revenue_data,
        'chart_revenue_data_json': json.dumps(chart_revenue_data),
        'chart_revenue_labels': chart_revenue_labels,
        'chart_revenue_labels_json': json.dumps(chart_revenue_labels),
        'chart_sessions_data': chart_sessions_data,
        'chart_sessions_total': chart_sessions_total,
        'leaderboard': leaderboard_data,
        'total_revenue': round(sum(chart_revenue_data), 2),
        'greeting_time': greeting_time,
        'recent_notifications': recent_notifications,
        'unread_messages_count': unread_messages_count,
        'recent_courses': recent_courses,
        'recent_activities': recent_activities,
    }


def get_student_stats(student_profile, user):
    """
    Calcule toutes les statistiques pour un étudiant
    
    Args:
        student_profile: Instance de StudentProfile
        user: Instance de CustomUser
    
    Returns:
        dict: Dictionnaire contenant stats, charts, leaderboard, et autres données
    """
    today = timezone.now().date()
    current_month_start = today.replace(day=1)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = current_month_start - timedelta(days=1)
    
    # Sessions à venir - Optimisé avec select_related
    upcoming_sessions = MentoringSession.objects.filter(
        student=student_profile,
        date__gte=today,
        status__in=['pending', 'scheduled', 'in_progress']
    ).select_related('mentor', 'mentor__user', 'student', 'student__user').order_by('date', 'start_time')[:5]
    
    # 1. Sessions créées ce mois vs mois dernier
    sessions_created_this_month = MentoringSession.objects.filter(
        student=student_profile,
        created_at__date__gte=current_month_start
    ).count()
    
    sessions_created_last_month = MentoringSession.objects.filter(
        student=student_profile,
        created_at__date__gte=last_month_start,
        created_at__date__lte=last_month_end
    ).count()
    
    sessions_created_change = 0
    if sessions_created_last_month > 0:
        sessions_created_change = ((sessions_created_this_month - sessions_created_last_month) / sessions_created_last_month) * 100
    
    # 2. Sessions ouvertes (scheduled + in_progress)
    sessions_open = MentoringSession.objects.filter(
        student=student_profile,
        status__in=['pending', 'scheduled', 'in_progress'],
        date__gte=today
    ).count()
    
    sessions_open_last_month = MentoringSession.objects.filter(
        student=student_profile,
        status__in=['pending', 'scheduled', 'in_progress'],
        date__gte=last_month_start,
        date__lte=last_month_end
    ).count()
    
    sessions_open_change = 0
    if sessions_open_last_month > 0:
        sessions_open_change = ((sessions_open - sessions_open_last_month) / sessions_open_last_month) * 100
    
    # 3. Total heures de mentorat
    completed_sessions = MentoringSession.objects.filter(
        student=student_profile,
        status='completed'
    )
    
    total_hours = 0
    for session in completed_sessions:
        total_hours += session.duration() / 60  # Convertir minutes en heures
    
    # Heures du mois dernier
    completed_sessions_last_month = MentoringSession.objects.filter(
        student=student_profile,
        status='completed',
        date__gte=last_month_start,
        date__lte=last_month_end
    )
    
    total_hours_last_month = 0
    for session in completed_sessions_last_month:
        total_hours_last_month += session.duration() / 60
    
    total_hours_change = 0
    if total_hours_last_month > 0:
        total_hours_change = ((total_hours - total_hours_last_month) / total_hours_last_month) * 100
    
    # 4. Mentors actifs
    active_mentors = MentoringSession.objects.filter(
        student=student_profile,
        status__in=['pending', 'completed', 'scheduled']
    ).values('mentor').distinct().count()
    
    active_mentors_last_month = MentoringSession.objects.filter(
        student=student_profile,
        status__in=['completed', 'scheduled'],
        date__gte=last_month_start,
        date__lte=last_month_end
    ).values('mentor').distinct().count()
    
    active_mentors_change = 0
    if active_mentors_last_month > 0:
        active_mentors_change = ((active_mentors - active_mentors_last_month) / active_mentors_last_month) * 100
    
    # Données pour les graphiques
    # Graphique 1: Heures par mois (6 derniers mois)
    chart_hours_data = []
    chart_hours_labels = []
    for i in range(5, -1, -1):
        month_date = (current_month_start - timedelta(days=30*i)).replace(day=1)
        month_end = (month_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_sessions = MentoringSession.objects.filter(
            student=student_profile,
            date__gte=month_date,
            date__lte=month_end,
            status='completed'
        )
        
        month_hours = 0
        for session in month_sessions:
            month_hours += session.duration() / 60
        
        chart_hours_data.append(float(month_hours))
        chart_hours_labels.append(month_date.strftime('%b'))
    
    # Graphique 2: Sessions par statut
    chart_sessions_data = {
        'pending': MentoringSession.objects.filter(student=student_profile, status='pending').count(),
        'scheduled': MentoringSession.objects.filter(student=student_profile, status='scheduled').count(),
        'in_progress': MentoringSession.objects.filter(student=student_profile, status='in_progress').count(),
        'completed': MentoringSession.objects.filter(student=student_profile, status='completed').count(),
        'cancelled': MentoringSession.objects.filter(student=student_profile, status='cancelled').count(),
    }
    
    # Calculer le total des sessions pour le template
    chart_sessions_total = sum(chart_sessions_data.values())
    
    # Leaderboard: Top mentors (par nombre de sessions complétées avec cet étudiant)
    # Récupérer les mentors avec lesquels l'étudiant a eu des sessions
    mentors_with_sessions = MentorProfile.objects.filter(
        mentoring_sessions__student=student_profile
    ).annotate(
        completed_count=Count('mentoring_sessions', filter=Q(mentoring_sessions__student=student_profile, mentoring_sessions__status='completed'))
    ).order_by('-completed_count')[:5]
    
    leaderboard_data = []
    for idx, mentor in enumerate(mentors_with_sessions, 1):
        # Sessions avec cet étudiant spécifiquement
        sessions_with_student = mentor.mentoring_sessions.filter(student=student_profile)
        total_sessions = sessions_with_student.count()
        completed_sessions = sessions_with_student.filter(status='completed').count()
        
        # Calculer les heures totales avec cet étudiant
        completed_sessions_list = sessions_with_student.filter(status='completed')
        total_hours_mentor = 0
        for session in completed_sessions_list:
            total_hours_mentor += session.duration() / 60
        
        leaderboard_data.append({
            'rank': idx,
            'mentor': mentor,
            'user': mentor.user,
            'total_sessions': total_sessions,
            'completed_sessions': completed_sessions,
            'total_hours': round(total_hours_mentor, 1),
        })
    
    # Si le leaderboard est vide, suggérer des mentors approuvés
    if not leaderboard_data:
        suggested_mentors = MentorProfile.objects.filter(status='approved').exclude(user=user)[:5]
        for idx, mentor in enumerate(suggested_mentors, 1):
            leaderboard_data.append({
                'rank': idx,
                'mentor': mentor,
                'user': mentor.user,
                'total_sessions': mentor.mentoring_sessions.count(),
                'completed_sessions': mentor.mentoring_sessions.filter(status='completed').count(),
                'total_hours': 0, # Pour l'étudiant actuel
                'is_recommendation': True
            })
    
    stats = {
        'sessions_created': sessions_created_this_month,
        'sessions_created_change': round(sessions_created_change, 1),
        'sessions_created_change_abs': round(abs(sessions_created_change), 1),
        'sessions_created_last_month': sessions_created_last_month,
        'sessions_open': sessions_open,
        'sessions_open_change': round(sessions_open_change, 1),
        'sessions_open_change_abs': round(abs(sessions_open_change), 1),
        'sessions_open_last_month': sessions_open_last_month,
        'total_hours': round(total_hours, 1),
        'total_hours_change': round(total_hours_change, 1),
        'total_hours_change_abs': round(abs(total_hours_change), 1),
        'total_hours_last_month': round(total_hours_last_month, 1),
        'active_mentors': active_mentors,
        'active_mentors_change': round(active_mentors_change, 1),
        'active_mentors_change_abs': round(abs(active_mentors_change), 1),
        'active_mentors_last_month': active_mentors_last_month,
    }
    
    # Déterminer le moment de la journée pour le message de bienvenue
    current_hour = timezone.now().hour
    if 5 <= current_hour < 12:
        greeting_time = 'morning'
    elif 12 <= current_hour < 18:
        greeting_time = 'afternoon'
    elif 18 <= current_hour < 22:
        greeting_time = 'evening'
    else:
        greeting_time = 'night'
    
    # Nouvelles données de la base de données
    # 1. Notifications récentes
    recent_notifications = Notification.objects.filter(user=user).order_by('-created_at')[:3]
    
    # 2. Nombre de messages non lus
    unread_messages_count = Message.objects.filter(
        conversation__participants=user
    ).exclude(sender=user).filter(is_read=False).count()
    
    # 3. Progrès des cours
    enrolled_courses = CourseProgress.objects.filter(
        student=user
    ).select_related('course').order_by('-last_accessed')[:3]
    
    # 4. Activités récentes
    recent_activities = Activity.objects.filter(user=user).order_by('-created_at')[:5]
    
    return {
        'stats': stats,
        'upcoming_sessions': upcoming_sessions,
        'user_role': 'student',
        'chart_hours_data': chart_hours_data,
        'chart_hours_data_json': json.dumps(chart_hours_data),
        'chart_hours_labels': chart_hours_labels,
        'chart_hours_labels_json': json.dumps(chart_hours_labels),
        'chart_sessions_data': chart_sessions_data,
        'chart_sessions_total': chart_sessions_total,
        'leaderboard': leaderboard_data,
        'total_hours_chart': round(sum(chart_hours_data), 1),
        'greeting_time': greeting_time,
        'recent_notifications': recent_notifications,
        'unread_messages_count': unread_messages_count,
        'enrolled_courses': enrolled_courses,
        'recent_activities': recent_activities,
    }
