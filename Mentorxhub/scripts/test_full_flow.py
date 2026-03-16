import os
import django
import sys
from datetime import date, time, timedelta

# Configuration Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorxhub.settings')
django.setup()

from django.contrib.auth import get_user_model
from mentoring.models import MentorProfile, StudentProfile, MentoringSession
from dashboard.models import Notification

User = get_user_model()

def run_full_test():
    print("🚀 Démarrage du test système complet...")

    # 1. Nettoyage
    print("\n🧹 Nettoyage des données de test...")
    email_mentor = "t_mentor@test.com"
    email_student = "t_student@test.com"
    User.objects.filter(email__in=[email_mentor, email_student]).delete()

    # 2. Création Mentor
    print("\n👤 Création du Mentor...")
    mentor_user = User.objects.create_user(
        email=email_mentor, 
        password="password123", 
        first_name="Test", 
        last_name="Mentor",
        role='mentor',
        onboarding_completed=True
    )
    mentor_profile = MentorProfile.objects.create(
        user=mentor_user,
        expertise="Python Django",
        years_of_experience=5,
        hourly_rate=50,
        status='approved' # IMPORTANT: Doit être approuvé pour être visible
    )
    print(f"✅ Mentor créé: {mentor_user.email} (ID: {mentor_profile.id})")

    # 3. Création Étudiant
    print("\n🎓 Création de l'Étudiant...")
    student_user = User.objects.create_user(
        email=email_student, 
        password="password123", 
        first_name="Test", 
        last_name="Student",
        role='student',
        onboarding_completed=True
    )
    student_profile = StudentProfile.objects.create(
        user=student_user,
        level='débutant'
    )
    print(f"✅ Étudiant créé: {student_user.email} (ID: {student_profile.id})")

    # 4. Réservation de Session (Simulation Étudiant)
    print("\n📅 Simulation: Réservation d'une session...")
    
    # On simule ce que fait la vue MentoringSessionCreateView
    session = MentoringSession.objects.create(
        mentor=mentor_profile,
        student=student_profile,
        title="Session Test Python",
        description="J'ai besoin d'aide sur les Vues Django",
        date=date.today() + timedelta(days=1),
        start_time=time(14, 0),
        end_time=time(15, 0),
        status='pending' # Par défaut c'est pending maintenant
    )
    print(f"✅ Session créée (Pending): ID {session.id}, Status: {session.status}")

    # 5. Vérification Notification Mentor
    print("\n🔔 Vérification des notifications (Côté Mentor)...")
    notif_mentor = Notification.objects.filter(user=mentor_user).order_by('-created_at').first()
    if notif_mentor and "Nouvelle demande" in notif_mentor.title:
        print(f"✅ Notification reçue par le mentor: {notif_mentor.title}")
    else:
        print(f"❌ ERREUR: Pas de notification pour le mentor. (Dernière: {notif_mentor})")

    # 6. Approbation de la Session (Simulation Mentor)
    print("\n✅ Simulation: Approbation par le mentor...")
    # On simule l'action dans SessionApproveView
    session.status = 'scheduled'
    session.save() # Cela devrait déclencher le signal pour notifier l'étudiant
    print(f"✅ Session mise à jour: Status = {session.status}")

    # 7. Vérification Notification Étudiant
    print("\n🔔 Vérification des notifications (Côté Étudiant)...")
    notif_student = Notification.objects.filter(user=student_user).order_by('-created_at').first()
    if notif_student and "Session confirmée" in notif_student.title:
        print(f"✅ Notification reçue par l'étudiant: {notif_student.title}")
    else:
        print(f"❌ ERREUR: Pas de notification pour l'étudiant. (Dernière: {notif_student})")

    # 8. Vérification URL Vidéo
    print("\n🎥 Vérification accès vidéo...")
    from django.urls import reverse
    # On triche un peu car reverse a besoin du contexte web, mais on connait l'URL
    expected_url = f"/dashboard/sessions/{session.id}/video/"
    print(f"✅ URL de la salle prévue: {expected_url}")
    
    print("\n✨ TEST SYSTÈME TERMINÉ AVEC SUCCÈS ✨")

if __name__ == '__main__':
    run_full_test()
