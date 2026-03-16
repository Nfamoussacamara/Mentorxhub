from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from accounts.services.role_transition import RoleTransitionService
from mentoring.models import MentorProfile, StudentProfile

class RoleTransitionServiceTest(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create(
            email='student@example.com',
            role='student',
            password='password123'
        )
        self.mentor = CustomUser.objects.create(
            email='mentor@example.com',
            role='mentor',
            password='password123'
        )
        self.admin = CustomUser.objects.create(
            email='admin@example.com',
            role='student',
            is_staff=True,
            password='password123'
        )

    def test_request_mentorship_success(self):
        """Test qu'un étudiant peut faire une demande"""
        profile = RoleTransitionService.request_mentorship(self.student)
        self.assertEqual(profile.user, self.student)
        self.assertEqual(profile.status, 'pending')
        # Vérifie que le rôle n'a PAS changé
        self.student.refresh_from_db()
        self.assertEqual(self.student.role, 'student')

    def test_request_mentorship_already_mentor(self):
        """Test qu'un mentor ne peut pas refaire une demande"""
        with self.assertRaisesMessage(ValidationError, "L'utilisateur est déjà un mentor"):
            RoleTransitionService.request_mentorship(self.mentor)

    def test_request_mentorship_existing_pending(self):
        """Test qu'on ne peut pas avoir deux demandes en cours"""
        RoleTransitionService.request_mentorship(self.student)
        with self.assertRaisesMessage(ValidationError, "Une demande est déjà en cours"):
            RoleTransitionService.request_mentorship(self.student)

    def test_approve_mentorship_success(self):
        """Test la validation par un admin"""
        RoleTransitionService.request_mentorship(self.student)
        
        updated_user = RoleTransitionService.approve_mentorship(self.student, self.admin)
        
        self.assertEqual(updated_user.role, 'mentor')
        self.assertEqual(updated_user.mentor_profile.status, 'approved')

    def test_approve_mentorship_unauthorized(self):
        """Test qu'un non-admin ne peut pas valider"""
        RoleTransitionService.request_mentorship(self.student)
        
        with self.assertRaisesMessage(ValidationError, "Seul un administrateur peut"):
            RoleTransitionService.approve_mentorship(self.student, self.student)

    def test_approve_mentorship_no_request(self):
        """Test validation sans demande préalable"""
        user_no_request = CustomUser.objects.create(email='other@test.com', role='student')
        with self.assertRaisesMessage(ValidationError, "Aucun profil mentor associé"):
            RoleTransitionService.approve_mentorship(user_no_request, self.admin)
    def test_approve_mentorship_preserves_history(self):
        """Test que l'historique (StudentProfile) est conservé après transition"""
        # S'assurer qu'un profil étudiant existe (le créer s'il n'existe pas déjà)
        student_profile, _ = StudentProfile.objects.get_or_create(user=self.student)
        
        RoleTransitionService.request_mentorship(self.student)
        RoleTransitionService.approve_mentorship(self.student, self.admin)
        
        self.student.refresh_from_db()
        self.assertEqual(self.student.role, 'mentor')
        # Vérifier que le profil étudiant existe toujours
        self.assertTrue(StudentProfile.objects.filter(user=self.student).exists())
        self.assertEqual(self.student.student_profile, student_profile)
