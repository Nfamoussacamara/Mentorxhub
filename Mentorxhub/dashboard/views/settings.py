"""
Vues pour les paramètres du dashboard
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import UserProfileImageForm


@login_required
def settings_view(request):
    """Vue principale des paramètres"""
    user = request.user
    
    context = {
        'user': user,
        'user_role': user.role,
    }
    
    # Détecter si c'est une requête AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/settings.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/settings/view.html', context)


@login_required
def settings_general(request):
    """Paramètres généraux"""
    user = request.user
    
    if request.method == 'POST':
        # Mettre à jour les informations générales
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.bio = request.POST.get('bio', user.bio)
        user.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Paramètres mis à jour avec succès'})
        
        messages.success(request, 'Paramètres mis à jour avec succès')
        return redirect('dashboard:settings')
    
    context = {
        'user': user,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/settings_general.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/settings/general.html', context)


@login_required
def settings_security(request):
    """Paramètres de sécurité"""
    user = request.user
    
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Mot de passe modifié avec succès'})
            
            messages.success(request, 'Mot de passe modifié avec succès')
            return redirect('dashboard:settings_security')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = PasswordChangeForm(user)
    
    context = {
        'form': form,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/settings_security.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/settings/security.html', context)


@login_required
def settings_notifications(request):
    """Paramètres de notifications"""
    user = request.user
    
    if request.method == 'POST':
        # Récupérer les préférences (à implémenter avec un modèle UserPreferences)
        # Pour l'instant, on simule
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Préférences de notifications mises à jour'})
        
        messages.success(request, 'Préférences de notifications mises à jour')
        return redirect('dashboard:settings_notifications')
    
    context = {
        'user': user,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/settings_notifications.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/settings/notifications.html', context)


@login_required
@require_http_methods(["POST"])
def settings_theme(request):
    """Changer le thème (dark/light mode)"""
    theme = request.POST.get('theme', 'light')
    
    if theme not in ['light', 'dark']:
        return JsonResponse({'error': 'Invalid theme'}, status=400)
    
    # Sauvegarder dans la session ou le profil utilisateur
    request.session['theme'] = theme
    
    return JsonResponse({'success': True, 'theme': theme})

