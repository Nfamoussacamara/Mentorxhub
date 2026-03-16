from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from mentoring.models import MentorProfile, StudentProfile, MentoringSession

def home(request):
    """Page d'accueil publique avec statistiques"""
    from accounts.models import CustomUser
    
    # Calculer les statistiques pour la page d'accueil
    mentors_count = CustomUser.objects.filter(role='mentor', is_active=True).count()
    students_count = CustomUser.objects.filter(role='student', is_active=True).count()
    
    # Total des sessions
    sessions_count = MentoringSession.objects.filter(
        status__in=['pending', 'completed', 'scheduled']
    ).count()
    
    # Taux de satisfaction (basé sur la moyenne des ratings)
    avg_rating = MentoringSession.objects.filter(
        rating__isnull=False
    ).aggregate(Avg('rating'))['rating__avg']
    
    # Convertir en pourcentage (rating de 1-5 -> pourcentage)
    satisfaction_rate = int((avg_rating / 5.0) * 100) if avg_rating else 95
    
    # Valeurs par défaut si la base est vide
    stats = {
        'mentors_count': mentors_count if mentors_count > 0 else 150,
        'students_count': students_count if students_count > 0 else 500,
        'sessions_count': sessions_count if sessions_count > 0 else 850,
        'satisfaction_rate': satisfaction_rate,
    }
    
    context = {
        'stats': stats,
    }
    
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    """
    Dashboard principal qui redirige vers la vue appropriée selon le rôle.
    Si l'utilisateur n'a pas de rôle, redirige vers la sélection de rôle.
    """
    user = request.user
    
    # Vérifier le rôle et rediriger vers le dashboard approprié
    if user.role == 'mentor':
        return mentor_dashboard(request)
    elif user.role == 'student':
        return student_dashboard(request)
    else:
        # Si pas de rôle défini, rediriger vers la sélection de rôle
        # (le middleware devrait normalement gérer cela, mais c'est une sécurité supplémentaire)
        return redirect('accounts:onboarding_role')

@login_required
def mentor_dashboard(request):
    """Dashboard pour les mentors"""
    user = request.user
    
    # Vérifier si le profil mentor existe
    try:
        mentor_profile = user.mentor_profile
    except MentorProfile.DoesNotExist:
        # Si pas de profil mentor, créer un profil basique ou rediriger
        return render(request, 'dashboard-mentor.html', {
            'stats': {
                'pending_requests': 0,
                'total_sessions': 0,
                'avg_rating': 0.0,
                'monthly_earnings': 0.0,
            },
            'upcoming_sessions': [],
            'pending_count': 0,
        })
    
    # Calculer les statistiques
    today = timezone.now().date()
    current_month_start = today.replace(day=1)
    
    # Sessions à venir (ordonnées par date)
    upcoming_sessions = MentoringSession.objects.filter(
        mentor=mentor_profile,
        date__gte=today,
        status__in=['pending', 'scheduled', 'in_progress']
    ).select_related('student__user').order_by('date', 'start_time')[:5]
    
    # Demandes en attente (sessions avec statut scheduled récentes)
    pending_count = MentoringSession.objects.filter(
        mentor=mentor_profile,
        status='scheduled',
        date__gte=today
    ).count()
    
    # Total des sessions
    total_sessions = MentoringSession.objects.filter(
        mentor=mentor_profile
    ).count()
    
    # Note moyenne
    avg_rating = MentoringSession.objects.filter(
        mentor=mentor_profile,
        rating__isnull=False
    ).aggregate(Avg('rating'))['rating__avg'] or 0.0
    
    # Revenus du mois (calcul simplifié : nb sessions * tarif horaire)
    monthly_sessions = MentoringSession.objects.filter(
        mentor=mentor_profile,
        date__gte=current_month_start,
        date__lte=today,
        status='completed'
    ).count()
    
    monthly_earnings = monthly_sessions * float(mentor_profile.hourly_rate)
    
    stats = {
        'pending_requests': pending_count,
        'total_sessions': total_sessions,
        'avg_rating': avg_rating,
        'monthly_earnings': monthly_earnings,
    }
    
    context = {
        'stats': stats,
        'upcoming_sessions': upcoming_sessions,
        'pending_count': pending_count,
    }
    
    return render(request, 'dashboard-mentor.html', context)

@login_required
def student_dashboard(request):
    """Dashboard pour les étudiants"""
    user = request.user
    
    # Vérifier si le profil étudiant existe
    try:
        student_profile = user.student_profile
    except StudentProfile.DoesNotExist:
        # Si pas de profil étudiant, créer un profil basique ou rediriger
        return render(request, 'dashboard-mentee.html', {
            'stats': {
                'upcoming_sessions': 0,
                'total_hours': 0,
                'active_mentors': 0,
            },
            'upcoming_sessions': [],
            'recommended_mentors': [],
        })
    
    # Calculer les statistiques
    today = timezone.now().date()
    
    # Sessions à venir
    upcoming_sessions = MentoringSession.objects.filter(
        student=student_profile,
        date__gte=today,
        status__in=['pending', 'scheduled', 'in_progress']
    ).select_related('mentor__user').order_by('date', 'start_time')[:5]
    
    # Nombre de sessions à venir
    upcoming_count = upcoming_sessions.count()
    
    # Total heures de mentorat (calculer la durée de toutes les sessions complétées)
    completed_sessions = MentoringSession.objects.filter(
        student=student_profile,
        status='completed'
    )
    
    total_hours = 0
    for session in completed_sessions:
        total_hours += session.duration() / 60  # Convertir minutes en heures
    
    # Nombre de mentors actifs (mentors avec qui l'étudiant a eu des sessions)
    active_mentors = MentoringSession.objects.filter(
        student=student_profile,
        status__in=['pending', 'completed', 'scheduled']
    ).values('mentor').distinct().count()
    
    # Mentors recommandés (les mieux notés et disponibles)
    recommended_mentors = MentorProfile.objects.filter(
        is_available=True
    ).exclude(
        # Exclure les mentors avec qui l'étudiant a déjà des sessions à venir
        mentoring_sessions__student=student_profile,
        mentoring_sessions__date__gte=today,
        mentoring_sessions__status='scheduled'
    ).order_by('-rating', '-total_sessions')[:4]
    
    stats = {
        'upcoming_sessions': upcoming_count,
        'total_hours': int(total_hours),
        'active_mentors': active_mentors,
    }
    
    context = {
        'stats': stats,
        'upcoming_sessions': upcoming_sessions,
        'recommended_mentors': recommended_mentors,
    }
    
    return render(request, 'dashboard-mentee.html', context)


# ============================================================
# PAGES PUBLIQUES
# ============================================================

def pricing_view(request):
    """
    Page de présentation des tarifs de la plateforme.
    Affiche les différentes options de tarification et les avantages.
    Accessible à tous les visiteurs (connectés ou non).
    """
    context = {
        'page_title': 'Tarifs',
        'plans': [
            {
                'name': 'Gratuit',
                'price': '0',
                'features': [
                    'Parcourir tous les mentors',
                    'Voir les profils complets',
                    'Messagerie de base',
                    'Support communautaire',
                ]
            },
            {
                'name': 'Étudiant',
                'price': '29',
                'popular': True,
                'features': [
                    'Toutes les fonctionnalités gratuites',
                    'Sessions de mentorat illimitées',
                    'Accès au matériel de formation',
                    'Support prioritaire',
                    'Certificats de complétion',
                ]
            },
            {
                'name': 'Mentor Pro',
                'price': '49',
                'features': [
                    'Profil mis en avant',
                    'Statistiques avancées',
                    'Calendrier intégré',
                    'Outils de gestion',
                    'Support dédié',
                ]
            },
        ]
    }
    return render(request, 'core/pricing.html', context)


def top_mentors_view(request):
    """
    Affiche la liste des mentors les mieux notés.
    Trie par note moyenne et nombre de sessions complétées.
    Accessible à tous les visiteurs.
    """
    from django.db.models import Avg, Count
    
    # Récupérer les mentors les mieux notés avec leurs statistiques
    top_mentors = MentorProfile.objects.filter(
        user__is_active=True
    ).annotate(
        avg_rating=Avg('mentoring_sessions__rating'),
        sessions_count=Count('mentoring_sessions', filter=Q(mentoring_sessions__status='completed'))
    ).filter(
        sessions_count__gt=0  # Au moins une session complétée
    ).order_by('-avg_rating', '-sessions_count')[:20]
    
    context = {
        'page_title': 'Mentors Mieux Notés',
        'mentors': top_mentors,
    }
    return render(request, 'core/top_mentors.html', context)


def about_view(request):
    """
    Page À propos de MentorXHub.
    Présente la mission, la vision et l'équipe de la plateforme.
    Accessible à tous les visiteurs.
    """
    context = {
        'page_title': 'À Propos',
        'stats': {
            'mentors': MentorProfile.objects.filter(user__is_active=True).count() or 150,
            'students': StudentProfile.objects.filter(user__is_active=True).count() or 500,
            'sessions': MentoringSession.objects.filter(status='completed').count() or 850,
            'satisfaction': 95,
        },
        'team_members': [
            {
                'name': 'Équipe MentorXHub',
                'role': 'Fondateurs',
                'description': 'Une équipe passionnée dédiée à connecter les mentors et les étudiants.',
            }
        ]
    }
    return render(request, 'core/about.html', context)


def how_it_works_view(request):
    """
    Page expliquant le fonctionnement de la plateforme.
    Guide pas à pas pour les mentors et les étudiants.
    Accessible à tous les visiteurs.
    """
    context = {
        'page_title': 'Comment Ça Marche',
        'steps_student': [
            {
                'number': 1,
                'title': 'Créez votre profil',
                'description': 'Inscrivez-vous gratuitement et complétez votre profil étudiant.',
                'icon': '👤'
            },
            {
                'number': 2,
                'title': 'Trouvez un mentor',
                'description': 'Parcourez notre liste de mentors experts dans différents domaines.',
                'icon': '🔍'
            },
            {
                'number': 3,
                'title': 'Réservez une session',
                'description': 'Choisissez un créneau horaire qui vous convient.',
                'icon': '📅'
            },
            {
                'number': 4,
                'title': 'Apprenez et progressez',
                'description': 'Participez à vos sessions et atteignez vos objectifs.',
                'icon': '🚀'
            },
        ],
        'steps_mentor': [
            {
                'number': 1,
                'title': 'Devenez mentor',
                'description': 'Créez votre profil mentor et partagez votre expertise.',
                'icon': '🎓'
            },
            {
                'number': 2,
                'title': 'Définissez vos disponibilités',
                'description': 'Configurez votre calendrier et vos tarifs.',
                'icon': '⏰'
            },
            {
                'number': 3,
                'title': 'Acceptez des demandes',
                'description': 'Recevez et acceptez les demandes de sessions.',
                'icon': '✅'
            },
            {
                'number': 4,
                'title': 'Partagez votre savoir',
                'description': 'Inspirez et guidez la prochaine génération.',
                'icon': '💡'
            },
        ]
    }
    return render(request, 'core/how_it_works.html', context)


def careers_view(request):
    """
    Page Carrières de MentorXHub.
    Liste des opportunités d'emploi et présentation de la culture d'entreprise.
    Accessible à tous les visiteurs.
    """
    context = {
        'page_title': 'Carrières',
        'positions': [
            {
                'title': 'Développeur Full-Stack',
                'type': 'Temps plein',
                'location': 'Remote',
                'description': 'Nous recherchons un développeur passionné pour rejoindre notre équipe.',
            },
            {
                'title': 'Designer UI/UX',
                'type': 'Temps plein',
                'location': 'Remote',
                'description': 'Créez des expériences utilisateur exceptionnelles pour notre plateforme.',
            },
            {
                'title': 'Community Manager',
                'type': 'Temps partiel',
                'location': 'Remote',
                'description': 'Animez notre communauté de mentors et d\'étudiants.',
            },
        ]
    }
    return render(request, 'core/careers.html', context)


def blog_view(request):
    """
    Page Blog - Liste des articles.
    Affiche les derniers articles et conseils sur le mentorat.
    Accessible à tous les visiteurs.
    """
    context = {
        'page_title': 'Blog',
        'articles': [
            {
                'title': 'Comment choisir le bon mentor pour votre carrière',
                'excerpt': 'Découvrez les critères essentiels pour trouver le mentor idéal qui vous aidera à atteindre vos objectifs professionnels.',
                'date': '2024-12-01',
                'author': 'Équipe MentorXHub',
                'image': '/static/images/blog/mentor-choice.jpg',
            },
            {
                'title': '5 conseils pour tirer le meilleur parti de vos sessions de mentorat',
                'excerpt': 'Maximisez la valeur de chaque session avec ces stratégies éprouvées.',
                'date': '2024-11-28',
                'author': 'Équipe MentorXHub',
                'image': '/static/images/blog/tips.jpg',
            },
            {
                'title': 'L\'importance du mentorat dans le développement professionnel',
                'excerpt': 'Pourquoi le mentorat est crucial pour votre croissance de carrière.',
                'date': '2024-11-25',
                'author': 'Équipe MentorXHub',
                'image': '/static/images/blog/importance.jpg',
            },
        ]
    }
    return render(request, 'core/blog.html', context)


def privacy_policy_view(request):
    """
    Page Politique de Confidentialité.
    Détaille comment les données des utilisateurs sont collectées et utilisées.
    Accessible à tous les visiteurs.
    """
    context = {
        'page_title': 'Politique de Confidentialité',
        'last_updated': '7 Décembre 2024',
    }
    return render(request, 'core/privacy_policy.html', context)


def terms_of_service_view(request):
    """
    Page Conditions d'Utilisation.
    Présente les termes et conditions d'utilisation de la plateforme.
    Accessible à tous les visiteurs.
    """
    context = {
        'page_title': 'Conditions d\'Utilisation',
        'last_updated': '7 Décembre 2024',
    }
    return render(request, 'core/terms_of_service.html', context)


def all_links_view(request):
    """
    Page qui affiche tous les liens disponibles dans l'application.
    Utile pour le développement et la documentation.
    Accessible à tous les visiteurs.
    """
    from django.urls import get_resolver
    from django.urls.resolvers import URLPattern, URLResolver
    
    def extract_urls(urlpatterns, prefix=''):
        """Extrait récursivement toutes les URLs du projet"""
        urls = []
        for pattern in urlpatterns:
            if isinstance(pattern, URLPattern):
                try:
                    url_name = pattern.name
                    url_path = prefix + str(pattern.pattern)
                    urls.append({
                        'name': url_name,
                        'path': url_path,
                        'namespace': pattern.namespace if hasattr(pattern, 'namespace') else None,
                    })
                except:
                    pass
            elif isinstance(pattern, URLResolver):
                namespace = pattern.namespace
                new_prefix = prefix + str(pattern.pattern)
                urls.extend(extract_urls(pattern.url_patterns, new_prefix))
        return urls
    
    # Récupérer toutes les URLs
    resolver = get_resolver()
    all_urls = extract_urls(resolver.url_patterns)
    
    # Organiser par namespace
    urls_by_namespace = {}
    for url_info in all_urls:
        namespace = url_info.get('namespace') or 'core'
        if namespace not in urls_by_namespace:
            urls_by_namespace[namespace] = []
        urls_by_namespace[namespace].append(url_info)
    
    context = {
        'page_title': 'Tous les Liens - MentorXHub',
        'urls_by_namespace': urls_by_namespace,
        'total_urls': len(all_urls),
    }
    return render(request, 'core/all_links.html', context)
