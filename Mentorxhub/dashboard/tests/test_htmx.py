"""
Tests unitaires pour les fonctionnalités HTMX du dashboard
Vérifie que les fragments HTMX sont correctement retournés et fonctionnent
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.loader import render_to_string
from dashboard.models import Conversation, Message, Notification, Course, Payment, SupportTicket
import json

User = get_user_model()


class HtmxFragmentTest(TestCase):
    """Tests pour les fragments HTMX"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='mentor'
        )
        self.client.login(email='test@example.com', password='testpass123')
        self.htmx_headers = {'HTTP_HX-Request': 'true'}
    
    def test_dashboard_overview_fragment(self):
        """Test que le fragment overview_dashboard est retourné correctement"""
        response = self.client.get(
            reverse('dashboard:dashboard'),
            **self.htmx_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('welcome-section', response.content.decode())
        self.assertIn('stats-cards', response.content.decode())
    
    def test_messages_list_panel_fragment(self):
        """Test que le fragment messages_list_panel est retourné"""
        # Créer une conversation de test
        other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        conversation = Conversation.objects.create(subject='Test')
        conversation.participants.add(self.user, other_user)
        
        response = self.client.get(
            reverse('dashboard:messages_list'),
            **self.htmx_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('messages-list-panel', response.content.decode())
    
    def test_messages_chat_panel_fragment(self):
        """Test que le fragment messages_chat_panel est retourné"""
        # Créer une conversation avec messages
        other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        conversation = Conversation.objects.create(subject='Test')
        conversation.participants.add(self.user, other_user)
        Message.objects.create(
            conversation=conversation,
            sender=self.user,
            content='Test message'
        )
        
        response = self.client.get(
            reverse('dashboard:conversation_detail', args=[conversation.id]),
            **self.htmx_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('messages-chat-panel', response.content.decode())
        self.assertIn('Test message', response.content.decode())
    
    def test_send_message_htmx(self):
        """Test l'envoi de message via HTMX"""
        other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        conversation = Conversation.objects.create(subject='Test')
        conversation.participants.add(self.user, other_user)
        
        response = self.client.post(
            reverse('dashboard:message_send', args=[conversation.id]),
            {'content': 'Hello HTMX!'},
            **self.htmx_headers
        )
        self.assertEqual(response.status_code, 200)
        # Vérifier que le message a été créé
        self.assertTrue(Message.objects.filter(content='Hello HTMX!').exists())
    
    def test_notifications_list_fragment(self):
        """Test que le fragment notifications_list est retourné"""
        # Créer une notification
        Notification.objects.create(
            user=self.user,
            title='Test Notification',
            message='Test message',
            notification_type='info'
        )
        
        response = self.client.get(
            reverse('dashboard:notifications'),
            **self.htmx_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Notification', response.content.decode())
    
    def test_courses_list_fragment(self):
        """Test que le fragment courses_list est retourné"""
        # Créer un cours
        Course.objects.create(
            title='Test Course',
            description='Test description',
            instructor=self.user,
            price=99.99
        )
        
        response = self.client.get(
            reverse('dashboard:courses_list'),
            **self.htmx_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Course', response.content.decode())
    
    def test_payments_list_fragment(self):
        """Test que le fragment payments_list est retourné"""
        # Créer un paiement
        Payment.objects.create(
            user=self.user,
            amount=100.00,
            payment_method='card',
            status='completed'
        )
        
        response = self.client.get(
            reverse('dashboard:payments_list'),
            **self.htmx_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('100.00', response.content.decode())
    
    def test_support_tickets_list_fragment(self):
        """Test que le fragment support_tickets_list est retourné"""
        # Créer un ticket
        SupportTicket.objects.create(
            user=self.user,
            subject='Test Ticket',
            message='Test message',
            status='open'
        )
        
        response = self.client.get(
            reverse('dashboard:support_tickets_list'),
            **self.htmx_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Ticket', response.content.decode())


class HtmxAttributesTest(TestCase):
    """Tests pour vérifier que les attributs HTMX sont présents dans les templates"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='mentor'
        )
        self.client.login(email='test@example.com', password='testpass123')
    
    def test_base_template_has_hx_boost(self):
        """Test que base.html a l'attribut hx-boost"""
        response = self.client.get(reverse('dashboard:dashboard'))
        content = response.content.decode()
        self.assertIn('hx-boost="true"', content)
        self.assertIn('hx-target="this"', content)
        self.assertIn('hx-swap="innerHTML"', content)
    
    def test_overview_dashboard_has_htmx_polling(self):
        """Test que overview_dashboard a le polling HTMX"""
        response = self.client.get(reverse('dashboard:dashboard'))
        content = response.content.decode()
        # Vérifier que le polling est présent
        self.assertIn('hx-get', content)
        self.assertIn('hx-trigger="every 60s"', content)
    
    def test_messages_chat_has_htmx_form(self):
        """Test que messages_chat_panel a le formulaire HTMX"""
        other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        conversation = Conversation.objects.create(subject='Test')
        conversation.participants.add(self.user, other_user)
        
        response = self.client.get(
            reverse('dashboard:conversation_detail', args=[conversation.id])
        )
        content = response.content.decode()
        self.assertIn('hx-post', content)
        self.assertIn('hx-target', content)
        self.assertIn('hx-swap', content)
    
    def test_messages_chat_has_htmx_polling(self):
        """Test que messages_chat_panel a le polling HTMX pour nouveaux messages"""
        other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        conversation = Conversation.objects.create(subject='Test')
        conversation.participants.add(self.user, other_user)
        
        response = self.client.get(
            reverse('dashboard:conversation_detail', args=[conversation.id])
        )
        content = response.content.decode()
        # Vérifier le polling pour nouveaux messages
        self.assertIn('hx-trigger="every 5s"', content)
        self.assertIn('messages_poll', content)


class HtmxResponseTest(TestCase):
    """Tests pour vérifier les réponses HTMX"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='mentor'
        )
        self.client.login(email='test@example.com', password='testpass123')
        self.htmx_headers = {'HTTP_HX-Request': 'true'}
    
    def test_htmx_response_is_html_fragment(self):
        """Test que les réponses HTMX sont des fragments HTML, pas du JSON"""
        response = self.client.get(
            reverse('dashboard:dashboard'),
            **self.htmx_headers
        )
        self.assertEqual(response.status_code, 200)
        # Vérifier que c'est du HTML, pas du JSON
        content = response.content.decode()
        self.assertIn('<div', content)
        self.assertNotIn('"html"', content)  # Pas de JSON avec propriété html
    
    def test_htmx_response_has_correct_content_type(self):
        """Test que les réponses HTMX ont le bon Content-Type"""
        response = self.client.get(
            reverse('dashboard:dashboard'),
            **self.htmx_headers
        )
        self.assertEqual(response.status_code, 200)
        # Django retourne text/html par défaut pour les templates
        self.assertIn('text/html', response.get('Content-Type', ''))
    
    def test_htmx_error_handling(self):
        """Test la gestion des erreurs HTMX"""
        # Tester avec une URL invalide
        response = self.client.get(
            '/dashboard/messages/invalid-uuid/',
            **self.htmx_headers
        )
        # Devrait retourner une erreur 404 ou un message d'erreur
        self.assertIn(response.status_code, [404, 400])


class HtmxPerformanceTest(TestCase):
    """Tests pour vérifier les performances des fragments HTMX"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='mentor'
        )
        self.client.login(email='test@example.com', password='testpass123')
        self.htmx_headers = {'HTTP_HX-Request': 'true'}
    
    def test_fragment_size_is_reasonable(self):
        """Test que les fragments HTMX ne sont pas trop volumineux"""
        response = self.client.get(
            reverse('dashboard:dashboard'),
            **self.htmx_headers
        )
        content_length = len(response.content)
        # Les fragments ne devraient pas dépasser 100KB
        self.assertLess(content_length, 100000, 
                       f"Fragment trop volumineux: {content_length} bytes")
    
    def test_fragment_rendering_time(self):
        """Test que les fragments se rendent rapidement"""
        import time
        start = time.time()
        response = self.client.get(
            reverse('dashboard:dashboard'),
            **self.htmx_headers
        )
        elapsed = time.time() - start
        # Le rendu ne devrait pas prendre plus de 1 seconde
        self.assertLess(elapsed, 1.0, 
                       f"Rendu trop lent: {elapsed:.2f} secondes")
        self.assertEqual(response.status_code, 200)

