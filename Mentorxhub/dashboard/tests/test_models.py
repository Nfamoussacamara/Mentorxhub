"""
Tests unitaires pour les modèles du dashboard
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

from dashboard.models import (
    UserProfile, DashboardSettings, Activity, Conversation, Message,
    Course, Lesson, CourseProgress, Payment, SupportTicket, TicketReply,
    Notification
)

User = get_user_model()


class UserProfileModelTest(TestCase):
    """Tests pour le modèle UserProfile"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_user_profile_creation(self):
        """Test la création automatique du profil"""
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.user)
    
    def test_user_profile_str(self):
        """Test la représentation string du profil"""
        profile = UserProfile.objects.get(user=self.user)
        self.assertIn(self.user.email, str(profile))
    
    def test_user_profile_bio(self):
        """Test la bio du profil"""
        profile = UserProfile.objects.get(user=self.user)
        profile.bio = "Test bio"
        profile.save()
        self.assertEqual(profile.bio, "Test bio")
    
    def test_user_profile_location(self):
        """Test la localisation"""
        profile = UserProfile.objects.get(user=self.user)
        profile.location = "Paris, France"
        profile.save()
        self.assertEqual(profile.location, "Paris, France")


class DashboardSettingsModelTest(TestCase):
    """Tests pour le modèle DashboardSettings"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_dashboard_settings_creation(self):
        """Test la création automatique des paramètres"""
        settings = DashboardSettings.objects.get(user=self.user)
        self.assertIsNotNone(settings)
        self.assertEqual(settings.user, self.user)
    
    def test_default_theme(self):
        """Test le thème par défaut"""
        settings = DashboardSettings.objects.get(user=self.user)
        self.assertEqual(settings.theme, 'light')
    
    def test_change_theme(self):
        """Test le changement de thème"""
        settings = DashboardSettings.objects.get(user=self.user)
        settings.theme = 'dark'
        settings.save()
        self.assertEqual(settings.theme, 'dark')


class ActivityModelTest(TestCase):
    """Tests pour le modèle Activity"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_activity(self):
        """Test la création d'une activité"""
        activity = Activity.objects.create(
            user=self.user,
            activity_type='login',
            description='User logged in'
        )
        self.assertIsNotNone(activity)
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'login')
    
    def test_activity_timestamp(self):
        """Test le timestamp automatique"""
        activity = Activity.objects.create(
            user=self.user,
            activity_type='login',
            description='User logged in'
        )
        self.assertIsNotNone(activity.timestamp)
        self.assertIsInstance(activity.timestamp, datetime)


class ConversationModelTest(TestCase):
    """Tests pour le modèle Conversation"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='testpass123'
        )
    
    def test_create_conversation(self):
        """Test la création d'une conversation"""
        conversation = Conversation.objects.create(
            participant1=self.user1,
            participant2=self.user2
        )
        self.assertIsNotNone(conversation)
        self.assertIn(self.user1, [conversation.participant1, conversation.participant2])
        self.assertIn(self.user2, [conversation.participant1, conversation.participant2])
    
    def test_conversation_get_other_participant(self):
        """Test la méthode get_other_participant"""
        conversation = Conversation.objects.create(
            participant1=self.user1,
            participant2=self.user2
        )
        other = conversation.get_other_participant(self.user1)
        self.assertEqual(other, self.user2)
    
    def test_conversation_unread_count(self):
        """Test le compteur de messages non lus"""
        conversation = Conversation.objects.create(
            participant1=self.user1,
            participant2=self.user2
        )
        # Créer des messages non lus
        Message.objects.create(
            conversation=conversation,
            sender=self.user2,
            content='Test message',
            is_read=False
        )
        unread = conversation.get_unread_count(self.user1)
        self.assertEqual(unread, 1)


class MessageModelTest(TestCase):
    """Tests pour le modèle Message"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='testpass123'
        )
        self.conversation = Conversation.objects.create(
            participant1=self.user1,
            participant2=self.user2
        )
    
    def test_create_message(self):
        """Test la création d'un message"""
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='Test message'
        )
        self.assertIsNotNone(message)
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.content, 'Test message')
        self.assertFalse(message.is_read)
    
    def test_message_timestamp(self):
        """Test le timestamp automatique"""
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='Test message'
        )
        self.assertIsNotNone(message.timestamp)
    
    def test_mark_as_read(self):
        """Test le marquage comme lu"""
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='Test message',
            is_read=False
        )
        message.mark_as_read()
        self.assertTrue(message.is_read)


class CourseModelTest(TestCase):
    """Tests pour le modèle Course"""
    
    def setUp(self):
        self.mentor = User.objects.create_user(
            email='mentor@example.com',
            password='testpass123',
            role='mentor'
        )
    
    def test_create_course(self):
        """Test la création d'un cours"""
        course = Course.objects.create(
            title='Test Course',
            description='Test description',
            mentor=self.mentor,
            price=99.99
        )
        self.assertIsNotNone(course)
        self.assertEqual(course.title, 'Test Course')
        self.assertEqual(course.mentor, self.mentor)
    
    def test_course_slug(self):
        """Test la génération automatique du slug"""
        course = Course.objects.create(
            title='Test Course',
            description='Test description',
            mentor=self.mentor
        )
        self.assertEqual(course.slug, 'test-course')
    
    def test_course_status(self):
        """Test le statut par défaut"""
        course = Course.objects.create(
            title='Test Course',
            description='Test description',
            mentor=self.mentor
        )
        self.assertEqual(course.status, 'draft')


class LessonModelTest(TestCase):
    """Tests pour le modèle Lesson"""
    
    def setUp(self):
        self.mentor = User.objects.create_user(
            email='mentor@example.com',
            password='testpass123',
            role='mentor'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test description',
            mentor=self.mentor
        )
    
    def test_create_lesson(self):
        """Test la création d'une leçon"""
        lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            content='Test content',
            order=1
        )
        self.assertIsNotNone(lesson)
        self.assertEqual(lesson.course, self.course)
        self.assertEqual(lesson.order, 1)


class CourseProgressModelTest(TestCase):
    """Tests pour le modèle CourseProgress"""
    
    def setUp(self):
        self.mentor = User.objects.create_user(
            email='mentor@example.com',
            password='testpass123',
            role='mentor'
        )
        self.student = User.objects.create_user(
            email='student@example.com',
            password='testpass123',
            role='student'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test description',
            mentor=self.mentor
        )
    
    def test_create_progress(self):
        """Test la création d'une progression"""
        progress = CourseProgress.objects.create(
            student=self.student,
            course=self.course
        )
        self.assertIsNotNone(progress)
        self.assertEqual(progress.student, self.student)
        self.assertEqual(progress.course, self.course)
        self.assertEqual(progress.completion_percentage, 0)
    
    def test_update_progress(self):
        """Test la mise à jour de la progression"""
        progress = CourseProgress.objects.create(
            student=self.student,
            course=self.course
        )
        progress.completion_percentage = 50
        progress.save()
        self.assertEqual(progress.completion_percentage, 50)


class PaymentModelTest(TestCase):
    """Tests pour le modèle Payment"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
    
    def test_create_payment(self):
        """Test la création d'un paiement"""
        payment = Payment.objects.create(
            user=self.user,
            amount=99.99,
            payment_type='course',
            status='pending'
        )
        self.assertIsNotNone(payment)
        self.assertEqual(payment.amount, 99.99)
        self.assertEqual(payment.status, 'pending')
    
    def test_payment_status_transitions(self):
        """Test les transitions de statut"""
        payment = Payment.objects.create(
            user=self.user,
            amount=99.99,
            payment_type='course',
            status='pending'
        )
        payment.status = 'completed'
        payment.save()
        self.assertEqual(payment.status, 'completed')


class SupportTicketModelTest(TestCase):
    """Tests pour le modèle SupportTicket"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
    
    def test_create_ticket(self):
        """Test la création d'un ticket"""
        ticket = SupportTicket.objects.create(
            user=self.user,
            subject='Test Subject',
            description='Test description',
            priority='medium'
        )
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.subject, 'Test Subject')
        self.assertEqual(ticket.status, 'open')
    
    def test_ticket_priority(self):
        """Test les priorités"""
        ticket = SupportTicket.objects.create(
            user=self.user,
            subject='Test Subject',
            description='Test description',
            priority='high'
        )
        self.assertEqual(ticket.priority, 'high')
    
    def test_close_ticket(self):
        """Test la fermeture d'un ticket"""
        ticket = SupportTicket.objects.create(
            user=self.user,
            subject='Test Subject',
            description='Test description'
        )
        ticket.status = 'closed'
        ticket.save()
        self.assertEqual(ticket.status, 'closed')


class TicketReplyModelTest(TestCase):
    """Tests pour le modèle TicketReply"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.ticket = SupportTicket.objects.create(
            user=self.user,
            subject='Test Subject',
            description='Test description'
        )
    
    def test_create_reply(self):
        """Test la création d'une réponse"""
        reply = TicketReply.objects.create(
            ticket=self.ticket,
            author=self.user,
            content='Test reply'
        )
        self.assertIsNotNone(reply)
        self.assertEqual(reply.ticket, self.ticket)
        self.assertEqual(reply.content, 'Test reply')


class NotificationModelTest(TestCase):
    """Tests pour le modèle Notification"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
    
    def test_create_notification(self):
        """Test la création d'une notification"""
        notification = Notification.objects.create(
            user=self.user,
            notification_type='message',
            title='Test Notification',
            message='Test message'
        )
        self.assertIsNotNone(notification)
        self.assertFalse(notification.is_read)
    
    def test_mark_as_read(self):
        """Test le marquage comme lu"""
        notification = Notification.objects.create(
            user=self.user,
            notification_type='message',
            title='Test Notification',
            message='Test message'
        )
        notification.mark_as_read()
        self.assertTrue(notification.is_read)
    
    def test_unread_count(self):
        """Test le compteur de notifications non lues"""
        Notification.objects.create(
            user=self.user,
            notification_type='message',
            title='Test Notification 1',
            message='Test message',
            is_read=False
        )
        Notification.objects.create(
            user=self.user,
            notification_type='message',
            title='Test Notification 2',
            message='Test message',
            is_read=True
        )
        unread_count = Notification.objects.filter(
            user=self.user,
            is_read=False
        ).count()
        self.assertEqual(unread_count, 1)

