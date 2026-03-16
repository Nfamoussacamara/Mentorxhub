#!/usr/bin/env python
"""
Script pour lancer les tests du dashboard
"""
import os
import sys
import django

# Configuration Django
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorxhub.settings')
    django.setup()
    
    from django.test.utils import get_runner
    from django.conf import settings
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False)
    
    # Lancer les tests
    failures = test_runner.run_tests(['dashboard.tests'])
    
    sys.exit(0 if failures == 0 else 1)

