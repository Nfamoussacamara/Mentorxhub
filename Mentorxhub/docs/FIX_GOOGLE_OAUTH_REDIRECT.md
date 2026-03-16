# 🔧 Fix : Redirection vers Google Workspace au lieu d'OAuth

## 🐛 Problème

Quand vous cliquez sur "Connexion avec Google", vous êtes redirigé vers :
```
https://workspace.google.com/u/3/checkout/plan?snip=x
```

Au lieu de la page d'authentification OAuth normale de Google.

---

## 🔍 Causes Possibles

1. **Credentials OAuth non configurés** dans Django Admin
2. **Client ID ou Secret incorrect** dans Google Cloud Console
3. **URLs de redirection non autorisées** dans Google Cloud Console
4. **Application OAuth mal configurée** dans Google Cloud Console

---

## ✅ Solution Étape par Étape

### Étape 1 : Vérifier la Configuration dans Django Admin

1. **Accédez à Django Admin** : `http://127.0.0.1:8000/admin/`

2. **Allez dans "Social Applications"** :
   - Menu : `Sites` → `Social applications`
   - Ou directement : `http://127.0.0.1:8000/admin/socialaccount/socialapp/`

3. **Vérifiez qu'une application Google existe** :
   - Si elle n'existe pas → Créez-en une (voir Étape 2)
   - Si elle existe → Vérifiez les credentials (voir Étape 3)

---

### Étape 2 : Créer/Configurer l'Application OAuth dans Django Admin

1. **Cliquez sur "Add Social application"**

2. **Remplissez le formulaire** :
   - **Provider** : `Google`
   - **Name** : `MentorXHub Google OAuth` (ou un nom de votre choix)
   - **Client id** : (à obtenir dans Google Cloud Console - voir Étape 4)
   - **Secret key** : (à obtenir dans Google Cloud Console - voir Étape 4)
   - **Key** : (laissez vide)

3. **Sites** :
   - Sélectionnez le site dans la liste de droite (généralement `example.com` ou `127.0.0.1:8000`)
   - Cliquez sur la flèche `>` pour l'ajouter à "Chosen sites"

4. **Cliquez sur "Save"**

---

### Étape 3 : Vérifier/Créer les Credentials dans Google Cloud Console

#### 3.1 Accéder à Google Cloud Console

1. Allez sur : https://console.cloud.google.com/
2. Connectez-vous avec votre compte Google
3. Sélectionnez votre projet (ou créez-en un nouveau)

#### 3.2 Activer l'API Google+

1. Dans le menu hamburger (☰), allez dans **"APIs & Services"** → **"Library"**
2. Recherchez **"Google+ API"** ou **"Google Identity"**
3. Cliquez dessus et cliquez sur **"Enable"**

#### 3.3 Créer les Credentials OAuth 2.0

1. Allez dans **"APIs & Services"** → **"Credentials"**
2. Cliquez sur **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**

3. **Si c'est la première fois** :
   - Configurez l'écran de consentement OAuth :
     - **User Type** : `External` (pour développement) ou `Internal` (pour G Suite)
     - **App name** : `MentorXHub`
     - **User support email** : Votre email
     - **Developer contact information** : Votre email
     - Cliquez sur **"Save and Continue"**
     - **Scopes** : Cliquez sur **"Save and Continue"** (pas besoin de modifier)
     - **Test users** : Ajoutez votre email si nécessaire
     - Cliquez sur **"Save and Continue"**

4. **Créer l'OAuth Client ID** :
   - **Application type** : `Web application`
   - **Name** : `MentorXHub Web Client`
   - **Authorized JavaScript origins** :
     ```
     http://127.0.0.1:8000
     http://localhost:8000
     ```
   - **Authorized redirect URIs** :
     ```
     http://127.0.0.1:8000/accounts/google/login/callback/
     http://localhost:8000/accounts/google/login/callback/
     ```
   - **Pour la production**, ajoutez aussi :
     ```
     https://votre-domaine.com/accounts/google/login/callback/
     ```

5. **Cliquez sur "Create"**

6. **Copiez les credentials** :
   - **Client ID** : `xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com`
   - **Client secret** : `GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

### Étape 4 : Mettre à Jour Django Admin avec les Credentials

1. **Retournez à Django Admin** : `http://127.0.0.1:8000/admin/socialaccount/socialapp/`

2. **Modifiez l'application Google** (ou créez-en une nouvelle) :
   - **Client id** : Collez le **Client ID** copié
   - **Secret key** : Collez le **Client secret** copié

3. **Vérifiez que le site est bien sélectionné** dans "Chosen sites"

4. **Cliquez sur "Save"**

---

### Étape 5 : Vérifier la Configuration dans settings.py

Vérifiez que `settings.py` contient bien :

```python
# Dans INSTALLED_APPS
'django.contrib.sites',
'allauth',
'allauth.account',
'allauth.socialaccount',
'allauth.socialaccount.providers.google',

# SITE_ID
SITE_ID = 2  # Vérifiez que c'est le bon ID (voir Étape 6)

# AUTHENTICATION_BACKENDS
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configuration OAuth
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
```

---

### Étape 6 : Vérifier le SITE_ID

Le `SITE_ID` dans `settings.py` doit correspondre au site dans Django Admin.

1. **Allez dans Django Admin** : `http://127.0.0.1:8000/admin/sites/site/`

2. **Vérifiez le site** :
   - Il devrait y avoir un site avec `Domain name` = `example.com` ou `127.0.0.1:8000`
   - Notez l'**ID** de ce site (généralement `1` ou `2`)

3. **Vérifiez dans `settings.py`** :
   ```python
   SITE_ID = 2  # Remplacez par l'ID de votre site
   ```

4. **Si le site n'existe pas**, créez-en un :
   - Cliquez sur "Add Site"
   - **Domain name** : `127.0.0.1:8000` (pour développement)
   - **Display name** : `MentorXHub`
   - Cliquez sur "Save"

---

### Étape 7 : Vérifier les URLs

Vérifiez que `mentorxhub/urls.py` contient :

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('mentoring/', include('mentoring.urls')),
    path('dashboard/', include('dashboard.urls')),
    
    # URLs django-allauth (IMPORTANT : après accounts.urls)
    path('accounts/', include('allauth.urls')),
]
```

**Important** : `allauth.urls` doit être **après** `accounts.urls` pour éviter les conflits.

---

### Étape 8 : Tester la Connexion

1. **Redémarrez le serveur Django** :
   ```bash
   python manage.py runserver
   ```

2. **Allez sur la page de connexion** : `http://127.0.0.1:8000/accounts/login/`

3. **Cliquez sur "Connexion avec Google"**

4. **Vous devriez être redirigé vers** :
   ```
   https://accounts.google.com/o/oauth2/v2/auth?...
   ```
   (Page d'authentification Google normale, PAS Google Workspace)

5. **Autorisez l'application**

6. **Vous devriez être redirigé vers** : `/dashboard/`

---

## 🔍 Vérifications Supplémentaires

### Vérifier les Logs Django

Si ça ne fonctionne toujours pas, vérifiez les logs du serveur Django pour voir les erreurs :

```bash
python manage.py runserver
```

Cherchez les erreurs liées à :
- `Invalid client`
- `Redirect URI mismatch`
- `Invalid credentials`

### Vérifier dans Google Cloud Console

1. **Allez dans "APIs & Services"** → **"Credentials"**
2. **Cliquez sur votre OAuth Client ID**
3. **Vérifiez** :
   - ✅ L'API "Google+ API" ou "Google Identity" est activée
   - ✅ Les "Authorized redirect URIs" contiennent bien :
     ```
     http://127.0.0.1:8000/accounts/google/login/callback/
     ```
   - ✅ Les "Authorized JavaScript origins" contiennent bien :
     ```
     http://127.0.0.1:8000
     ```

### Vérifier dans Django Admin

1. **Allez dans "Social Applications"** : `http://127.0.0.1:8000/admin/socialaccount/socialapp/`
2. **Vérifiez** :
   - ✅ Le Provider est bien `Google`
   - ✅ Le Client ID correspond à celui de Google Cloud Console
   - ✅ Le Secret key correspond à celui de Google Cloud Console
   - ✅ Le site est bien dans "Chosen sites"

---

## 🚨 Erreurs Courantes

### Erreur : "Redirect URI mismatch"

**Cause** : L'URL de callback dans Google Cloud Console ne correspond pas à celle utilisée par django-allauth.

**Solution** : Vérifiez que les "Authorized redirect URIs" contiennent exactement :
```
http://127.0.0.1:8000/accounts/google/login/callback/
```

### Erreur : "Invalid client"

**Cause** : Le Client ID ou Secret est incorrect dans Django Admin.

**Solution** : Vérifiez que les credentials dans Django Admin correspondent exactement à ceux de Google Cloud Console.

### Erreur : Redirection vers Google Workspace

**Cause** : Les credentials ne sont pas configurés ou sont incorrects.

**Solution** : Suivez toutes les étapes ci-dessus, en particulier :
- Créer l'application OAuth dans Google Cloud Console
- Configurer l'application dans Django Admin
- Vérifier le SITE_ID

---

## 📝 Checklist de Vérification

- [ ] Application OAuth créée dans Google Cloud Console
- [ ] Client ID et Secret copiés depuis Google Cloud Console
- [ ] Application Google configurée dans Django Admin avec les bons credentials
- [ ] Site sélectionné dans "Chosen sites" de l'application
- [ ] SITE_ID dans settings.py correspond au site dans Django Admin
- [ ] URLs de redirection autorisées dans Google Cloud Console
- [ ] API Google+ ou Google Identity activée dans Google Cloud Console
- [ ] `allauth.urls` inclus dans `urls.py` après `accounts.urls`
- [ ] Serveur Django redémarré

---

## 🎯 Résultat Attendu

Après avoir suivi toutes ces étapes, quand vous cliquez sur "Connexion avec Google" :

1. ✅ Redirection vers `https://accounts.google.com/o/oauth2/v2/auth?...`
2. ✅ Page d'authentification Google normale
3. ✅ Autorisation de l'application
4. ✅ Redirection vers `/dashboard/`
5. ✅ Utilisateur connecté automatiquement

---

## 📚 Références

- **Documentation django-allauth** : https://docs.allauth.org/
- **Google Cloud Console** : https://console.cloud.google.com/
- **Documentation OAuth Google** : https://developers.google.com/identity/protocols/oauth2

---

*Document créé le : 2025-12-11*  
*Statut : ✅ Guide de dépannage complet*

