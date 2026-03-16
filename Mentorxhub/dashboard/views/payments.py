"""
Vues pour la gestion des paiements
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from ..models import Payment
from ..forms import PaymentForm
from django.contrib import messages
import json


@login_required
def payments_list(request):
    """Liste des paiements de l'utilisateur"""
    user = request.user
    
    payments = Payment.objects.filter(user=user).select_related(
        'session', 'course'
    ).order_by('-created_at')
    
    # Statistiques
    total_paid = payments.filter(status='completed').aggregate(
        Sum('amount')
    )['amount__sum'] or 0.0
    
    pending_payments = payments.filter(status='pending').count()
    
    context = {
        'payments': payments,
        'total_paid': total_paid,
        'pending_payments': pending_payments,
        'user_role': user.role,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/payments_list.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/payments/list.html', context)


@login_required
def payment_detail(request, payment_id):
    """Détails d'un paiement"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    context = {
        'payment': payment,
        'user_role': request.user.role,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/payment_detail.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/payments/detail.html', context)


@login_required
def payment_create(request):
    """Créer un nouveau paiement"""
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.status = 'pending'
            payment.save()
            
            # TODO: Intégrer avec un système de paiement (Stripe, PayPal, etc.)
            # Pour l'instant, on simule juste la création
            
            messages.success(request, "Paiement initié avec succès!")
            return redirect('dashboard:payment_detail', payment_id=payment.id)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'user_role': request.user.role,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/payment_create.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/payments/create.html', context)


@login_required
def payment_invoice(request, payment_id):
    """Télécharger la facture PDF d'un paiement"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    if payment.status != 'completed':
        messages.error(request, "Le paiement doit être complété pour télécharger la facture.")
        return redirect('dashboard:payment_detail', payment_id=payment.id)
    
    # TODO: Générer le PDF de la facture
    # Pour l'instant, on retourne un message
    if payment.invoice_pdf:
        # Si le PDF existe déjà, le servir
        from django.conf import settings
        import os
        file_path = os.path.join(settings.MEDIA_ROOT, payment.invoice_pdf.name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="invoice_{payment.id}.pdf"'
                return response
    
    # Sinon, générer le PDF (à implémenter)
    messages.info(request, "Génération de la facture en cours...")
    return redirect('dashboard:payment_detail', payment_id=payment.id)


@login_required
def payments_stats(request):
    """Statistiques des paiements (API endpoint)"""
    user = request.user
    period = request.GET.get('period', '30d')  # 7d, 30d, 90d, 365d
    
    # Calculer la date de début selon la période
    end_date = timezone.now().date()
    if period == '7d':
        start_date = end_date - timedelta(days=7)
    elif period == '30d':
        start_date = end_date - timedelta(days=30)
    elif period == '90d':
        start_date = end_date - timedelta(days=90)
    elif period == '365d':
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=30)
    
    payments = Payment.objects.filter(
        user=user,
        created_at__date__range=[start_date, end_date]
    )
    
    stats = {
        'total_amount': float(payments.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0.0),
        'total_count': payments.count(),
        'completed_count': payments.filter(status='completed').count(),
        'pending_count': payments.filter(status='pending').count(),
        'failed_count': payments.filter(status='failed').count(),
        'by_type': {
            'session': float(payments.filter(payment_type='session', status='completed').aggregate(Sum('amount'))['amount__sum'] or 0.0),
            'course': float(payments.filter(payment_type='course', status='completed').aggregate(Sum('amount'))['amount__sum'] or 0.0),
            'subscription': float(payments.filter(payment_type='subscription', status='completed').aggregate(Sum('amount'))['amount__sum'] or 0.0),
        }
    }
    
    return JsonResponse(stats)

