# Importer toutes les vues depuis le fichier views original
# Pour maintenir la compatibilité avec urls.py
from .main import *
from .onboarding.mentee import MenteeOnboardingView, SkipMenteeOnboardingView
from .onboarding.mentor import MentorOnboardingView
