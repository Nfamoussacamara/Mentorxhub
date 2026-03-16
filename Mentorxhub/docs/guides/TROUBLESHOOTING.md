# 🔍 Guide de Dépannage - Application Mentoring

*Documentation de résolution de problèmes et FAQ*

---

## 🎯 Vue d'Ensemble

Ce guide vous aide à résoudre les problèmes courants rencontrés avec l'application `mentoring` de MentorXHub.

---

## 📋 Table des Matières

1. [Problèmes d'Installation](#problèmes-dinstallation)
2. [Erreurs de Base de Données](#erreurs-de-base-de-données)
3. [Problèmes d'Authentification](#problèmes-dauthentification)
4. [Erreurs de Vues et Templates](#erreurs-de-vues-et-templates)
5. [Problèmes de Sessions Vidéo](#problèmes-de-sessions-vidéo)
6. [Problèmes de Notifications](#problèmes-de-notifications)
7. [Erreurs de Formulaires](#erreurs-de-formulaires)
8. [FAQ](#faq)
9. [Debugging Avancé](#debugging-avancé)

---

## 🔧 Problèmes d'Installation

### Erreur : Module 'mentoring' not found

**Symptôme :**
```
ModuleNotFoundError: No module named 'mentoring'
```

**Causes possibles :**
1. L'app n'est pas dans `INSTALLED_APPS`
2. Problème de structure de dossiers

**Solutions :**

**1. Vérifier INSTALLED_APPS :**
```python
# mentorxhub/settings.py
INSTALLED_APPS = [
    # ...
    'mentoring',  # Doit être présent
    # ...
]
```

**2. Vérifier la structure :**
```
Mentorxhub/
├── manage.py
├── mentorxhub/
│   └── settings.py
└── mentoring/
    ├── __init__.py  # Doit exister
    ├── models.py
    └── ...
```

**3. Redémarrer le serveur :**
```bash
# Ctrl+C pour arrêter
python manage.py runserver
```

---

### Erreur : Pillow installation failed

**Symptôme :**
```
ERROR: Could not build wheels for Pillow
```

**Solution (Windows) :**
```bash
# Installer la dernière version de Pillow
pip install --upgrade Pillow

# Sur Python 3.14+
pip install Pillow>=12.0.0
```

**Solution (Linux/Mac) :**
```bash
# Installer les dépendances système
sudo apt-get install python3-dev python3-setuptools
sudo apt-get install libjpeg-dev zlib1g-dev

# Puis installer Pillow
pip install Pillow
```

---

## 💾 Erreurs de Base de Données

### Erreur : no such table: mentoring_mentorprofile

**Symptôme :**
```
sqlite3.OperationalError: no such table: mentoring_mentorprofile
```

**Cause :** Migrations non appliquées.

**Solution :**
```bash
# 1. Créer les migrations
python manage.py makemigrations mentoring

# 2. Appliquer les migrations
python manage.py migrate mentoring

# 3. Vérifier
python manage.py showmigrations mentoring
```

**Résultat attendu :**
```
mentoring
 [X] 0001_initial
 [X] 0002_...
 [X] 0003_...
```

---

### Erreur : UNIQUE constraint failed: mentoring_subject.name

**Symptôme :**
```
IntegrityError: UNIQUE constraint failed: mentoring_subject.name
```

**Cause :** Tentative de créer une matière avec un nom existant.

**Solution 1 (via code) :**
```python
from mentoring.models import Subject

# Utiliser get_or_create au lieu de create
subject, created = Subject.objects.get_or_create(
    name='Python',
    defaults={'description': 'Langage de programmation', 'is_active': True}
)

if created:
    print("Nouvelle matière créée")
else:
    print("Matière existante récupérée")
```

**Solution 2 (via admin) :**
- Vérifiez d'abord si la matière existe
- Modifiez plutôt que créer

---

### Erreur : NOT NULL constraint failed: mentoring_mentorprofile.status

**Symptôme :**
```
IntegrityError: NOT NULL constraint failed: mentoring_mentorprofile.status
```

**Cause :** Création de MentorProfile sans définir le statut.

**Solution :**
```python
# Toujours définir le statut
mentor = MentorProfile.objects.create(
    user=user,
    expertise='Python',
    years_of_experience=5,
    hourly_rate=50.00,
    languages='Français',
    linkedin_profile='https://...',
    status='pending'  # ✅ OBLIGATOIRE
)
```

**Migration de correction (si données existantes) :**
```bash
python manage.py shell
```

```python
from mentoring.models import MentorProfile

# Mettre à jour les profils sans statut
MentorProfile.objects.filter(status__isnull=True).update(status='pending')
```

---

## 🔐 Problèmes d'Authentification

### Erreur : User has no mentor_profile

**Symptôme :**
```
RelatedObjectDoesNotExist: User has no mentor_profile
```

**Cause :** Tentative d'accéder au profil mentor d'un utilisateur qui n'en a pas.

**Solution (dans le code) :**
```python
# ❌ MAUVAIS
mentor_profile = request.user.mentor_profile  # Erreur si n'existe pas

# ✅ BON - Vérifier d'abord
if hasattr(request.user, 'mentor_profile'):
    mentor_profile = request.user.mentor_profile
else:
    # Rediriger vers onboarding ou afficher message
    return redirect('mentoring:mentor_onboarding')

# ✅ BON - Utiliser try/except
try:
    mentor_profile = request.user.mentor_profile
except:
    return redirect('mentoring:mentor_onboarding')
```

**Solution (créer le profil manquant) :**
```python
from mentoring.models import MentorProfile

mentor_profile, created = MentorProfile.objects.get_or_create(
    user=request.user,
    defaults={
        'expertise': '',
        'years_of_experience': 0,
        'hourly_rate': 0,
        'languages': '',
        'status': 'pending'
    }
)
```

---

### Erreur : Permission Denied (403)

**Symptôme :**
```
403 Forbidden
```

**Causes possibles :**
1. Utilisateur non connecté
2. Rôle insuffisant
3. `test_func()` retourne False

**Solution 1 - Vérifier la connexion :**
```python
# Dans la vue
class MyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # URL de redirection
```

**Solution 2 - Vérifier le rôle :**
```python
from django.contrib.auth.mixins import UserPassesTestMixin

class MentorOnlyView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # Vérifier que l'utilisateur a le rôle mentor
        return 'mentor' in self.request.user.role
    
    def handle_no_permission(self):
        # Message personnalisé
        messages.error(self.request, "Vous devez être mentor pour accéder à cette page.")
        return redirect('dashboard:dashboard')
```

**Debugging :**
```python
# Dans le shell
from accounts.models import CustomUser
user = CustomUser.objects.get(email='user@example.com')
print(f"Rôles: {user.role}")
print(f"Mentor profile exists: {hasattr(user, 'mentor_profile')}")
```

---

## 🖼️ Erreurs de Vues et Templates

### Erreur : NoReverseMatch at /mentoring/mentors/

**Symptôme :**
```
django.urls.exceptions.NoReverseMatch: Reverse for 'mentor_detail' not found
```

**Causes possibles :**
1. Nom d'URL incorrect
2. Namespace manquant
3. Paramètres manquants

**Solution 1 - Vérifier le namespace :**
```django
{# ❌ MAUVAIS #}
{% url 'mentor_detail' mentor.id %}

{# ✅ BON #}
{% url 'mentoring:mentor_detail' mentor.id %}
```

**Solution 2 - Vérifier les paramètres :**
```django
{# Si l'URL attend 'pk' #}
{% url 'mentoring:mentor_detail' pk=mentor.id %}

{# Ou en utilisant la position #}
{% url 'mentoring:mentor_detail' mentor.id %}
```

**Solution 3 - Lister toutes les URLs :**
```bash
python manage.py show_urls | grep mentoring
```

---

### Erreur : TemplateDoesNotExist

**Symptôme :**
```
TemplateDoesNotExist at /mentoring/sessions/
mentoring/session_list.html
```

**Causes possibles :**
1. Template dans le mauvais dossier
2. Nom de fichier incorrect
3. App pas dans INSTALLED_APPS

**Solution 1 - Vérifier la structure :**
```
mentoring/
└── templates/
    └── mentoring/  # ✅ Sous-dossier avec le nom de l'app
        └── session_list.html
```

**Solution 2 - Vérifier TEMPLATES dans settings :**
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,  # ✅ Doit être True
        # ...
    },
]
```

**Debugging :**
```python
# Dans la vue, afficher le chemin cherché
from django.template.loader import get_template
try:
    template = get_template('mentoring/session_list.html')
    print(f"Template trouvé: {template.origin.name}")
except:
    print("Template introuvable")
```

---

### Erreur : Variable 'mentor' does not exist

**Symptôme :**
```
TemplateSyntaxError: Could not parse the remainder: '...'
```

**Cause :** Variable non passée au contexte.

**Solution :**
```python
# Dans la vue
class MentorDetailView(DetailView):
    model = MentorProfile
    template_name = 'mentoring/mentor_detail.html'
    context_object_name = 'mentor'  # ✅ Définir le nom
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessions'] = self.object.mentoring_sessions.all()
        return context
```

**Debugging dans le template :**
```django
{# Afficher toutes les variables disponibles #}
<pre>{{ debug }}</pre>

{# Ou #}
{% load static %}
{% debug %}
```

---

## 🎥 Problèmes de Sessions Vidéo

### Erreur : Jitsi ne se charge pas

**Symptôme :** Page blanche ou erreur JavaScript.

**Causes possibles :**
1. Script Jitsi non chargé
2. Bloqueur de publicités
3. Configuration incorrecte

**Solution 1 - Vérifier le script :**
```html
<!-- Dans le template -->
{% block extra_js %}
<script src='https://meet.jit.si/external_api.js'></script>
<script>
    document.addEventListener('DOMContentLoaded', () => {
        // Vérifier que l'API est chargée
        if (typeof JitsiMeetExternalAPI === 'undefined') {
            console.error('Jitsi API non chargée !');
            alert('Erreur de chargement de la visioconférence');
            return;
        }
        
        const api = new JitsiMeetExternalAPI('meet.jit.si', {
            roomName: '{{ room_name }}',
            // ...
        });
    });
</script>
{% endblock %}
```

**Solution 2 - Désactiver les bloqueurs :**
- Demander à l'utilisateur de désactiver AdBlock pour le site

**Solution 3 - Vérifier la console :**
- F12 > Console
- Chercher des erreurs JavaScript

---

### Erreur : "Room name" vide

**Symptôme :** Jitsi se charge mais erreur "Invalid room name".

**Cause :** Variable `room_name` non définie dans le contexte.

**Solution :**
```python
# Dans la vue
class VideoRoomView(DetailView):
    model = MentoringSession
    template_name = 'dashboard/sessions/video_room.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.object
        
        # Générer un nom de salle unique
        import time
        room_name = f"session-{session.id}-{int(time.time())}"
        
        context['room_name'] = room_name
        context['user_name'] = self.request.user.get_full_name()
        return context
```

---

## 🔔 Problèmes de Notifications

### Les notifications ne sont pas envoyées

**Symptôme :** Pas de notification après création/approbation de session.

**Debugging :**

**1. Vérifier que le signal est enregistré :**
```python
# mentoring/apps.py
class MentoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mentoring'
    
    def ready(self):
        import mentoring.signals  # ✅ Import ici
```

**2. Vérifier que le signal se déclenche :**
```python
# mentoring/signals.py
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=MentoringSession)
def notify_session_status_change(sender, instance, created, **kwargs):
    logger.info(f"Signal déclenché pour session {instance.id}")
    
    if created and instance.status == 'pending':
        logger.info(f"Création de notification pour mentor {instance.mentor.user.email}")
        # ...
```

**3. Vérifier les logs :**
```bash
# Dans settings.py, activer le logging
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'mentoring': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

**4. Tester manuellement :**
```python
from mentoring.models import MentoringSession
from dashboard.models import Notification

session = MentoringSession.objects.create(
    mentor=...,
    student=...,
    title="Test",
    # ...
)

# Vérifier les notifications créées
notifications = Notification.objects.filter(user=session.mentor.user)
print(f"{notifications.count()} notification(s)")
```

---

## 📝 Erreurs de Formulaires

### Erreur : "This field is required"

**Symptôme :** Formulaire ne se soumet pas, message d'erreur sur un champ.

**Causes possibles :**
1. Champ obligatoire non rempli
2. Validation personnalisée échoue

**Solution 1 - Rendre un champ optionnel :**
```python
# forms.py
class MyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre le champ optionnel
        self.fields['github_profile'].required = False
```

**Solution 2 - Debugging :**
```python
# Dans la vue
def form_invalid(self, form):
    print("Erreurs de formulaire:")
    for field, errors in form.errors.items():
        print(f"  {field}: {errors}")
    return super().form_invalid(form)
```

---

### Erreur : ValidationError heure de fin < heure de début

**Symptôme :**
```
L'heure de fin doit être après l'heure de début.
```

**Cause :** Validation personnalisée détecte une incohérence.

**Solution :**
```python
# Vérifier les valeurs
from datetime import time

start_time = time(14, 0)  # 14:00
end_time = time(15, 30)    # 15:30

print(f"Début: {start_time}, Fin: {end_time}")
print(f"Valide: {end_time > start_time}")
```

**Dans le formulaire :**
```python
class AvailabilityForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        
        if start and end:
            if start >= end:
                raise forms.ValidationError(
                    f"Incohérence détectée: {start} >= {end}"
                )
        
        return cleaned_data
```

---

## ❓ FAQ

### Q : Comment réinitialiser la base de données ?

**Solution (ATTENTION : Perte de données) :**
```bash
# 1. Supprimer la base de données
rm db.sqlite3

# 2. Supprimer les migrations (sauf __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# 3. Recréer les migrations
python manage.py makemigrations

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer un super-utilisateur
python manage.py createsuperuser
```

---

### Q : Comment accéder au shell Django ?

```bash
# Shell interactif
python manage.py shell

# Importer les modèles
from mentoring.models import MentorProfile, StudentProfile, MentoringSession
from accounts.models import CustomUser

# Exemples de requêtes
mentors = MentorProfile.objects.filter(status='approved')
print(f"{mentors.count()} mentors approuvés")
```

---

### Q : Comment changer le statut d'un mentor ?

```python
python manage.py shell

from mentoring.models import MentorProfile

# Trouver le mentor
mentor = MentorProfile.objects.get(user__email='mentor@example.com')

# Changer le statut
mentor.status = 'approved'
mentor.save()

print(f"Statut changé: {mentor.status}")
```

---

### Q : Comment voir toutes les URLs disponibles ?

```bash
python manage.py show_urls

# Filtrer par app
python manage.py show_urls | grep mentoring

# Ou installer django-extensions
pip install django-extensions

# Puis
python manage.py show_urls
```

---

## 🐛 Debugging Avancé

### Activer le Mode Debug

**settings.py :**
```python
DEBUG = True  # En développement uniquement !
```

**Effet :** Affichage détaillé des erreurs avec traceback.

> [!CAUTION]
> **JAMAIS** en production ! Risque de sécurité.

---

### Django Debug Toolbar

**Installation :**
```bash
pip install django-debug-toolbar
```

**Configuration :**
```python
# settings.py
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]

INTERNAL_IPS = ['127.0.0.1']

# urls.py
from django.urls import include

urlpatterns = [
    # ...
    path('__debug__/', include('debug_toolbar.urls')),
]
```

**Utilisation :**
- Panneau latéral sur chaque page
- SQL queries, templates, contexte, etc.

---

### Logging Personnalisé

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'mentoring': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
    },
}
```

**Dans le code :**
```python
import logging
logger = logging.getLogger('mentoring')

def my_view(request):
    logger.debug("Vue appelée")
    logger.info(f"Utilisateur: {request.user.email}")
    logger.warning("Attention !")
    logger.error("Erreur critique !")
```

---

### Profiling des Requêtes SQL

```python
from django.db import connection
from django.test.utils import override_settings

@override_settings(DEBUG=True)
def my_view(request):
    # Votre code
    mentors = MentorProfile.objects.filter(status='approved')
    
    # Afficher les requêtes SQL
    print(f"{len(connection.queries)} requêtes SQL")
    for query in connection.queries:
        print(query['sql'])
```

---

## 📞 Support

**Si vous ne trouvez pas de solution :**

1. **Consultez les logs :**
   ```bash
   tail -f debug.log
   ```

2. **Cherchez l'erreur sur Stack Overflow :**
   - Copiez le message d'erreur exact
   - Ajoutez "Django" au début

3. **Contactez le support :**
   - Email : dev-support@mentorxhub.com
   - Slack : #mentoring-support
   - GitHub Issues : [lien]

**Informations à fournir :**
- Message d'erreur complet
- Traceback si disponible
- Version de Django (`python -m django --version`)
- Étapes pour reproduire

---

*Guide généré pour MentorXHub - Dépannage Application Mentoring*
