"""
Vues pour le support client
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from ..models import SupportTicket, TicketReply
from ..forms import SupportTicketForm
from django.utils import timezone


@login_required
def support_tickets_list(request):
    """Liste des tickets de support de l'utilisateur"""
    user = request.user
    
    tickets = SupportTicket.objects.filter(user=user).order_by('-created_at')
    
    # Statistiques
    open_tickets = tickets.filter(status__in=['open', 'in_progress']).count()
    resolved_tickets = tickets.filter(status='resolved').count()
    
    context = {
        'tickets': tickets,
        'open_tickets': open_tickets,
        'resolved_tickets': resolved_tickets,
        'user_role': user.role,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/support_tickets_list.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/support/tickets_list.html', context)


@login_required
def support_ticket_create(request):
    """Créer un nouveau ticket de support"""
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.status = 'open'
            ticket.save()
            messages.success(request, "Ticket créé avec succès! Nous vous répondrons bientôt.")
            return redirect('dashboard:support_ticket_detail', ticket_id=ticket.id)
    else:
        form = SupportTicketForm()
    
    context = {
        'form': form,
        'user_role': request.user.role,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/support_ticket_create.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/support/ticket_create.html', context)


@login_required
def support_ticket_detail(request, ticket_id):
    """Détails d'un ticket de support"""
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    
    # Récupérer les réponses
    replies = ticket.replies.all().order_by('created_at')
    
    context = {
        'ticket': ticket,
        'replies': replies,
        'user_role': request.user.role,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/support_ticket_detail.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/support/ticket_detail.html', context)


@login_required
def support_ticket_reply(request, ticket_id):
    """Ajouter une réponse à un ticket"""
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        
        if not content:
            return JsonResponse({'error': 'Le contenu est requis'}, status=400)
        
        reply = TicketReply.objects.create(
            ticket=ticket,
            author=request.user,
            content=content
        )
        
        # Mettre à jour le statut du ticket si nécessaire
        if ticket.status == 'resolved':
            ticket.status = 'open'
            ticket.save(update_fields=['status'])
        
        return JsonResponse({
            'success': True,
            'reply': {
                'id': str(reply.id),
                'content': reply.content,
                'author': reply.author.get_full_name(),
                'created_at': reply.created_at.isoformat(),
            }
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def support_ticket_close(request, ticket_id):
    """Fermer un ticket"""
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    
    if request.method == 'POST':
        ticket.status = 'closed'
        ticket.save(update_fields=['status'])
        messages.success(request, "Ticket fermé avec succès.")
        return redirect('dashboard:support_tickets_list')
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def support_faq(request):
    """Page FAQ"""
    # TODO: Créer un modèle FAQ si nécessaire
    faqs = [
        {
            'question': 'Comment créer un compte ?',
            'answer': 'Cliquez sur "S\'inscrire" et remplissez le formulaire.',
        },
        {
            'question': 'Comment réserver une session ?',
            'answer': 'Allez dans "Trouver un Mentor", choisissez un mentor et créez une session.',
        },
        {
            'question': 'Comment payer ?',
            'answer': 'Les paiements se font via notre système sécurisé après chaque session.',
        },
        # Ajouter plus de FAQs selon les besoins
    ]
    
    context = {
        'faqs': faqs,
        'user_role': request.user.role,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/support_faq.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/support/faq.html', context)

