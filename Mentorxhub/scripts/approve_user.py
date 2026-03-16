"""
Script pour valider l'onboarding d'un utilisateur
"""
import os
import django
import sys

# Configuration Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorxhub.settings')
django.setup()

from accounts.models import CustomUser

def approve_user():
    email = 'redirect_test@example.com'
    try:
        user = CustomUser.objects.get(email=email)
        user.onboarding_completed = True
        user.save()
        print(f"[OK] Utilisateur {email} debloque (onboarding_completed=True)")
    except CustomUser.DoesNotExist:
        print(f"[ERREUR] Utilisateur {email} introuvable")

if __name__ == '__main__':
    approve_user()
