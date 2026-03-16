"""
Script pour vérifier la connexion à la base de données
et lister tous les utilisateurs
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorxhub.settings')
django.setup()

from accounts.models import CustomUser
from mentoring.models import StudentProfile, MentorProfile

def check_database():
    """Vérifie la connexion à la base de données"""
    
    print("=" * 60)
    print("VERIFICATION BASE DE DONNEES - MentorXHub")
    print("=" * 60)
    print("")
    
    # Compter les utilisateurs
    total_users = CustomUser.objects.count()
    mentors_count = CustomUser.objects.filter(role='mentor').count()
    students_count = CustomUser.objects.filter(role='student').count()
    
    print(f"Total utilisateurs : {total_users}")
    print(f"Mentors : {mentors_count}")
    print(f"Etudiants : {students_count}")
    print("")
    
    # Lister tous les utilisateurs
    print("=" * 60)
    print("LISTE DES UTILISATEURS")
    print("=" * 60)
    
    users = CustomUser.objects.all().order_by('-date_joined')
    
    if users.exists():
        for i, user in enumerate(users, 1):
            print(f"\n--- Utilisateur {i} ---")
            print(f"ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Username: {user.username}")
            print(f"Nom complet: {user.get_full_name()}")
            print(f"Role: {user.role}")
            print(f"Is active: {user.is_active}")
            print(f"Is superuser: {user.is_superuser}")
            print(f"Date inscription: {user.date_joined}")
            
            # Vérifier si le profil existe
            if user.role == 'student':
                has_profile = hasattr(user, 'student_profile')
                print(f"A un profil etudiant: {has_profile}")
                if has_profile:
                    print(f"  - Level: {user.student_profile.level}")
                    print(f"  - Objectifs: {user.student_profile.learning_goals}")
            elif user.role == 'mentor':
                has_profile = hasattr(user, 'mentor_profile')
                print(f"A un profil mentor: {has_profile}")
                if has_profile:
                    print(f"  - Expertise: {user.mentor_profile.expertise}")
                    print(f"  - Experience: {user.mentor_profile.years_of_experience} ans")
                    print(f"  - Tarif: {user.mentor_profile.hourly_rate} EUR/h")
    else:
        print("Aucun utilisateur trouve dans la base de donnees!")
    
    print("")
    print("=" * 60)
    print("PROFILS")
    print("=" * 60)
    student_profiles = StudentProfile.objects.count()
    mentor_profiles = MentorProfile.objects.count()
    print(f"Profils etudiants: {student_profiles}")
    print(f"Profils mentors: {mentor_profiles}")
    print("")

if __name__ == '__main__':
    check_database()
