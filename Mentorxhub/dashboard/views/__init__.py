"""
Vues du dashboard MentorXHub
"""
from .dashboard import dashboard, mentor_dashboard, student_dashboard
from . import profile
from . import notifications
from . import analytics
from . import sessions
from . import settings
from . import messages
from . import courses
from . import payments
from . import support

# Exporter pour compatibilité
__all__ = [
    'dashboard', 'mentor_dashboard', 'student_dashboard',
    'profile', 'notifications', 'analytics', 'sessions', 'settings',
    'messages', 'courses', 'payments', 'support'
]

