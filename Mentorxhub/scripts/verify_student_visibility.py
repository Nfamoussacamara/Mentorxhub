"""
Script de vérification pour la visibilité des sessions étudiant.
Vérifie que les sessions 'pending' apparaissent bien dans le dashboard et le profil étudiant.
"""
import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

# Configuration Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
print(f"DEBUG: sys.path = {sys.path}")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorxhub.settings')
try:
    import django
    print(f"DEBUG: django version = {django.get_version()}")
except ImportError as e:
    print(f"DEBUG: Failed to import django: {e}")
    sys.exit(1)
django.setup()

from django.test import Client, RequestFactory
from django.contrib.auth import get_user_model
from mentoring.models import MentorProfile, StudentProfile, MentoringSession
from dashboard.views.dashboard import student_dashboard
from mentoring.views.main import StudentProfileView

User = get_user_model()

def verify_visibility():
    print("=" * 60)
    print("VÉRIFICATION DE LA VISIBILITÉ DES SESSIONS ÉTUDIANT")
    print("=" * 60)
    
    # 1. Préparation des données
    print("\n1. Préparation des données de test...")
    
    # Créer ou récupérer mentor
    mentor_user, _ = User.objects.get_or_create(
        email='test_mentor_vis@test.com',
        defaults={'first_name': 'Mentor', 'last_name': 'Test', 'role': 'mentor'}
    )
    mentor_user.set_password('pass123')
    mentor_user.save()
    
    mentor_profile, _ = MentorProfile.objects.get_or_create(
        user=mentor_user,
        defaults={'expertise': 'Test', 'hourly_rate': 50}
    )
    
    # Créer ou récupérer étudiant
    student_user, _ = User.objects.get_or_create(
        email='test_student_vis@test.com',
        defaults={'first_name': 'Student', 'last_name': 'Test', 'role': 'student'}
    )
    student_user.set_password('pass123')
    student_user.save()
    
    student_profile, _ = StudentProfile.objects.get_or_create(
        user=student_user,
        defaults={'level': 'Beginner'}
    )
    
    # Nettoyer les sessions existantes pour ce test
    MentoringSession.objects.filter(student=student_profile).delete()
    
    # Créer une session PENDING
    pending_session = MentoringSession.objects.create(
        student=student_profile,
        mentor=mentor_profile,
        title='Session de Test Visibility',
        date=timezone.now().date() + timedelta(days=1),
        start_time='10:00:00',
        duration=60,
        status='pending'
    )
    print(f"   ✅ Session 'pending' créée: {pending_session.id}")
    
    # 2. Vérification Dashboard Étudiant
    print("\n2. Vérification du dashboard étudiant...")
    factory = RequestFactory()
    request = factory.get('/dashboard/')
    request.user = student_user
    
    response = student_dashboard(request)
    
    # Pour tester le contexte si c'est une TemplateResponse
    if hasattr(response, 'context_data'):
        context = response.context_data
        upcoming = context.get('upcoming_sessions', [])
        sessions_open = context.get('stats', {}).get('sessions_open', 0)
        
        found = any(s.id == pending_session.id for s in upcoming)
        if found:
            print("   ✅ Session 'pending' trouvée dans upcoming_sessions !")
        else:
            print("   ❌ Session 'pending' ABSENTE de upcoming_sessions")
            
        if sessions_open >= 1:
            print(f"   ✅ Stats sessions_open correcte: {sessions_open}")
        else:
            print(f"   ❌ Stats sessions_open incorrecte: {sessions_open}")
    else:
        # Si c'est un HttpResponse normal (render), on ne peut pas facilement inspecter le contexte sans Client()
        client = Client()
        client.force_login(student_user)
        response = client.get('/dashboard/')
        
        # On vérifie la présence dans le contenu HTML (moins précis mais utile)
        if b'Session de Test Visibility' in response.content:
            print("   ✅ Session trouvée dans le rendu HTML du dashboard !")
        else:
            print("   ❌ Session ABSENTE du rendu HTML du dashboard")

    # 3. Vérification Profil Étudiant
    print("\n3. Vérification de la vue Profil Étudiant...")
    view = StudentProfileView()
    view.request = request
    view.object = student_profile
    context = view.get_context_data()
    
    upcoming_profile = context.get('upcoming_sessions', [])
    found_profile = any(s.id == pending_session.id for s in upcoming_profile)
    
    if found_profile:
        print("   ✅ Session 'pending' trouvée dans StudentProfileView.upcoming_sessions !")
    else:
        print("   ❌ Session 'pending' ABSENTE de StudentProfileView.upcoming_sessions")
        
    active_mentors = context.get('active_mentors', 0)
    if active_mentors >= 1:
        print(f"   ✅ Count active_mentors correct: {active_mentors}")
    else:
        print(f"   ❌ Count active_mentors incorrect: {active_mentors}")

    print("\n" + "=" * 60)
    print("FIN DE VÉRIFICATION")
    print("=" * 60)

if __name__ == '__main__':
    verify_visibility()
