"""
Vues pour la gestion des cours
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count, Avg, Q
from django.contrib import messages
from ..models import Course, Lesson, CourseProgress
from ..forms import CourseForm, LessonForm
from django.utils import timezone


@login_required
def courses_list(request):
    """Liste des cours (pour étudiants) ou mes cours (pour mentors)"""
    user = request.user
    
    if user.role == 'mentor':
        # Les mentors voient leurs propres cours
        courses = Course.objects.filter(mentor=user).order_by('-created_at')
        template = 'dashboard/courses/my_courses.html'
    else:
        # Les étudiants voient les cours publiés
        courses = Course.objects.filter(is_published=True).select_related('mentor').order_by('-created_at')
        template = 'dashboard/courses/list.html'
    
    context = {
        'courses': courses,
        'user_role': user.role,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/courses_list.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, template, context)


@login_required
def course_detail(request, course_id):
    """Détails d'un cours"""
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    
    # Vérifier les permissions
    if user.role == 'mentor' and course.mentor != user:
        messages.error(request, "Vous n'avez pas accès à ce cours.")
        return redirect('dashboard:courses_list')
    
    # Récupérer les leçons
    lessons = course.lessons.all().order_by('order')
    
    # Pour les étudiants, récupérer la progression
    progress = None
    if user.role == 'student':
        progress, created = CourseProgress.objects.get_or_create(
            student=user,
            course=course
        )
    
    context = {
        'course': course,
        'lessons': lessons,
        'progress': progress,
        'user_role': user.role,
        'is_mentor': user.role == 'mentor' and course.mentor == user,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/course_detail.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/courses/detail.html', context)


@login_required
def course_create(request):
    """Créer un nouveau cours (mentors uniquement)"""
    if request.user.role != 'mentor':
        messages.error(request, "Seuls les mentors peuvent créer des cours.")
        return redirect('dashboard:courses_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.mentor = request.user
            course.save()
            messages.success(request, "Cours créé avec succès!")
            return redirect('dashboard:course_detail', course_id=course.id)
    else:
        form = CourseForm()
    
    context = {
        'form': form,
        'user_role': request.user.role,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/course_create.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/courses/create.html', context)


@login_required
def course_edit(request, course_id):
    """Modifier un cours (mentors uniquement)"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.user.role != 'mentor' or course.mentor != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier ce cours.")
        return redirect('dashboard:course_detail', course_id=course.id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Cours mis à jour avec succès!")
            return redirect('dashboard:course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    context = {
        'form': form,
        'course': course,
        'user_role': request.user.role,
    }
    
    return render(request, 'dashboard/courses/edit.html', context)


@login_required
def lesson_detail(request, course_id, lesson_id):
    """Détails d'une leçon"""
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    user = request.user
    
    # Vérifier les permissions
    if user.role == 'mentor' and course.mentor != user:
        messages.error(request, "Vous n'avez pas accès à cette leçon.")
        return redirect('dashboard:course_detail', course_id=course.id)
    
    # Pour les étudiants, mettre à jour la progression
    progress = None
    if user.role == 'student':
        progress, created = CourseProgress.objects.get_or_create(
            student=user,
            course=course
        )
        # Marquer la leçon comme accédée (mais pas complétée)
        progress.last_accessed = timezone.now()
        progress.save(update_fields=['last_accessed'])
    
    # Récupérer les leçons précédente et suivante
    all_lessons = list(course.lessons.all().order_by('order'))
    current_index = all_lessons.index(lesson)
    previous_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None
    
    context = {
        'course': course,
        'lesson': lesson,
        'progress': progress,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'user_role': user.role,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/lesson_detail.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/courses/lesson_detail.html', context)


@login_required
def lesson_complete(request, course_id, lesson_id):
    """Marquer une leçon comme complétée"""
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    if request.user.role != 'student':
        return JsonResponse({'error': 'Students only'}, status=403)
    
    if request.method == 'POST':
        progress, created = CourseProgress.objects.get_or_create(
            student=request.user,
            course=course
        )
        
        # Ajouter la leçon aux leçons complétées
        if lesson not in progress.completed_lessons.all():
            progress.completed_lessons.add(lesson)
            progress.update_progress()
        
        return JsonResponse({
            'success': True,
            'progress_percentage': float(progress.progress_percentage)
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def lesson_create(request, course_id):
    """Créer une nouvelle leçon (mentors uniquement)"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.user.role != 'mentor' or course.mentor != request.user:
        messages.error(request, "Vous n'avez pas la permission de créer une leçon.")
        return redirect('dashboard:course_detail', course_id=course.id)
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, "Leçon créée avec succès!")
            return redirect('dashboard:course_detail', course_id=course.id)
    else:
        form = LessonForm()
    
    context = {
        'form': form,
        'course': course,
        'user_role': request.user.role,
    }
    
    return render(request, 'dashboard/courses/lesson_create.html', context)

