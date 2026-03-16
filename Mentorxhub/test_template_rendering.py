from django.test import Client
from accounts.models import CustomUser
from mentoring.models import MentorProfile, StudentProfile

# Créer client de test
client = Client()

# Créer un utilisateur de test
user = CustomUser.objects.create_user(
    email='test@test.com',
    password='testpass123',
    role='student'
)

# Créer profil student
StudentProfile.objects.create(user=user)

# Se connecter
client.login(email='test@test.com', password='testpass123')

# Récupérer la page dashboard
response = client.get('/dashboard/')

# Afficher le code HTML
html = response.content.decode('utf-8')

# Chercher les balises template
import re
template_tags = re.findall(r'\{\{.*?\}\}', html)

print("=== BALISES TEMPLATE TROUVÉES DANS LE HTML ===")
if template_tags:
    print(f"PROBLÈME! {len(template_tags)} balises template non rendues:")
    for tag in template_tags[:10]:  # Afficher les 10 premières
        print(f"  - {tag}")
else:
    print("SUCCÈS! Aucune balise template brute trouvée")

# Chercher spécifiquement total_hours_chart
if 'total_hours_chart' in html:
    # Extraire le contexte
    idx = html.find('total_hours_chart')
    context = html[max(0, idx-100):idx+100]
    print("\n=== CONTEXTE total_hours_chart ===")
    print(context)
