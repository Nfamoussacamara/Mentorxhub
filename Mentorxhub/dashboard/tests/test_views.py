"""
Tests unitaires pour les vues du dashboard
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from dashboard.models import (
    UserProfile, Conversation, Message, Course, Lesson, CourseProgress,
    Payment, SupportTicket, Notification
)

User = get_user_model()


class DashboardViewTest(TestCase):
    """Tests pour la vue dashboard"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.login(email='test@example.com', password='testpass123')
    
    def test_dashboard_requires_login(self):
        """Test que le dashboard nécessite une connexion"""
        self.client.logout()
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_dashboard_mentor_view(self):
        """Test la vue dashboard pour un mentor"""
        self.user.role = 'mentor'
        self.user.save()
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
    
    def test_dashboard_student_view(self):
        """Test la vue dashboard pour un étudiant"""
        self.user.role = 'student'
        self.user.save()
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
    
    def test_dashboard_ajax_request(self):
        """Test la vue dashboard en AJAX"""
        response = self.client.get(
            reverse('dashboard:dashboard'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        # Vérifier que c'est une réponse JSON ou HTML fragment
        self.assertIn(response['Content-Type'], ['application/json', 'text/html; charset=utf-8'])


class ProfileViewTest(TestCase):
    """Tests pour les vues de profil"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.login(email='test@example.com', password='testpass123')
    
    def test_profile_view(self):
        """Test la vue de profil"""
        response = self.client.get(reverse('dashboard:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profil')
    
    def test_profile_edit(self):
        """Test l'édition du profil"""
        response = self.client.post(
            reverse('dashboard:profile_edit'),
            {
                'bio': 'New bio',
                'location': 'Paris, France',
                'phone': '+33123456789'
            }
        )
        self.assertEqual(response.status_code, 200)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.bio, 'New bio')
    
    def test_profile_avatar_upload(self):
        """Test l'upload d'un avatar"""
        image = SimpleUploadedFile(
            "avatar.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        response = self.client.post(
            reverse('dashboard:profile_edit'),
            {'avatar': image}
        )
        self.assertEqual(response.status_code, 200)
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsNotNone(profile.avatar)


class MessagesViewTest(TestCase):
    """Tests pour les vues de messagerie"""
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='testpass123'
        )
        self.client.login(email='user1@example.com', password='testpass123')
        self.conversation = Conversation.objects.create(
            participant1=self.user1,
            participant2=self.user2
        )
    
    def test_messages_list_view(self):
        """Test la liste des conversations"""
        response = self.client.get(reverse('dashboard:messages_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Messages')
    
    def test_conversation_view(self):
        """Test la vue d'une conversation"""
        response = self.client.get(
            reverse('dashboard:conversation', args=[self.conversation.id])
        )
        self.assertEqual(response.status_code, 200)
    
    def test_send_message(self):
        """Test l'envoi d'un message"""
        response = self.client.post(
            reverse('dashboard:send_message', args=[self.conversation.id]),
            {'content': 'Test message'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        message = Message.objects.filter(conversation=self.conversation).first()
        self.assertIsNotNone(message)
        self.assertEqual(message.content, 'Test message')
    
    def test_unread_count(self):
        """Test le compteur de messages non lus"""
        Message.objects.create(
            conversation=self.conversation,
            sender=self.user2,
            content='Unread message',
            is_read=False
        )
        response = self.client.get(
            reverse('dashboard:messages_unread_count'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('unread_count', response.json())


class CoursesViewTest(TestCase):
    """Tests pour les vues de cours"""
    
    def setUp(self):
        self.client = Client()
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
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            content='Test content',
            order=1
        )
        self.client.login(email='student@example.com', password='testpass123')
    
    def test_courses_list_view(self):
        """Test la liste des cours"""
        response = self.client.get(reverse('dashboard:courses_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cours')
    
    def test_course_detail_view(self):
        """Test les détails d'un cours"""
        response = self.client.get(
            reverse('dashboard:course_detail', args=[self.course.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.title)
    
    def test_complete_lesson(self):
        """Test la complétion d'une leçon"""
        progress = CourseProgress.objects.create(
            student=self.student,
            course=self.course
        )
        response = self.client.post(
            reverse('dashboard:complete_lesson', args=[self.course.id, self.lesson.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        # Vérifier que la progression a été mise à jour
        progress.refresh_from_db()
        self.assertGreater(progress.completion_percentage, 0)


class PaymentsViewTest(TestCase):
    """Tests pour les vues de paiements"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.login(email='user@example.com', password='testpass123')
        self.payment = Payment.objects.create(
            user=self.user,
            amount=99.99,
            payment_type='course',
            status='completed'
        )
    
    def test_payments_list_view(self):
        """Test la liste des paiements"""
        response = self.client.get(reverse('dashboard:payments_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Paiements')
    
    def test_payment_invoice_download(self):
        """Test le téléchargement d'une facture"""
        response = self.client.get(
            reverse('dashboard:payment_invoice', args=[self.payment.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')


class SupportViewTest(TestCase):
    """Tests pour les vues de support"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.login(email='user@example.com', password='testpass123')
        self.ticket = SupportTicket.objects.create(
            user=self.user,
            subject='Test Subject',
            description='Test description'
        )
    
    def test_support_tickets_list(self):
        """Test la liste des tickets"""
        response = self.client.get(reverse('dashboard:support_tickets_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Support')
    
    def test_create_ticket(self):
        """Test la création d'un ticket"""
        response = self.client.post(
            reverse('dashboard:support_create_ticket'),
            {
                'subject': 'New Ticket',
                'description': 'New description',
                'priority': 'high'
            }
        )
        self.assertEqual(response.status_code, 200)
        ticket = SupportTicket.objects.filter(subject='New Ticket').first()
        self.assertIsNotNone(ticket)
    
    def test_ticket_reply(self):
        """Test l'envoi d'une réponse à un ticket"""
        response = self.client.post(
            reverse('dashboard:support_ticket_reply', args=[self.ticket.id]),
            {'content': 'Test reply'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        from dashboard.models import TicketReply
        reply = TicketReply.objects.filter(ticket=self.ticket).first()
        self.assertIsNotNone(reply)
        self.assertEqual(reply.content, 'Test reply')
    
    def test_close_ticket(self):
        """Test la fermeture d'un ticket"""
        response = self.client.post(
            reverse('dashboard:support_close_ticket', args=[self.ticket.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'closed')


class NotificationsViewTest(TestCase):
    """Tests pour les vues de notifications"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.login(email='user@example.com', password='testpass123')
        self.notification = Notification.objects.create(
            user=self.user,
            notification_type='message',
            title='Test Notification',
            message='Test message',
            is_read=False
        )
    
    def test_notifications_list(self):
        """Test la liste des notifications"""
        response = self.client.get(reverse('dashboard:notifications_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Notifications')
    
    def test_mark_notification_read(self):
        """Test le marquage d'une notification comme lue"""
        response = self.client.post(
            reverse('dashboard:notification_mark_read', args=[self.notification.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
    
    def test_notifications_unread_count(self):
        """Test le compteur de notifications non lues"""
        Notification.objects.create(
            user=self.user,
            notification_type='message',
            title='Another Notification',
            message='Another message',
            is_read=False
        )
        response = self.client.get(
            reverse('dashboard:notifications_unread_count'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(data.get('unread_count', 0), 0)


class AnalyticsViewTest(TestCase):
    """Tests pour les vues d'analytics"""
    
    def setUp(self):
        self.client = Client()
        self.mentor = User.objects.create_user(
            email='mentor@example.com',
            password='testpass123',
            role='mentor'
        )
        self.client.login(email='mentor@example.com', password='testpass123')
    
    def test_analytics_view(self):
        """Test la vue analytics"""
        response = self.client.get(reverse('dashboard:analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Analytics')
    
    def test_analytics_data_ajax(self):
        """Test les données analytics en AJAX"""
        response = self.client.get(
            reverse('dashboard:analytics_data'),
            {'period': '7d'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('labels', data)
        self.assertIn('sessions_data', data)


class SessionsViewTest(TestCase):
    """Tests pour les vues de sessions"""
    
    def setUp(self):
        self.client = Client()
        self.mentor = User.objects.create_user(
            email='mentor@example.com',
            password='testpass123',
            role='mentor'
        )
        self.client.login(email='mentor@example.com', password='testpass123')
    
    def test_sessions_view(self):
        """Test la vue des sessions"""
        response = self.client.get(reverse('dashboard:sessions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sessions')
    
    def test_sessions_events_ajax(self):
        """Test les événements de sessions en AJAX"""
        response = self.client.get(
            reverse('dashboard:sessions_events'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        # Vérifier que c'est du JSON
        self.assertEqual(response['Content-Type'], 'application/json')

