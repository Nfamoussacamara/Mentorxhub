from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import MentorProfile, StudentProfile, Availability, MentoringSession
from .forms import MentorProfileForm, StudentProfileForm, AvailabilityForm, MentoringSessionForm, SessionFeedbackForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Count, Sum

class HomeView(ListView):
    template_name = 'mentoring/home.html'
    context_object_name = 'mentors'

    def get_queryset(self):
        return MentorProfile.objects.filter(is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mentors'] = MentorProfile.objects.count()
        context['total_students'] = StudentProfile.objects.count()
        context['total_sessions'] = MentoringSession.objects.count()
        context['total_hours'] = MentoringSession.objects.aggregate(
            total_hours=Sum('duration')
        )['total_hours'] or 0
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Vérifier si l'utilisateur a un profil
            if request.user.role == 'mentor' and not hasattr(request.user, 'mentor_profile'):
                return redirect('mentoring:mentor_create')
            elif request.user.role == 'student' and not hasattr(request.user, 'student_profile'):
                return redirect('mentoring:student_create')
        return super().dispatch(request, *args, **kwargs)

class MentorListView(ListView):
    model = MentorProfile
    template_name = 'mentoring/mentor_list.html'
    context_object_name = 'mentors'
    paginate_by = 10

    def get_queryset(self):
        queryset = MentorProfile.objects.filter(is_available=True)
        search_query = self.request.GET.get('search', '')
        expertise = self.request.GET.get('expertise', '')
        
        if search_query:
            queryset = queryset.filter(
                user__first_name__icontains=search_query
            ) | queryset.filter(
                user__last_name__icontains=search_query
            ) | queryset.filter(
                expertise__icontains=search_query
            )
        
        if expertise:
            queryset = queryset.filter(expertise__icontains=expertise)
            
        return queryset.select_related('user')

class MentorDetailView(LoginRequiredMixin, DetailView):
    model = MentorProfile
    template_name = 'mentoring/mentor_detail.html'
    context_object_name = 'mentor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['availabilities'] = self.object.availabilities.all()
        context['available_slots'] = self.object.get_available_slots()
        return context

class MentorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MentorProfile
    form_class = MentorProfileForm
    template_name = 'mentoring/mentor_form.html'

    def test_func(self):
        return not hasattr(self.request.user, 'mentor_profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_available = True
        messages.success(self.request, 'Profil mentor créé avec succès !')
        response = super().form_valid(form)
        return redirect('mentoring:mentor_detail', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Créer un profil mentor'
        return context

class MentorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MentorProfile
    form_class = MentorProfileForm
    template_name = 'mentoring/mentor_profile_update.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profil mentor mis à jour avec succès !')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mentoring:mentor_detail', kwargs={'pk': self.object.pk})

class StudentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = StudentProfile
    template_name = 'mentoring/student_profile.html'
    context_object_name = 'student'

    def test_func(self):
        return self.request.user.role == 'student'

    def get_context_data(self, **kwargs):      
        context = super().get_context_data(**kwargs)
        context['sessions'] = self.object.mentoring_sessions.all()
        return context

class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'mentoring/student_profile_update.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profil étudiant mis à jour avec succès !')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mentoring:student_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mettre à jour le profil étudiant'
        return context

class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'mentoring/student_form.html'

    def test_func(self):
        return not hasattr(self.request.user, 'student_profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Profil étudiant créé avec succès !')
        response = super().form_valid(form)
        return redirect('mentoring:student_detail', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Créer un profil étudiant'
        return context

class SessionListView(LoginRequiredMixin, ListView):
    model = MentoringSession
    template_name = 'mentoring/session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        if self.request.user.role == 'student':
            return MentoringSession.objects.filter(student=self.request.user.student_profile)
        return MentoringSession.objects.filter(mentor=self.request.user.mentor_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['upcoming_sessions'] = self.get_queryset().filter(
            start_time__gt=now
        ).order_by('start_time')
        context['past_sessions'] = self.get_queryset().filter(
            start_time__lte=now
        ).order_by('-start_time')
        return context

class SessionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MentoringSession
    template_name = 'mentoring/session_detail.html'
    context_object_name = 'session'

    def test_func(self):
        session = self.get_object()
        return (self.request.user.role == 'student' and session.student == self.request.user.student_profile) or \
               (self.request.user.role == 'mentor' and session.mentor == self.request.user.mentor_profile)

class SessionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MentoringSession
    form_class = MentoringSessionForm
    template_name = 'mentoring/session_form.html'

    def test_func(self):
        return self.request.user.role == 'student'

    def form_valid(self, form):
        form.instance.student = self.request.user.student_profile
        messages.success(self.request, 'Session créée avec succès !')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mentoring:session_list')

class SessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MentoringSession
    form_class = MentoringSessionForm
    template_name = 'mentoring/session_form.html'

    def test_func(self):
        session = self.get_object()
        return (self.request.user.role == 'student' and session.student == self.request.user.student_profile) or \
               (self.request.user.role == 'mentor' and session.mentor == self.request.user.mentor_profile)

    def form_valid(self, form):
        messages.success(self.request, 'Session mise à jour avec succès !')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mentoring:session_list')

class SessionCancelView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MentoringSession
    fields = []
    template_name = 'mentoring/session_confirm_cancel.html'

    def test_func(self):
        session = self.get_object()
        return (self.request.user.role == 'student' and session.student == self.request.user.student_profile) or \
               (self.request.user.role == 'mentor' and session.mentor == self.request.user.mentor_profile)

    def form_valid(self, form):
        self.object.status = 'cancelled'
        messages.success(self.request, 'Session annulée avec succès !')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mentoring:session_list')

class AvailabilityListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Availability 
    template_name = 'mentoring/availability_list.html'
    context_object_name = 'availabilities'

    def test_func(self):
        return self.request.user.role == 'mentor'

    def get_queryset(self):
        return Availability.objects.filter(mentor=self.request.user.mentor_profile)

class AvailabilityCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'mentoring/availability_form.html'

    def test_func(self):
        return self.request.user.role == 'mentor'

    def form_valid(self, form):
        form.instance.mentor = self.request.user.mentor_profile
        messages.success(self.request, 'Disponibilité créée avec succès !')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mentoring:availability_list')

class AvailabilityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'mentoring/availability_form.html'

    def test_func(self):
        return self.get_object().mentor == self.request.user.mentor_profile

    def form_valid(self, form):
        messages.success(self.request, 'Disponibilité mise à jour avec succès !')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mentoring:availability_list')

class AvailabilityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Availability
    template_name = 'mentoring/availability_confirm_delete.html'

    def test_func(self):
        return self.get_object().mentor == self.request.user.mentor_profile

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Disponibilité supprimée avec succès !')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('mentoring:availability_list')

class FeedbackCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MentoringSession
    form_class = SessionFeedbackForm
    template_name = 'mentoring/feedback_form.html'

    def test_func(self):
        session = self.get_object()
        return (self.request.user.role == 'student' and session.student == self.request.user.student_profile) or \
               (self.request.user.role == 'mentor' and session.mentor == self.request.user.mentor_profile)

    def form_valid(self, form):
        messages.success(self.request, 'Feedback envoyé avec succès !')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mentoring:session_list')

@login_required
def mentor_detail(request, pk):
    mentor = get_object_or_404(MentorProfile, user_id=pk)
    availabilities = Availability.objects.filter(mentor=mentor, date__gte=timezone.now().date())
    reviews = Review.objects.filter(session__mentor=mentor).order_by('-created_at')
    
    context = {
        'mentor': mentor,
        'availabilities': availabilities,
        'reviews': reviews,
    }
    return render(request, 'profiles/mentor_profile.html', context)

@login_required
def mentor_edit(request, pk):
    mentor = get_object_or_404(MentorProfile, user_id=pk)
    
    if request.user != mentor.user:
        messages.error(request, "Vous n'avez pas la permission de modifier ce profil.")
        return redirect('mentoring:mentor_detail', pk=pk)
    
    if request.method == 'POST':
        form = MentorProfileForm(request.POST, request.FILES, instance=mentor)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('mentoring:mentor_detail', pk=pk)
    else:
        form = MentorProfileForm(instance=mentor)
    
    context = {
        'form': form,
        'mentor': mentor,
    }
    return render(request, 'mentoring/mentor_edit.html', context)

@login_required
def student_detail(request, pk):
    student = get_object_or_404(StudentProfile, user_id=pk)
    upcoming_sessions = MentoringSession.objects.filter(
        student=student,
        date__gte=timezone.now().date()
    ).order_by('date', 'start_time')
    
    past_sessions = MentoringSession.objects.filter(
        student=student,
        date__lt=timezone.now().date()
    ).order_by('-date', '-start_time')
    
    context = {
        'student': student,
        'upcoming_sessions': upcoming_sessions,
        'past_sessions': past_sessions,
    }
    return render(request, 'profiles/student_profile.html', context)

@login_required
def student_edit(request, pk):
    student = get_object_or_404(StudentProfile, user_id=pk)
    
    if request.user != student.user:
        messages.error(request, "Vous n'avez pas la permission de modifier ce profil.")
        return redirect('mentoring:student_detail', pk=pk)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('mentoring:student_detail', pk=pk)
    else:
        form = StudentProfileForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
    }
    return render(request, 'mentoring/student_edit.html', context)