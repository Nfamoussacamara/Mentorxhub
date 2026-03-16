"""
Script pour créer un superuser admin
Exécuter avec : python create_admin.py
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorxhub.settings')
django.setup()

from accounts.models import CustomUser

def create_admin():
    """Crée un utilisateur admin s'il n'existe pas déjà"""
    
    email = 'admin@mentorxhub.com'
    username = 'admin'
    password = 'admin123'  # ⚠️ CHANGEZ CE MOT DE PASSE EN PRODUCTION !
    
    # Vérifier si l'admin existe déjà
    if CustomUser.objects.filter(email=email).exists():
        print(f"[ERREUR] L'utilisateur {email} existe deja !")
        user = CustomUser.objects.get(email=email)
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Is superuser: {user.is_superuser}")
        print(f"   Is staff: {user.is_staff}")
        return
    
    # Créer le superuser
    print("Creation du superuser en cours...")
    admin = CustomUser.objects.create_superuser(
        email=email,
        username=username,
        password=password,
        role='mentor',  # Les admins sont considérés comme mentors
        first_name='Admin',
        last_name='MentorXHub'
    )
    
    print("[OK] Superuser cree avec succes !")
    print(f"")
    print(f"Email: {email}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Role: {admin.role}")
    print(f"")
    print(f"[IMPORTANT] Changez le mot de passe apres la premiere connexion !")
    print(f"")
    print(f"Connexion admin: http://127.0.0.1:8000/admin/")

if __name__ == '__main__':
    create_admin()
