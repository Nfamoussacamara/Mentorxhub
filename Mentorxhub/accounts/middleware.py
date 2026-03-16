"""
Middleware pour gérer le processus d'onboarding des utilisateurs.

Ce middleware assure que tous les utilisateurs authentifiés complètent
leur profil après la connexion Google OAuth.
"""

from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch


class OnboardingMiddleware:
    """
    Middleware qui redirige les utilisateurs vers les pages d'onboarding
    s'ils n'ont pas complété leur inscription.
    
    Flux d'onboarding :
    1. Utilisateur se connecte via Google OAuth
    2. Si role == NULL → Redirection vers /onboarding/role/
    3. Si onboarding incomplet → Redirection vers /onboarding/profile/
    4. Sinon → Accès normal à l'application
    """
    
    # URLs publiques accessibles sans authentification
    PUBLIC_URLS = [
        '/accounts/login/',
        '/accounts/signup/',
        '/accounts/logout/',
        '/accounts/google/',  # URLs Google OAuth
        '/admin/',  # Django Admin
        '/static/',  # Fichiers statiques
        '/media/',  # Fichiers média
    ]
    
    # URLs d'onboarding (pour éviter les boucles infinies)
    ONBOARDING_URLS = [
        '/onboarding/role/',
        '/onboarding/profile/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.reverse_exempt_urls = [
            'accounts:login',
            'accounts:signup',
            'accounts:logout',
            'accounts:onboarding_role',  # Page de sélection de rôle
            'admin:index',
            'core:home',  # Page d'accueil publique
            'core:pricing',
            'core:top_mentors',
            'core:about',
            'core:how_it_works',
            'core:careers',
            'core:blog',
            'core:privacy_policy',
            'core:terms_of_service',
            'mentoring:mentors_list',  # Liste des mentors (publique)
            'mentoring:mentor_detail',  # Profil public mentor
            'mentoring:mentee_onboarding',  # Page d'onboarding étudiant
            'mentoring:skip_mentee_onboarding',  # Skip onboarding étudiant
            'mentoring:mentor_onboarding',  # Page d'onboarding mentor
        ]
        # URLs commençant par ceci sont ignorées (Social Auth, Static, Media)
        self.public_prefixes = [
            '/accounts/google/',
            '/static/',
            '/media/',
        ]

    def __call__(self, request):
        path = request.path
        
        # 0. Ignorer les URLs publiques (préfixes)
        if any(path.startswith(prefix) for prefix in self.public_prefixes):
            return self.get_response(request)

        # 1. Vérifier si l'URL est exemptée (résolution dynamique)
        for url_name in self.reverse_exempt_urls:
            try:
                exempted_path = reverse(url_name)
                # Gérer les URLs avec paramètres (ex: public_mentor_profile)
                if path == exempted_path or path.startswith(exempted_path + '/'):
                    return self.get_response(request)
            except NoReverseMatch:
                continue
        
        # 2. Vérifier authentification
        if not request.user.is_authenticated:
            # Login est public via reverse_exempt_urls, donc on laisse passer
            # Si c'est autre chose, @login_required s'en chargera
            return self.get_response(request)
            
        user = request.user
        
        # URLs d'onboarding résolues dynamiquement
        try:
            url_role = reverse('accounts:onboarding_role')
        except NoReverseMatch as e:
            print(f"CRITICAL ERROR: Could not reverse 'accounts:onboarding_role': {e}")
            return self.get_response(request)
        
        # 3. Vérification du Rôle
        if not user.role:
            if path != url_role:
                return redirect(url_role)
            return self.get_response(request)
        
        # Si on est sur la page de choix de rôle mais qu'on a déjà un rôle, on doit sortir
        if path == url_role and user.role:
             # Cette logique est déjà gérée dans la vue RoleSelectionView, mais le middleware doit laisser passer
             pass 

        # 4. Vérification Onboarding
        if not user.onboarding_completed:
            # Vérifier d'abord si l'URL actuelle est une page publique (exemptée)
            is_public_url = False
            for url_name in self.reverse_exempt_urls:
                try:
                    exempted_path = reverse(url_name)
                    if path == exempted_path or path.startswith(exempted_path + '/'):
                        is_public_url = True
                        break
                except NoReverseMatch:
                    continue
            
            # Si c'est une page publique (y compris les pages d'onboarding), laisser passer sans redirection
            if is_public_url:
                return self.get_response(request)
            
            try:
                # Déterminer l'URL cible selon le rôle
                if user.role == 'student':
                    target_url = reverse('mentoring:mentee_onboarding')
                    url_skip = reverse('mentoring:skip_mentee_onboarding')
                elif user.role == 'mentor':
                    target_url = reverse('mentoring:mentor_onboarding')
                    url_skip = None
                else:
                    # Cas fallback, ne devrait pas arriver
                    return self.get_response(request)
                
                # Éviter la boucle de redirection : si on est déjà sur la bonne page ou l'API skip
                if path != target_url and (url_skip is None or path != url_skip):
                    # Rediriger vers la page d'onboarding standalone
                    return redirect(target_url)
                         
            except NoReverseMatch as e:
                print(f"CRITICAL ERROR: Could not reverse onboarding URLs for role {user.role}: {e}")
                return self.get_response(request)

        return self.get_response(request)
