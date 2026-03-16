from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from mentoring.models import MentorProfile

User = get_user_model()

class OnboardingCrashTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='mentor@example.com',
            password='password123',
            role='mentor',
            onboarding_completed=False
        )
        # Update profile (it might be auto-created by signals)
        MentorProfile.objects.update_or_create(
            user=self.user,
            defaults={
                'expertise': "Python",
                'years_of_experience': 5,
                'hourly_rate': 50.00,
                'languages': "Français"
            }
        )
        self.client.login(email='mentor@example.com', password='password123')

    def test_mentor_onboarding_page_rendering(self):
        """
        Test that accessing the mentor onboarding page does not crash with NoReverseMatch.
        """
        url = reverse('mentoring:mentor_onboarding')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
