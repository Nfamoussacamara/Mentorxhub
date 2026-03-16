"""
Script de test pour vérifier que le dashboard fonctionne correctement
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Mentorxhub'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorxhub.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from mentoring.models import MentorProfile, StudentProfile

User = get_user_model()

def test_dashboard_urls():
    """Test que les URLs du dashboard sont accessibles"""
    print("=" * 60)
    print("TEST DES URLs DU DASHBOARD")
    print("=" * 60)
    
    client = Client()
    
    # Test 1: Dashboard sans authentification (doit rediriger)
    print("\n1. Test dashboard sans authentification...")
    response = client.get('/dashboard/')
    if response.status_code == 302:
        print("   ✅ Redirection vers login correcte")
    else:
        print(f"   ❌ Erreur: Status {response.status_code}")
    
    # Test 2: Créer un utilisateur mentor et tester
    print("\n2. Test avec utilisateur mentor...")
    try:
        mentor_user = User.objects.filter(email='test_mentor@test.com').first()
        if not mentor_user:
            mentor_user = User.objects.create_user(
                email='test_mentor@test.com',
                password='testpass123',
                first_name='Mentor',
                last_name='Test',
                role='mentor'
            )
            MentorProfile.objects.create(
                user=mentor_user,
                expertise='Web Development',
                years_of_experience=5,
                hourly_rate=50.00,
                languages='Python, JavaScript'
            )
            print("   ✅ Utilisateur mentor créé")
        else:
            print("   ℹ️  Utilisateur mentor existe déjà")
        
        client.force_login(mentor_user)
        response = client.get('/dashboard/')
        if response.status_code == 200:
            print("   ✅ Dashboard accessible pour mentor")
        else:
            print(f"   ❌ Erreur: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: Créer un utilisateur étudiant et tester
    print("\n3. Test avec utilisateur étudiant...")
    try:
        student_user = User.objects.filter(email='test_student@test.com').first()
        if not student_user:
            student_user = User.objects.create_user(
                email='test_student@test.com',
                password='testpass123',
                first_name='Student',
                last_name='Test',
                role='student'
            )
            StudentProfile.objects.create(
                user=student_user,
                level='Intermediate'
            )
            print("   ✅ Utilisateur étudiant créé")
        else:
            print("   ℹ️  Utilisateur étudiant existe déjà")
        
        client.force_login(student_user)
        response = client.get('/dashboard/')
        if response.status_code == 200:
            print("   ✅ Dashboard accessible pour étudiant")
        else:
            print(f"   ❌ Erreur: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 4: Vérifier les URLs reverse
    print("\n4. Test des reverse URLs...")
    try:
        dashboard_url = reverse('dashboard:dashboard')
        print(f"   ✅ URL reverse: {dashboard_url}")
        
        home_url = reverse('dashboard:home')
        print(f"   ✅ URL reverse home: {home_url}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("TESTS TERMINÉS")
    print("=" * 60)

if __name__ == '__main__':
    test_dashboard_urls()

