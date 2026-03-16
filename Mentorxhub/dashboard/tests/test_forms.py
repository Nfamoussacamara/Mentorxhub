"""
Tests unitaires pour les formulaires du dashboard
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from dashboard.forms import (
    UserProfileForm, DashboardSettingsForm, CourseForm, LessonForm,
    SupportTicketForm, MessageForm, PaymentForm
)

User = get_user_model()


class UserProfileFormTest(TestCase):
    """Tests pour le formulaire UserProfileForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_valid_profile_form(self):
        """Test un formulaire valide"""
        form = UserProfileForm({
            'bio': 'Test bio',
            'location': 'Paris, France',
            'phone': '+33123456789',
            'website': 'https://example.com'
        }, instance=self.user.userprofile)
        self.assertTrue(form.is_valid())
    
    def test_profile_form_save(self):
        """Test la sauvegarde du formulaire"""
        form = UserProfileForm({
            'bio': 'Test bio',
            'location': 'Paris, France'
        }, instance=self.user.userprofile)
        self.assertTrue(form.is_valid())
        profile = form.save()
        self.assertEqual(profile.bio, 'Test bio')
        self.assertEqual(profile.location, 'Paris, France')
    
    def test_profile_form_avatar_upload(self):
        """Test l'upload d'un avatar"""
        image = SimpleUploadedFile(
            "avatar.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        form = UserProfileForm(
            {'bio': 'Test bio'},
            {'avatar': image},
            instance=self.user.userprofile
        )
        self.assertTrue(form.is_valid())
        profile = form.save()
        self.assertIsNotNone(profile.avatar)


class DashboardSettingsFormTest(TestCase):
    """Tests pour le formulaire DashboardSettingsForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_valid_settings_form(self):
        """Test un formulaire de paramètres valide"""
        form = DashboardSettingsForm({
            'theme': 'dark',
            'notifications_enabled': True,
            'email_notifications': True
        }, instance=self.user.dashboardsettings)
        self.assertTrue(form.is_valid())
    
    def test_settings_form_save(self):
        """Test la sauvegarde des paramètres"""
        form = DashboardSettingsForm({
            'theme': 'dark'
        }, instance=self.user.dashboardsettings)
        self.assertTrue(form.is_valid())
        settings = form.save()
        self.assertEqual(settings.theme, 'dark')


class CourseFormTest(TestCase):
    """Tests pour le formulaire CourseForm"""
    
    def setUp(self):
        self.mentor = User.objects.create_user(
            email='mentor@example.com',
            password='testpass123',
            role='mentor'
        )
    
    def test_valid_course_form(self):
        """Test un formulaire de cours valide"""
        form = CourseForm({
            'title': 'Test Course',
            'description': 'Test description',
            'price': 99.99,
            'status': 'published'
        })
        form.instance.mentor = self.mentor
        self.assertTrue(form.is_valid())
    
    def test_course_form_save(self):
        """Test la sauvegarde d'un cours"""
        form = CourseForm({
            'title': 'Test Course',
            'description': 'Test description',
            'price': 99.99
        })
        form.instance.mentor = self.mentor
        self.assertTrue(form.is_valid())
        course = form.save()
        self.assertEqual(course.title, 'Test Course')
        self.assertEqual(course.mentor, self.mentor)
    
    def test_course_form_required_fields(self):
        """Test les champs requis"""
        form = CourseForm({})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class LessonFormTest(TestCase):
    """Tests pour le formulaire LessonForm"""
    
    def setUp(self):
        self.mentor = User.objects.create_user(
            email='mentor@example.com',
            password='testpass123',
            role='mentor'
        )
        self.course = CourseForm({
            'title': 'Test Course',
            'description': 'Test description'
        })
        self.course.instance.mentor = self.mentor
        self.course.save()
    
    def test_valid_lesson_form(self):
        """Test un formulaire de leçon valide"""
        from dashboard.models import Course
        course = Course.objects.first()
        form = LessonForm({
            'title': 'Test Lesson',
            'content': 'Test content',
            'order': 1
        })
        form.instance.course = course
        self.assertTrue(form.is_valid())
    
    def test_lesson_form_save(self):
        """Test la sauvegarde d'une leçon"""
        from dashboard.models import Course
        course = Course.objects.first()
        form = LessonForm({
            'title': 'Test Lesson',
            'content': 'Test content',
            'order': 1
        })
        form.instance.course = course
        self.assertTrue(form.is_valid())
        lesson = form.save()
        self.assertEqual(lesson.title, 'Test Lesson')
        self.assertEqual(lesson.course, course)


class SupportTicketFormTest(TestCase):
    """Tests pour le formulaire SupportTicketForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
    
    def test_valid_ticket_form(self):
        """Test un formulaire de ticket valide"""
        form = SupportTicketForm({
            'subject': 'Test Subject',
            'description': 'Test description',
            'priority': 'medium'
        })
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
    
    def test_ticket_form_save(self):
        """Test la sauvegarde d'un ticket"""
        form = SupportTicketForm({
            'subject': 'Test Subject',
            'description': 'Test description',
            'priority': 'high'
        })
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
        ticket = form.save()
        self.assertEqual(ticket.subject, 'Test Subject')
        self.assertEqual(ticket.user, self.user)
        self.assertEqual(ticket.priority, 'high')
    
    def test_ticket_form_required_fields(self):
        """Test les champs requis"""
        form = SupportTicketForm({})
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)
        self.assertIn('description', form.errors)


class MessageFormTest(TestCase):
    """Tests pour le formulaire MessageForm"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='testpass123'
        )
        from dashboard.models import Conversation
        self.conversation = Conversation.objects.create(
            participant1=self.user1,
            participant2=self.user2
        )
    
    def test_valid_message_form(self):
        """Test un formulaire de message valide"""
        form = MessageForm({
            'content': 'Test message'
        })
        form.instance.conversation = self.conversation
        form.instance.sender = self.user1
        self.assertTrue(form.is_valid())
    
    def test_message_form_save(self):
        """Test la sauvegarde d'un message"""
        form = MessageForm({
            'content': 'Test message'
        })
        form.instance.conversation = self.conversation
        form.instance.sender = self.user1
        self.assertTrue(form.is_valid())
        message = form.save()
        self.assertEqual(message.content, 'Test message')
        self.assertEqual(message.sender, self.user1)
        self.assertFalse(message.is_read)
    
    def test_message_form_empty_content(self):
        """Test un message avec contenu vide"""
        form = MessageForm({
            'content': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)


class PaymentFormTest(TestCase):
    """Tests pour le formulaire PaymentForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
    
    def test_valid_payment_form(self):
        """Test un formulaire de paiement valide"""
        form = PaymentForm({
            'amount': 99.99,
            'payment_type': 'course',
            'status': 'pending'
        })
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
    
    def test_payment_form_save(self):
        """Test la sauvegarde d'un paiement"""
        form = PaymentForm({
            'amount': 99.99,
            'payment_type': 'course',
            'status': 'completed'
        })
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
        payment = form.save()
        self.assertEqual(payment.amount, 99.99)
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.status, 'completed')
    
    def test_payment_form_negative_amount(self):
        """Test un montant négatif"""
        form = PaymentForm({
            'amount': -10,
            'payment_type': 'course'
        })
        self.assertFalse(form.is_valid())

