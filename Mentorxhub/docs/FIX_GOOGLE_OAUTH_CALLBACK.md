# 🔧 Fix : Redirection vers Google Workspace après le choix du compte

## 🐛 Problème

Quand vous cliquez sur "Connexion avec Google" :
1. ✅ Vous êtes redirigé vers Google pour choisir un compte (ça fonctionne)
2. ❌ **APRÈS** avoir choisi le compte, vous êtes redirigé vers :
   ```
   https://workspace.google.com/u/3/checkout/plan?snip=x
   ```
   Au lieu de revenir sur votre application.

---

## 🔍 Cause du Problème

Le problème survient lors du **callback** (retour de Google vers votre application). Cela indique généralement :

1. **URL de callback incorrecte** dans Google Cloud Console
2. **Credentials OAuth incorrects** dans Django Admin
3. **Problème avec le domaine du site** dans Django Admin
4. **SITE_ID incorrect** dans settings.py

---

## ✅ Solution Étape par Étape

### Étape 1 : Vérifier l'URL de Callback Exacte

L'URL de callback utilisée par django-allauth est :
```
http://127.0.0.1:8000/accounts/google/login/callback/
```

**Important** : Notez le `/` à la fin ! L'URL doit être **exactement** celle-ci.

---

### Étape 2 : Vérifier dans Google Cloud Console

1. **Allez sur** : https://console.cloud.google.com/

2. **Allez dans** : "APIs & Services" → "Credentials"

3. **Cliquez sur votre OAuth Client ID** (celui utilisé par MentorXHub)

4. **Vérifiez la section "Authorized redirect URIs"** :
   - Elle doit contenir **exactement** :
     ```
     http://127.0.0.1:8000/accounts/google/login/callback/
     ```
   - **Avec le `/` à la fin !**
   - **Sans `https://`** (pour le développement local)

5. **Si l'URL n'est pas là ou est incorrecte** :
   - Cliquez sur "Edit" (icône crayon)
   - Dans "Authorized redirect URIs", ajoutez/modifiez :
     ```
     http://127.0.0.1:8000/accounts/google/login/callback/
     ```
   - Cliquez sur "Save"

---

### Étape 3 : Vérifier les Credentials dans Django Admin

1. **Allez sur** : `http://127.0.0.1:8000/admin/socialaccount/socialapp/`

2. **Cliquez sur votre application Google** (ou créez-en une si elle n'existe pas)

3. **Vérifiez** :
   - ✅ **Provider** : `Google`
   - ✅ **Client id** : Doit correspondre **exactement** au Client ID de Google Cloud Console
   - ✅ **Secret key** : Doit correspondre **exactement** au Client Secret de Google Cloud Console
   - ✅ **Sites** : Un site doit être dans "Chosen sites"

4. **Si les credentials sont incorrects** :
   - Copiez le **Client ID** depuis Google Cloud Console
   - Copiez le **Client Secret** depuis Google Cloud Console
   - Collez-les dans Django Admin
   - Cliquez sur "Save"

---

### Étape 4 : Vérifier le Site dans Django Admin

1. **Allez sur** : `http://127.0.0.1:8000/admin/sites/site/`

2. **Vérifiez le site** :
   - Il devrait y avoir un site avec :
     - **Domain name** : `example.com` ou `127.0.0.1:8000`
     - **Display name** : `example.com` ou autre
   - **Notez l'ID** de ce site (généralement `1` ou `2`)

3. **Si le site n'existe pas ou est incorrect** :
   - Créez un nouveau site ou modifiez l'existant
   - **Domain name** : `127.0.0.1:8000` (pour développement)
   - **Display name** : `MentorXHub Development`
   - Cliquez sur "Save"
   - **Notez l'ID** du site

---

### Étape 5 : Vérifier le SITE_ID dans settings.py

1. **Ouvrez** : `Mentorxhub/mentorxhub/settings.py`

2. **Cherchez** : `SITE_ID = ...`

3. **Vérifiez que le SITE_ID correspond au site dans Django Admin** :
   ```python
   SITE_ID = 2  # Remplacez par l'ID de votre site (voir Étape 4)
   ```

4. **Si le SITE_ID est incorrect** :
   - Modifiez-le pour correspondre à l'ID du site dans Django Admin
   - Sauvegardez le fichier

---

### Étape 6 : Vérifier que le Site est dans l'Application Social

1. **Retournez sur** : `http://127.0.0.1:8000/admin/socialaccount/socialapp/`

2. **Cliquez sur votre application Google**

3. **Vérifiez la section "Sites"** :
   - Le site (celui avec l'ID que vous avez noté) doit être dans **"Chosen sites"** (colonne de droite)
   - Si ce n'est pas le cas :
     - Sélectionnez le site dans la liste de gauche
     - Cliquez sur la flèche `>` pour l'ajouter à "Chosen sites"
     - Cliquez sur "Save"

---

### Étape 7 : Vérifier les URLs dans urls.py

1. **Ouvrez** : `Mentorxhub/mentorxhub/urls.py`

2. **Vérifiez que `allauth.urls` est inclus** :
   ```python
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('core.urls')),
       path('accounts/', include('accounts.urls')),
       path('mentoring/', include('mentoring.urls')),
       path('dashboard/', include('dashboard.urls')),
       
       # IMPORTANT : allauth.urls doit être APRÈS accounts.urls
       path('accounts/', include('allauth.urls')),
   ]
   ```

3. **Important** : `allauth.urls` doit être **après** `accounts.urls` pour éviter les conflits.

---

### Étape 8 : Redémarrer le Serveur

1. **Arrêtez le serveur Django** (Ctrl+C)

2. **Redémarrez-le** :
   ```bash
   python manage.py runserver
   ```

---

### Étape 9 : Tester à Nouveau

1. **Allez sur** : `http://127.0.0.1:8000/accounts/login/`

2. **Cliquez sur "Connexion avec Google"**

3. **Choisissez votre compte Google**

4. **Autorisez l'application**

5. **Vous devriez être redirigé vers** : `/dashboard/` (votre application)

---

## 🔍 Vérifications Supplémentaires

### Vérifier les Logs Django

Si ça ne fonctionne toujours pas, regardez les logs du serveur Django :

```bash
python manage.py runserver
```

Cherchez les erreurs après avoir choisi le compte Google. Les erreurs courantes :

- `Redirect URI mismatch` → L'URL de callback dans Google Cloud Console est incorrecte
- `Invalid client` → Les credentials dans Django Admin sont incorrects
- `Access denied` → Problème avec les permissions OAuth

### Vérifier dans Google Cloud Console - Détails

1. **Allez dans** : "APIs & Services" → "Credentials"

2. **Cliquez sur votre OAuth Client ID**

3. **Vérifiez** :
   - ✅ **Application type** : `Web application`
   - ✅ **Authorized JavaScript origins** :
     ```
     http://127.0.0.1:8000
     http://localhost:8000
     ```
   - ✅ **Authorized redirect URIs** :
     ```
     http://127.0.0.1:8000/accounts/google/login/callback/
     http://localhost:8000/accounts/google/login/callback/
     ```
     **Important** : Avec le `/` à la fin !

4. **Vérifiez aussi** :
   - ✅ L'API "Google+ API" ou "Google Identity" est activée
   - ✅ L'écran de consentement OAuth est configuré

---

## 🚨 Erreurs Courantes et Solutions

### Erreur : "Redirect URI mismatch"

**Message d'erreur** : `Error 400: redirect_uri_mismatch`

**Cause** : L'URL de callback dans Google Cloud Console ne correspond pas exactement à celle utilisée par django-allauth.

**Solution** :
1. Vérifiez que l'URL dans Google Cloud Console est **exactement** :
   ```
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
2. Vérifiez qu'il y a bien le `/` à la fin
3. Vérifiez qu'il n'y a pas d'espace ou de caractère invisible

---

### Erreur : "Invalid client"

**Message d'erreur** : `Error 401: invalid_client`

**Cause** : Le Client ID ou Secret dans Django Admin ne correspond pas à celui de Google Cloud Console.

**Solution** :
1. Allez dans Google Cloud Console → Credentials
2. Copiez le **Client ID** (tout le texte, y compris `.apps.googleusercontent.com`)
3. Copiez le **Client Secret** (tout le texte, y compris `GOCSPX-`)
4. Collez-les dans Django Admin → Social Applications
5. Vérifiez qu'il n'y a pas d'espaces avant/après

---

### Erreur : Redirection vers Google Workspace

**Cause** : Les credentials ne sont pas configurés ou sont incorrects, Google essaie de rediriger vers une page par défaut.

**Solution** :
1. Vérifiez que l'application OAuth existe dans Django Admin
2. Vérifiez que les credentials sont corrects
3. Vérifiez que le site est bien dans "Chosen sites"
4. Vérifiez que le SITE_ID correspond au site

---

## 📝 Checklist de Vérification

Avant de tester, vérifiez que tout est correct :

- [ ] Application OAuth créée dans Google Cloud Console
- [ ] Client ID et Secret copiés depuis Google Cloud Console
- [ ] **Authorized redirect URIs** contient exactement :
  ```
  http://127.0.0.1:8000/accounts/google/login/callback/
  ```
  (avec le `/` à la fin)
- [ ] Application Google configurée dans Django Admin
- [ ] **Client ID** dans Django Admin = Client ID de Google Cloud Console
- [ ] **Secret key** dans Django Admin = Client Secret de Google Cloud Console
- [ ] Site créé/modifié dans Django Admin avec `127.0.0.1:8000`
- [ ] **SITE_ID** dans settings.py = ID du site dans Django Admin
- [ ] Site sélectionné dans "Chosen sites" de l'application Google
- [ ] API Google+ ou Google Identity activée dans Google Cloud Console
- [ ] `allauth.urls` inclus dans `urls.py` après `accounts.urls`
- [ ] Serveur Django redémarré

---

## 🎯 Résultat Attendu

Après avoir suivi toutes ces étapes :

1. ✅ Clic sur "Connexion avec Google"
2. ✅ Redirection vers Google pour choisir un compte
3. ✅ Choix du compte Google
4. ✅ Autorisation de l'application
5. ✅ **Redirection vers `/dashboard/`** (votre application)
6. ✅ Utilisateur connecté automatiquement

---

## 🔧 Script de Vérification Rapide

Pour vérifier rapidement la configuration, vous pouvez exécuter ce script Python :

```python
# Vérifier la configuration OAuth
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings

print("=== Vérification OAuth ===")
print(f"SITE_ID dans settings: {settings.SITE_ID}")

sites = Site.objects.all()
print(f"\nSites dans la base de données:")
for site in sites:
    print(f"  - ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

social_apps = SocialApp.objects.filter(provider='google')
print(f"\nApplications Google OAuth:")
for app in social_apps:
    print(f"  - Name: {app.name}")
    print(f"    Client ID: {app.client_id[:20]}..." if app.client_id else "    Client ID: (vide)")
    print(f"    Secret: {'Configuré' if app.secret else '(vide)'}")
    print(f"    Sites: {[s.domain for s in app.sites.all()]}")
```

Exécutez-le avec :
```bash
python manage.py shell
```
Puis collez le script.

---

## 📚 Références

- **Documentation django-allauth** : https://docs.allauth.org/en/latest/socialaccount/providers/google.html
- **Google Cloud Console** : https://console.cloud.google.com/
- **OAuth 2.0 Google** : https://developers.google.com/identity/protocols/oauth2

---

*Document créé le : 2025-12-11*  
*Statut : ✅ Guide de dépannage spécifique pour le callback*

