"""
Vues pour la messagerie en temps réel
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q, Max, Count
from django.utils import timezone
from ..models import Conversation, Message
from ..forms import MessageForm
import json


@login_required
def messages_list(request):
    """Liste des conversations de l'utilisateur"""
    user = request.user
    
    # Récupérer toutes les conversations de l'utilisateur avec le dernier message
    conversations = Conversation.objects.filter(
        participants=user
    ).annotate(
        last_message_time=Max('messages__created_at'),
        participant_count=Count('participants')
    ).order_by('-last_message_time', '-updated_at')
    
    # Séparer les groupes (3+ participants) et les conversations directes (2 participants)
    groups = []
    direct_messages = []
    
    for conv in conversations:
        conv.unread_count = conv.get_unread_count(user)
        conv.last_message = conv.get_last_message()
        
        # Déterminer si c'est un groupe ou une conversation directe
        if conv.participant_count > 2:
            groups.append(conv)
        else:
            direct_messages.append(conv)
    
    context = {
        'groups': groups,
        'direct_messages': direct_messages,
        'conversations': conversations,  # Pour compatibilité
        'user_role': user.role,
    }
    
    # Pour les requêtes HTMX, retourner le layout de page complet
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'dashboard/fragments/messages_page_full.html', context)
    
    return render(request, 'dashboard/messages/list.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """Détails d'une conversation"""
    user = request.user
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=user)
    
    # Marquer tous les messages comme lus
    Message.objects.filter(
        conversation=conversation
    ).exclude(sender=user).update(is_read=True, status='read')
    
    # Récupérer tous les messages de la conversation
    messages = conversation.messages.select_related('sender').order_by('created_at')
    
    # Déterminer si c'est un groupe ou une conversation directe
    participant_count = conversation.participants.count()
    is_group = participant_count > 2
    
    # Récupérer les participants
    participants = conversation.participants.exclude(id=user.id)
    other_participant = participants.first() if not is_group else None
    
    # Récupérer toutes les conversations pour afficher la liste
    all_conversations = Conversation.objects.filter(
        participants=user
    ).annotate(
        last_message_time=Max('messages__created_at'),
        participant_count=Count('participants')
    ).order_by('-last_message_time', '-updated_at')
    
    # Séparer les groupes et les conversations directes
    groups = []
    direct_messages = []
    
    for conv in all_conversations:
        conv.unread_count = conv.get_unread_count(user)
        conv.last_message = conv.get_last_message()
        
        if conv.participant_count > 2:
            groups.append(conv)
        else:
            direct_messages.append(conv)
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'other_participant': other_participant,
        'participants': participants,
        'is_group': is_group,
        'groups': groups,
        'direct_messages': direct_messages,
        'form': MessageForm(),
    }
    
    # Pour les requêtes HTMX, retourner directement le fragment HTML
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'dashboard/fragments/messages_chat_panel.html', context)
    
    return render(request, 'dashboard/messages/conversation.html', context)


@login_required
def conversation_create(request):
    """Créer une nouvelle conversation"""
    if request.method == 'POST':
        data = json.loads(request.body)
        recipient_id = data.get('recipient_id')
        
        if not recipient_id:
            return JsonResponse({'error': 'Recipient ID required'}, status=400)
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        recipient = get_object_or_404(User, id=recipient_id)
        
        # Vérifier si une conversation existe déjà
        existing_conv = Conversation.objects.filter(
            participants=request.user
        ).filter(participants=recipient).first()
        
        if existing_conv:
            return JsonResponse({
                'success': True,
                'conversation_id': str(existing_conv.id),
                'redirect': f'/dashboard/messages/{existing_conv.id}/'
            })
        
        # Créer une nouvelle conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, recipient)
        
        return JsonResponse({
            'success': True,
            'conversation_id': str(conversation.id),
            'redirect': f'/dashboard/messages/{conversation.id}/'
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def message_send(request, conversation_id):
    """Envoyer un message dans une conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            # Mettre à jour la date de mise à jour de la conversation
            conversation.updated_at = timezone.now()
            conversation.save(update_fields=['updated_at'])
            
            # Pour HTMX, retourner le fragment HTML du message
            if request.headers.get('HX-Request') == 'true':
                context = {
                    'message': message,
                    'user': request.user,
                }
                return render(request, 'dashboard/fragments/message_item.html', context)
            
            # Fallback JSON pour compatibilité
            return JsonResponse({
                'success': True,
                'message': {
                    'id': str(message.id),
                    'content': message.content,
                    'sender': message.sender.get_full_name(),
                    'created_at': message.created_at.isoformat(),
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def messages_unread_count(request):
    """Retourne le nombre de messages non lus"""
    user = request.user
    conversations = Conversation.objects.filter(participants=user)
    total_unread = sum(conv.get_unread_count(user) for conv in conversations)
    
    return JsonResponse({'unread_count': total_unread})


@login_required
def messages_poll(request):
    """Endpoint pour polling des nouveaux messages (pour temps réel)"""
    user = request.user
    conversation_id = request.GET.get('conversation_id')
    
    if not conversation_id:
        return JsonResponse({'error': 'conversation_id required'}, status=400)
    
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=user)
    
    # Récupérer le dernier message ID depuis la requête HTMX
    last_message_id = request.GET.get('last_message_id')
    
    # Récupérer les nouveaux messages depuis le dernier message connu
    messages_query = conversation.messages.select_related('sender').exclude(sender=user)
    
    if last_message_id:
        messages_query = messages_query.filter(id__gt=last_message_id)
    else:
        # Si pas de last_message_id, prendre les 5 derniers messages non lus
        messages_query = messages_query.filter(is_read=False)[:5]
    
    new_messages = list(messages_query.order_by('created_at'))
    
    # Pour HTMX, retourner les fragments HTML des messages
    if request.headers.get('HX-Request') == 'true' and new_messages:
        html_parts = []
        for message in new_messages:
            context = {
                'message': message,
                'user': user,
            }
            html_parts.append(render_to_string('dashboard/fragments/message_item.html', context, request=request))
        return HttpResponse(''.join(html_parts))
    
    # Fallback JSON pour compatibilité
    return JsonResponse({
        'messages': [{
            'id': str(msg.id),
            'content': msg.content,
            'sender': msg.sender.get_full_name(),
            'created_at': msg.created_at.isoformat(),
        } for msg in new_messages]
    })

