"""
Vues pour les notifications
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from ..models import Notification


@login_required
def notifications_list(request):
    """Liste des notifications de l'utilisateur"""
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:50]
    
    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    
    # Détecter si c'est une requête AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/notifications_list.html', context, request=request)
        return JsonResponse({'html': html, 'unread_count': unread_count}, safe=False)
    
    return render(request, 'dashboard/notifications/list.html', context)


@login_required
@require_http_methods(["POST"])
def notification_mark_read(request, notification_id):
    """Marque une notification comme lue"""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )
    notification.mark_as_read()
    
    return JsonResponse({'success': True})


@login_required
@require_http_methods(["POST"])
def notifications_mark_all_read(request):
    """Marque toutes les notifications comme lues"""
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)
    
    return JsonResponse({'success': True})


@login_required
def notifications_count(request):
    """Retourne le nombre de notifications non lues (API)"""
    count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    return JsonResponse({'count': count})

