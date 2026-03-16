# Documentation - Système de Signals

## 📡 Vue d'Ensemble

Le projet MentorXHub utilise le système de **signals** de Django pour automatiser la création des profils utilisateurs (Student/Mentor) lors de l'inscription.

---

## 🎯 Objectif

**Problème :** Quand un utilisateur s'inscrit, il doit avoir un profil correspondant à son rôle (StudentProfile ou MentorProfile).

**Solution :** Les signals Django créent **automatiquement** le profil approprié dès qu'un utilisateur est créé.

---

## 📂 Structure des Fichiers

```
accounts/
├── models.py          # CustomUser avec champ 'role'
├── signals.py         # ⚡ Création automatique des profils
└── apps.py            # Activation des signals

mentoring/
└── models.py          # StudentProfile et MentorProfile
```

---

## 📝 Code du Signal

### Fichier : `accounts/signals.py`

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser
from mentoring.models import StudentProfile, MentorProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal qui crée automatiquement un profil Student ou Mentor
    quand un nouvel utilisateur est créé.
    
    Args:
        sender: Le modèle qui envoie le signal (CustomUser)
        instance: L'instance de l'utilisateur créé
        created: Boolean - True si création, False si modification
        **kwargs: Arguments supplémentaires
    """
    if created:
        if instance.role == 'student':
            StudentProfile.objects.create(user=instance)
        elif instance.role == 'mentor':
            MentorProfile.objects.create(user=instance)
```

---

## 🔄 Flux d'Exécution

### Diagramme de Séquence

```
┌─────────┐         ┌─────────┐         ┌────────┐         ┌─────────┐
│  Vue    │         │ Django  │         │ Signal │         │  Model  │
│ Signup  │         │  ORM    │         │ post_  │         │ Profile │
│         │         │         │         │ save   │         │         │
└────┬────┘         └────┬────┘         └───┬────┘         └────┬────┘
     │                   │                  │                   │
     │ 1. create_user()  │                  │                   │
     │──────────────────>│                  │                   │
     │                   │                  │                   │
     │                   │ 2. Sauvegarde    │                   │
     │                   │      en DB       │                   │
     │                   │──────────────────│                   │
     │                   │                  │                   │
     │                   │  3. post_save ⚡ │                   │
     │                   │──────────────────>│                  │
     │                   │                  │                   │
     │                   │                  │ 4. Vérifie role   │
     │                   │                  │   created=True    │
     │                   │                  │                   │
     │                   │                  │ 5. create()       │
     │                   │                  │──────────────────>│
     │                   │                  │                   │
     │                   │                  │ 6. Profile créé ✅│
     │                   │                  │<──────────────────│
     │                   │                  │                   │
     │ 7. User + Profile │                  │                   │
     │<──────────────────│                  │                   │
     │    créés          │                  │                   │
     │                   │                  │                   │
```

---

## 💡 Exemples d'Utilisation

### Exemple 1 : Inscription d'un Étudiant

```python
# Dans accounts/views.py
from .models import CustomUser

def signup_view(request):
    # Création de l'utilisateur
    user = CustomUser.objects.create_user(
        email='etudiant@example.com',
        username='etudiant123',
        password='password123',
        role='student'  # ← Définit le rôle
    )
    
    # ⚡ AUTOMATIQUE : StudentProfile créé par le signal
    # Pas besoin de faire :
    # StudentProfile.objects.create(user=user)
    
    # Le profil existe déjà !
    print(user.student_profile)  # ✅ Fonctionne
    print(user.student_profile.bio)  # ✅ Accessible
```

**Résultat en base de données :**

```sql
-- Table accounts_customuser
INSERT INTO accounts_customuser (email, username, role)
VALUES ('etudiant@example.com', 'etudiant123', 'student');

-- Table mentoring_studentprofile (créée automatiquement ⚡)
INSERT INTO mentoring_studentprofile (user_id, bio, ville, techno)
VALUES (1, '', '', '');
```

---

### Exemple 2 : Inscription d'un Mentor

```python
# Création d'un mentor
user = CustomUser.objects.create_user(
    email='mentor@example.com',
    username='mentor456',
    password='password123',
    role='mentor'  # ← Définit le rôle
)

# ⚡ AUTOMATIQUE : MentorProfile créé par le signal
print(user.mentor_profile)  # ✅ Fonctionne
print(user.mentor_profile.speciality)  # ✅ Accessible
```

---

### Exemple 3 : Modification (Signal ne crée rien)

```python
# Modification d'un utilisateur existant
user = CustomUser.objects.get(email='etudiant@example.com')
user.first_name = 'Jean'
user.save()

# ⚡ Signal déclenché MAIS created=False
# → Aucun profil n'est créé (car déjà existant)
```

---

## 🔗 Relations entre Modèles

### CustomUser (accounts/models.py)

```python
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('mentor', 'Mentor'),
        ('student', 'Étudiant'),
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # ... autres champs
```

### StudentProfile (mentoring/models.py)

```python
class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_profile'  # ← user.student_profile
    )
    bio = models.TextField(blank=True)
    ville = models.CharField(max_length=100, blank=True)
    techno = models.CharField(max_length=200, blank=True)
```

### MentorProfile (mentoring/models.py)

```python
class MentorProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='mentor_profile'  # ← user.mentor_profile
    )
    speciality = models.CharField(max_length=200)
    bio = models.TextField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    # ... autres champs
```

---

## ⚙️ Activation des Signals

### Fichier : `accounts/apps.py`

```python
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    def ready(self):
        """
        Méthode appelée au démarrage de Django.
        Import les signals pour les activer.
        """
        import accounts.signals  # ⚡ Active les signals
```

**Important :** Sans cette ligne, les signals ne fonctionneront pas !

---

## 🧪 Tests

### Test de Création Automatique

```python
# tests/test_signals.py
from django.test import TestCase
from accounts.models import CustomUser
from mentoring.models import StudentProfile, MentorProfile

class SignalTestCase(TestCase):
    
    def test_student_profile_created_automatically(self):
        """Vérifie qu'un StudentProfile est créé automatiquement"""
        # Création d'un utilisateur étudiant
        user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass',
            role='student'
        )
        
        # Vérifie que le profil existe
        self.assertTrue(hasattr(user, 'student_profile'))
        self.assertIsInstance(user.student_profile, StudentProfile)
    
    def test_mentor_profile_created_automatically(self):
        """Vérifie qu'un MentorProfile est créé automatiquement"""
        # Création d'un utilisateur mentor
        user = CustomUser.objects.create_user(
            email='mentor@example.com',
            username='mentoruser',
            password='testpass',
            role='mentor'
        )
        
        # Vérifie que le profil existe
        self.assertTrue(hasattr(user, 'mentor_profile'))
        self.assertIsInstance(user.mentor_profile, MentorProfile)
    
    def test_profile_not_created_on_update(self):
        """Vérifie qu'aucun profil n'est créé lors d'une modification"""
        # Création initiale
        user = CustomUser.objects.create_user(
            email='test2@example.com',
            username='testuser2',
            password='testpass',
            role='student'
        )
        
        initial_profile_id = user.student_profile.id
        
        # Modification de l'utilisateur
        user.first_name = 'Jean'
        user.save()
        
        # Vérifie que c'est toujours le même profil
        self.assertEqual(user.student_profile.id, initial_profile_id)
```

---

## 🐛 Débogage

### Vérifier si les Signals sont Actifs

```python
# Dans le shell Django
python manage.py shell

>>> from django.db.models.signals import post_save
>>> from accounts.models import CustomUser
>>> 
>>> # Liste tous les receivers pour post_save sur CustomUser
>>> receivers = post_save._live_receivers(CustomUser)
>>> print(receivers)
# Devrait afficher create_user_profile
```

### Problèmes Courants

#### 1. Le profil n'est pas créé

**Cause :** Les signals ne sont pas activés

**Solution :** Vérifier `accounts/apps.py` :
```python
def ready(self):
    import accounts.signals  # Cette ligne doit exister
```

#### 2. Erreur "RelatedObjectDoesNotExist"

**Cause :** Tentative d'accès au profil avant sa création

**Solution :** Toujours vérifier avec `hasattr()` :
```python
if hasattr(user, 'student_profile'):
    print(user.student_profile.bio)
```

#### 3. Profils en double

**Cause :** Signal déclenché plusieurs fois

**Solution :** Le `if created:` empêche normalement cela. Vérifier les migrations.

---

## 📊 Schéma de Base de Données

```
┌─────────────────────────┐
│   CustomUser            │
├─────────────────────────┤
│ id (PK)                 │
│ email (unique)          │
│ username                │
│ password                │
│ role ('student'/'mentor')│
│ created_at              │
│ updated_at              │
└───────────┬─────────────┘
            │
            │ OneToOne
            │
    ┌───────┴────────┐
    │                │
    ▼                ▼
┌─────────────┐  ┌─────────────┐
│Student      │  │Mentor       │
│Profile      │  │Profile      │
├─────────────┤  ├─────────────┤
│id (PK)      │  │id (PK)      │
│user_id (FK) │  │user_id (FK) │
│bio          │  │speciality   │
│ville        │  │bio          │
│techno       │  │hourly_rate  │
└─────────────┘  └─────────────┘
```

---

## ✅ Avantages du Système

1. **Automatique** : Aucun code manuel dans les vues
2. **Fiable** : Impossible d'oublier de créer le profil
3. **Centralisé** : Toute la logique au même endroit
4. **Maintenable** : Facile à modifier
5. **Testable** : Tests unitaires simples

---

## 🚀 Utilisation dans les Vues

Après l'inscription, vous pouvez accéder directement au profil :

```python
# Dans dashboard view
@login_required
def dashboard(request):
    user = request.user
    
    if user.role == 'mentor':
        # Accès direct au profil mentor
        profile = user.mentor_profile
        return render(request, 'dashboard-mentor.html', {
            'profile': profile,
            'sessions': profile.mentoring_sessions.all()
        })
    
    elif user.role == 'student':
        # Accès direct au profil étudiant
        profile = user.student_profile
        return render(request, 'dashboard-student.html', {
            'profile': profile,
            'sessions': profile.student_sessions.all()
        })
```

---

## 📚 Références Django

- [Django Signals Documentation](https://docs.djangoproject.com/en/5.0/topics/signals/)
- [post_save Signal](https://docs.djangoproject.com/en/5.0/ref/signals/#post-save)
- [receiver Decorator](https://docs.djangoproject.com/en/5.0/topics/signals/#receiver-functions)

---

## 📝 Changelog

- **2025-12-06** : Création du système de signals automatique
- **2025-12-06** : Documentation complète ajoutée

---

**Auteur :** Équipe MentorXHub  
**Dernière mise à jour :** 6 décembre 2025
