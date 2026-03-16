"""
Script pour créer un utilisateur test et vérifier la redirection
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorxhub.settings')
django.setup()

from accounts.models import CustomUser

def create_test_user():
    """Crée un utilisateur test avec un mot de passe simple (pour test uniquement)"""
    
    email = 'redirect_test@example.com'
    
    # Supprimer l'utilisateur s'il existe
    CustomUser.objects.filter(email=email).delete()
    
    # Créer un nouvel utilisateur
    from django.contrib.auth.hashers import make_password
    
    user = CustomUser.objects.create(
        email=email,
        password=make_password('test1234'),  # Mot de passe simple pour test
        first_name='Redirect',
        last_name='Test',
        role='student',
        is_active=True
    )
    
    print(f"[OK] Utilisateur cree : {email}")
    print(f"Password : test1234")
    print(f"Role : {user.role}")
    print(f"")
    print("Testez maintenant la connexion sur :")
    print("http://127.0.0.1:8000/accounts/login/")

if __name__ == '__main__':
    create_test_user()
