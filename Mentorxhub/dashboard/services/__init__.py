"""
Service Layer pour le module Dashboard
Contient la logique métier pure, indépendante des vues HTTP
"""
from .overview_service import get_mentor_stats, get_student_stats

__all__ = ['get_mentor_stats', 'get_student_stats']
