from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from accounts.models import CustomUser
from accounts.middleware import OnboardingMiddleware

class OnboardingMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Mock get_response to return 200 OK
        self.get_response_mock = lambda request: "Success"
        self.middleware = OnboardingMiddleware(self.get_response_mock)
        
        # URLs
        self.url_dashboard = reverse('dashboard:dashboard')
        self.url_role = reverse('accounts:onboarding_role')
        self.url_mentee = reverse('mentoring:mentee_onboarding')
        self.url_mentor = reverse('mentoring:mentor_onboarding')
        self.url_login = reverse('accounts:login')

    def test_public_url_access(self):
        """Test que les URLs publiques ne sont pas interceptées"""
        request = self.factory.get(self.url_login)
        request.user = AnonymousUser()
        response = self.middleware(request)
        self.assertEqual(response, "Success")

    def test_authenticated_no_role_redirect(self):
        """Test redirection vers choix du rôle si pas de rôle"""
        user = CustomUser.objects.create(email='test@test.com', password='pwd')
        # Pas de rôle
        request = self.factory.get(self.url_dashboard)
        request.user = user
        
        response = self.middleware(request)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url_role)

    def test_student_incomplete_redirect(self):
        """Test redirection étudiant vers onboarding mentee"""
        user = CustomUser.objects.create(
            email='student@test.com', 
            password='pwd',
            role='student',
            onboarding_completed=False
        )
        request = self.factory.get(self.url_dashboard)
        request.user = user
        
        response = self.middleware(request)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url_mentee)

    def test_mentor_incomplete_redirect(self):
        """Test redirection mentor vers onboarding mentor"""
        user = CustomUser.objects.create(
            email='mentor@test.com', 
            password='pwd',
            role='mentor',
            onboarding_completed=False
        )
        request = self.factory.get(self.url_dashboard)
        request.user = user
        
        response = self.middleware(request)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url_mentor)

    def test_completed_onboarding_access(self):
        """Test accès autorisé si onboarding complet"""
        user = CustomUser.objects.create(
            email='done@test.com', 
            password='pwd',
            role='student',
            onboarding_completed=True
        )
        request = self.factory.get(self.url_dashboard)
        request.user = user
        
        response = self.middleware(request)
        
        self.assertEqual(response, "Success")

    def test_access_onboarding_url_allowed(self):
        """Test accès autorisé à la page d'onboarding cible (pas de boucle)"""
        user = CustomUser.objects.create(
            email='loop@test.com', 
            password='pwd',
            role='student',
            onboarding_completed=False
        )
        # L'utilisateur essaie d'accéder à SA page d'onboarding
        request = self.factory.get(self.url_mentee)
        request.user = user
        
        response = self.middleware(request)
        
        self.assertEqual(response, "Success")
