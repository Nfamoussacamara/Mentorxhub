import re

# Lire le fichier
with open('templates/dashboard/fragments/overview_dashboard.html.backup', 'r', encoding='utf-8') as f:
    content = f.read()

# Supprimer les retours à la ligne DANS les balises template
# Pattern: trouve {{ ... }} ou {% ... %} qui s'étendent sur plusieurs lignes
def fix_multiline_tags(text):
    # Fix {{ }} tags
    text = re.sub(r'\{\{([^}]*?)\n\s*([^}]*?)\}\}', r'{{ \1 \2 }}', text)
    text = re.sub(r'\{\{([^}]*?)\n\s*([^}]*?)\n\s*([^}]*?)\}\}', r'{{ \1 \2 \3 }}', text)
    
    # Fix {% %} tags  
    text = re.sub(r'\{%([^%]*?)\n\s*([^%]*?)%\}', r'{% \1 \2 %}', text)
    text = re.sub(r'\{%([^%]*?)\n\s*([^%]*?)\n\s*([^%]*?)%\}', r'{% \1 \2 \3 %}', text)
    
    return text

# Appliquer les corrections plusieurs fois (pour les cas complexes)
for i in range(5):
    content = fix_multiline_tags(content)

# Supprimer les commentaires de debug
content = content.replace('<!-- TEST DIAGNOSTIC: Si vous voyez ce texte avec les balises brutes, Django ne rend PAS le template -->\n', '')
content = content.replace('<!-- TEST: user_role = {{ user_role }}, chart_sessions_total = {{ chart_sessions_total }} -->\n', '')
content = content.replace('<!-- Dashboard Overview - HTMX DESACTIVE POUR TEST -->\n', '<!-- Dashboard Overview -->\n')

# Reactiver HTMX
content = content.replace(
    '''<div id="dashboard-overview-polling">
    <!-- HTMX TEMPORAIREMENT DESACTIVE POUR DEBUG
    hx-get="{% url 'dashboard:dashboard' %}" 
    hx-trigger="every 60s" 
    hx-target="this" 
    hx-swap="innerHTML"
    hx-indicator="#loading-overlay" 
    hx-select="#dashboard-overview-content"
    -->''',
    '''<div id="dashboard-overview-polling" hx-get="{% url 'dashboard:dashboard' %}" hx-trigger="every 60s" hx-target="this" hx-swap="innerHTML" hx-indicator="#loading-overlay" hx-select="#dashboard-overview-content">'''
)

# Écrire le fichier corrigé
with open('templates/dashboard/fragments/overview_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fichier corrige!")
print("Nombre de caracteres:", len(content))
