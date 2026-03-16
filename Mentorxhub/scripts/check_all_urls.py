"""
Script pour vérifier que tous les URLs du projet sont fonctionnels
"""
import os
import sys
import django

# Configuration Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorxhub.settings')
django.setup()

from django.urls import reverse, NoReverseMatch, get_resolver
from django.conf import settings

def get_all_url_patterns():
    """Récupère tous les patterns d'URL du projet"""
    resolver = get_resolver()
    patterns = []
    
    def extract_urls(url_patterns, prefix=''):
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # Namespace ou include
                if hasattr(pattern, 'namespace') and pattern.namespace:
                    new_prefix = f"{pattern.namespace}:"
                else:
                    new_prefix = prefix
                extract_urls(pattern.url_patterns, new_prefix)
            else:
                # Pattern simple
                if hasattr(pattern, 'name') and pattern.name:
                    full_name = f"{prefix}{pattern.name}" if prefix else pattern.name
                    patterns.append(full_name)
    
    extract_urls(resolver.url_patterns)
    return patterns

def test_urls():
    """Teste tous les URLs"""
    print("=" * 60)
    print("VÉRIFICATION DE TOUS LES URLS")
    print("=" * 60)
    
    # URLs à tester manuellement
    test_urls = [
        # Core
        'core:home',
        'core:dashboard',
        'core:pricing',
        'core:top_mentors',
        'core:about',
        'core:how_it_works',
        'core:careers',
        'core:blog',
        'core:privacy_policy',
        'core:terms_of_service',
        
        # Accounts
        'accounts:signup',
        'accounts:login',
        'accounts:logout',
        'accounts:profile',
        'accounts:profile_edit',
        'accounts:onboarding_role',
        'accounts:password_reset',
        'accounts:password_reset_done',
        
        # Mentoring
        'mentoring:mentor_list',
        'mentoring:mentor_detail',
        'mentoring:mentor_dashboard',
        'mentoring:student_dashboard',
        'mentoring:mentee_onboarding',
        'mentoring:mentor_onboarding',
    ]
    
    success = []
    failed = []
    
    for url_name in test_urls:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:40} -> {url}")
            success.append(url_name)
        except NoReverseMatch as e:
            print(f"❌ {url_name:40} -> ERREUR: {e}")
            failed.append(url_name)
        except Exception as e:
            print(f"⚠️  {url_name:40} -> EXCEPTION: {e}")
            failed.append(url_name)
    
    print("\n" + "=" * 60)
    print(f"Résumé: {len(success)} réussis, {len(failed)} échoués")
    print("=" * 60)
    
    if failed:
        print("\nURLs en échec:")
        for url in failed:
            print(f"  - {url}")
    
    return len(failed) == 0

if __name__ == '__main__':
    success = test_urls()
    sys.exit(0 if success else 1)

