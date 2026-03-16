"""
Vues pour les analytics et statistiques
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from mentoring.models import MentorProfile, StudentProfile, MentoringSession


@login_required
def analytics_view(request):
    """Vue principale des analytics"""
    user = request.user
    
    context = {
        'user_role': user.role,
    }
    
    # Ajouter les sessions à venir pour les étudiants
    if user.role == 'student':
        try:
            student_profile = user.student_profile
            today = timezone.now().date()
            upcoming_sessions = MentoringSession.objects.filter(
                student=student_profile,
                date__gte=today,
                status__in=['pending', 'scheduled', 'in_progress']
            ).select_related('mentor', 'mentor__user').order_by('date', 'start_time')[:5]
            context['upcoming_sessions'] = upcoming_sessions
        except StudentProfile.DoesNotExist:
            context['upcoming_sessions'] = []
    
    # Détecter si c'est une requête HTMX ou AJAX
    if request.headers.get('HX-Request') == 'true' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Retourner uniquement le fragment pour éviter la duplication
        return render(request, 'dashboard/fragments/analytics.html', context)
    
    return render(request, 'dashboard/analytics/view.html', context)


@login_required
def analytics_data(request):
    """API endpoint pour les données des graphiques"""
    user = request.user
    period = request.GET.get('period', 'week')  # week, month, year
    
    # Calculer les dates selon la période
    now = timezone.now()
    if period == 'week':
        start_date = now - timedelta(days=7)
    elif period == 'month':
        start_date = now - timedelta(days=30)
    elif period == 'year':
        start_date = now - timedelta(days=365)
    else:
        start_date = now - timedelta(days=7)
    
    data = {}
    
    if user.role == 'mentor':
        try:
            mentor_profile = user.mentor_profile
            sessions = MentoringSession.objects.filter(
                mentor=mentor_profile,
                created_at__gte=start_date
            )
            
            # Données pour graphique linéaire (sessions par jour)
            sessions_by_day = {}
            for i in range(7 if period == 'week' else 30 if period == 'month' else 12):
                date = start_date + timedelta(days=i if period != 'year' else i*30)
                date_key = date.strftime('%Y-%m-%d')
                count = sessions.filter(
                    date=date.date() if period != 'year' else None,
                    created_at__date=date.date()
                ).count()
                sessions_by_day[date_key] = count
            
            # Données pour graphique en donut (statuts)
            status_data = {
                'scheduled': sessions.filter(status='scheduled').count(),
                'completed': sessions.filter(status='completed').count(),
                'cancelled': sessions.filter(status='cancelled').count(),
            }
            
            # Données pour graphique en barres (revenus par mois)
            earnings_by_month = {}
            completed_sessions = sessions.filter(status='completed')
            for session in completed_sessions:
                month_key = session.date.strftime('%Y-%m')
                if month_key not in earnings_by_month:
                    earnings_by_month[month_key] = 0
                # Calculer les revenus (durée * taux horaire)
                duration_hours = session.duration() / 60
                earnings = float(duration_hours) * float(mentor_profile.hourly_rate)
                earnings_by_month[month_key] += earnings
            
            data = {
                'sessions_by_day': sessions_by_day,
                'status_data': status_data,
                'earnings_by_month': earnings_by_month,
            }
            
        except MentorProfile.DoesNotExist:
            pass
    
    elif user.role == 'student':
        try:
            student_profile = user.student_profile
            sessions = MentoringSession.objects.filter(
                student=student_profile,
                created_at__gte=start_date
            )
            
            # Données pour graphique linéaire (sessions par jour)
            sessions_by_day = {}
            for i in range(7 if period == 'week' else 30 if period == 'month' else 12):
                date = start_date + timedelta(days=i if period != 'year' else i*30)
                date_key = date.strftime('%Y-%m-%d')
                count = sessions.filter(
                    date=date.date() if period != 'year' else None,
                    created_at__date=date.date()
                ).count()
                sessions_by_day[date_key] = count
            
            # Données pour graphique en donut (statuts)
            status_data = {
                'scheduled': sessions.filter(status='scheduled').count(),
                'completed': sessions.filter(status='completed').count(),
                'cancelled': sessions.filter(status='cancelled').count(),
            }
            
            # Données pour graphique en barres (heures par mois)
            hours_by_month = {}
            completed_sessions = sessions.filter(status='completed')
            for session in completed_sessions:
                month_key = session.date.strftime('%Y-%m')
                if month_key not in hours_by_month:
                    hours_by_month[month_key] = 0
                hours_by_month[month_key] += session.duration() / 60
            
            data = {
                'sessions_by_day': sessions_by_day,
                'status_data': status_data,
                'hours_by_month': hours_by_month,
            }
            
        except StudentProfile.DoesNotExist:
            pass
    
    return JsonResponse(data)


@login_required
def kpis_data(request):
    """API endpoint pour les KPIs"""
    user = request.user
    period = request.GET.get('period', 'week')
    
    now = timezone.now()
    if period == 'week':
        start_date = now - timedelta(days=7)
    elif period == 'month':
        start_date = now - timedelta(days=30)
    elif period == 'year':
        start_date = now - timedelta(days=365)
    else:
        start_date = now - timedelta(days=7)
    
    kpis = {}
    
    if user.role == 'mentor':
        try:
            mentor_profile = user.mentor_profile
            sessions = MentoringSession.objects.filter(
                mentor=mentor_profile,
                created_at__gte=start_date
            )
            
            previous_start = start_date - (now - start_date)
            previous_sessions = MentoringSession.objects.filter(
                mentor=mentor_profile,
                created_at__gte=previous_start,
                created_at__lt=start_date
            )
            
            total_sessions = sessions.count()
            previous_total = previous_sessions.count()
            sessions_change = ((total_sessions - previous_total) / previous_total * 100) if previous_total > 0 else 0
            
            completed = sessions.filter(status='completed').count()
            previous_completed = previous_sessions.filter(status='completed').count()
            completed_change = ((completed - previous_completed) / previous_completed * 100) if previous_completed > 0 else 0
            
            avg_rating = sessions.filter(rating__isnull=False).aggregate(Avg('rating'))['rating__avg'] or 0.0
            previous_avg = previous_sessions.filter(rating__isnull=False).aggregate(Avg('rating'))['rating__avg'] or 0.0
            rating_change = avg_rating - previous_avg if previous_avg > 0 else 0
            
            total_earnings = sum(
                (s.duration() / 60) * float(mentor_profile.hourly_rate)
                for s in sessions.filter(status='completed')
            )
            previous_earnings = sum(
                (s.duration() / 60) * float(mentor_profile.hourly_rate)
                for s in previous_sessions.filter(status='completed')
            )
            earnings_change = ((total_earnings - previous_earnings) / previous_earnings * 100) if previous_earnings > 0 else 0
            
            kpis = {
                'total_sessions': {
                    'value': total_sessions,
                    'change': round(sessions_change, 1),
                    'label': 'Sessions totales'
                },
                'completed_sessions': {
                    'value': completed,
                    'change': round(completed_change, 1),
                    'label': 'Sessions terminées'
                },
                'avg_rating': {
                    'value': round(avg_rating, 1),
                    'change': round(rating_change, 1),
                    'label': 'Note moyenne'
                },
                'total_earnings': {
                    'value': round(total_earnings, 2),
                    'change': round(earnings_change, 1),
                    'label': 'Revenus totaux'
                },
            }
            
        except MentorProfile.DoesNotExist:
            pass
    
    elif user.role == 'student':
        try:
            student_profile = user.student_profile
            sessions = MentoringSession.objects.filter(
                student=student_profile,
                created_at__gte=start_date
            )
            
            previous_start = start_date - (now - start_date)
            previous_sessions = MentoringSession.objects.filter(
                student=student_profile,
                created_at__gte=previous_start,
                created_at__lt=start_date
            )
            
            total_sessions = sessions.count()
            previous_total = previous_sessions.count()
            sessions_change = ((total_sessions - previous_total) / previous_total * 100) if previous_total > 0 else 0
            
            completed = sessions.filter(status='completed').count()
            previous_completed = previous_sessions.filter(status='completed').count()
            completed_change = ((completed - previous_completed) / previous_completed * 100) if previous_completed > 0 else 0
            
            total_hours = sum(s.duration() / 60 for s in sessions.filter(status='completed'))
            previous_hours = sum(s.duration() / 60 for s in previous_sessions.filter(status='completed'))
            hours_change = ((total_hours - previous_hours) / previous_hours * 100) if previous_hours > 0 else 0
            
            active_mentors = sessions.values('mentor').distinct().count()
            previous_mentors = previous_sessions.values('mentor').distinct().count()
            mentors_change = ((active_mentors - previous_mentors) / previous_mentors * 100) if previous_mentors > 0 else 0
            
            kpis = {
                'total_sessions': {
                    'value': total_sessions,
                    'change': round(sessions_change, 1),
                    'label': 'Sessions totales'
                },
                'completed_sessions': {
                    'value': completed,
                    'change': round(completed_change, 1),
                    'label': 'Sessions terminées'
                },
                'total_hours': {
                    'value': round(total_hours, 1),
                    'change': round(hours_change, 1),
                    'label': 'Heures totales'
                },
                'active_mentors': {
                    'value': active_mentors,
                    'change': round(mentors_change, 1),
                    'label': 'Mentors actifs'
                },
            }
            
        except StudentProfile.DoesNotExist:
            pass
    
    return JsonResponse(kpis)

