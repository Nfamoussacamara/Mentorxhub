# Guide d'Intégration Jitsi Meet - MentorXHub

Ce document détaille les étapes techniques suivies pour implémenter et stabiliser la visioconférence Jitsi dans la plateforme.

## 1. Architecture des URLs (Backend Django)

L'intégration repose sur une route dédiée qui génère un nom de salle unique par session.

### Configuration des routes (`dashboard/urls.py`)
```python
path('sessions/<int:session_id>/video/', sessions.session_video_room, name='session_video_room'),
```

### Logique de la Vue (`dashboard/views/sessions.py`)
La vue remplit trois rôles critiques :
1.  **Sécurité** : Vérification que l'utilisateur est bien le mentor ou l'étudiant lié à la session.
2.  **Identité de salle** : Génération d'un nom de salle unique (`MentorXHub-Session-[ID]`).
3.  **Nettoyage UI** : Injection de drapeaux pour masquer la navigation globale.

```python
context = {
    'session': session,
    'room_name': f"MentorXHub-Session-{session.id}",
    'user_name': request.user.get_full_name(),
    'hide_navbar': True,  # Supprime la navbar globale
    'hide_footer': True,  # Supprime le footer global
}
```

## 2. Intégration Frontend (Template HTML)

### Structure et CSS pour le Plein Écran
Pour que la vidéo soit immersive, le template (`video_room.html`) utilise un CSS spécifique qui neutralise les marges par défaut du site.

```css
body, html {
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden !important; /* Évite les doubles scrollbars */
}
.video-room-container {
    height: 100vh; /* Utilise 100% de la hauteur de la fenêtre */
    width: 100%;
}
```

### Chargement de l'API externe Jitsi
L'intégration utilise la bibliothèque `external_api.js` hébergée par Jitsi pour créer une iframe interactive.

```html
<script src='https://meet.jit.si/external_api.js'></script>
```

## 3. Configuration de l'API Jitsi (JavaScript)

Les paramètres suivants ont été optimisés pour la stabilité :

| Paramètre | Valeur | Description |
| :--- | :--- | :--- |
| `prejoinPageEnabled` | `true` | Essentiel pour initialiser les permissions micro/caméra avant l'entrée. |
| `disableDeepLinking` | `true` | Empêche Jitsi de forcer l'usage de l'application mobile (reste dans le navigateur). |
| `roomName` | Dynamique | Identifiant unique de la session. |
| `parentNode` | `#jitsi-container` | L'élément HTML qui recevra l'iframe. |

## 4. Résolution de Problèmes (Troubleshooting)

### Erreur `NoReverseMatch`
**Cause** : Utilisation de `{% url 'video_room' %}` dans les templates au lieu de `{% url 'dashboard:session_video_room' %}`. 
**Solution** : Toujours préfixer avec le namespace de l'application (`dashboard:`).

### Bouton "Hôte" bloqué
**Cause** : L'authentification Jitsi nécessite l'ouverture d'une pop-up de connexion (Google/FB).
**Solution** : 
1. Vérifier le bloqueur de pop-up du navigateur.
2. S'assurer que `prejoinPageEnabled` est à `true` car cela prépare l'environnement d'authentification.

### Chevauchements UI (Navbar/Footer)
**Cause** : Le template `base.html` inclut ces éléments par défaut.
**Solution** : Utiliser les conditions Django `{% if not hide_navbar %}` couplées aux variables de contexte envoyées par la vue Python.
