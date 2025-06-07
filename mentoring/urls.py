from django.urls import path
from . import views

app_name = 'mentoring'

urlpatterns = [
    # Vues principales
    path('', views.HomeView.as_view(), name='home'),
    
    # Vues des mentors
    path('mentors/', views.MentorListView.as_view(), name='mentor_list'),
    path('mentors/create/', views.MentorCreateView.as_view(), name='mentor_create'),
    path('mentors/<int:pk>/', views.MentorDetailView.as_view(), name='mentor_detail'),
    path('mentors/<int:pk>/update/', views.MentorUpdateView.as_view(), name='mentor_update'),
    path('mentors/<int:pk>/edit/', views.mentor_edit, name='mentor_edit'),
    
    # Vues des étudiants
    path('students/create/', views.StudentCreateView.as_view(), name='student_create'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/update/', views.StudentUpdateView.as_view(), name='student_update'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    
    # Vues des sessions
    path('sessions/', views.SessionListView.as_view(), name='session_list'),
    path('sessions/create/<int:mentor_id>/', views.SessionCreateView.as_view(), name='session_create'),
    path('sessions/<int:pk>/', views.SessionDetailView.as_view(), name='session_detail'),
    path('sessions/<int:pk>/update/', views.SessionUpdateView.as_view(), name='session_update'),
    path('sessions/<int:pk>/cancel/', views.SessionCancelView.as_view(), name='session_cancel'),
    path('sessions/<int:pk>/feedback/', views.FeedbackCreateView.as_view(), name='feedback_create'),
    path('sessions/new/', views.SessionCreateView.as_view(), name='session_new'),
    
    # Vues des disponibilités
    path('availabilities/', views.AvailabilityListView.as_view(), name='availability_list'),
    path('availabilities/create/', views.AvailabilityCreateView.as_view(), name='availability_create'),
    path('availabilities/<int:pk>/update/', views.AvailabilityUpdateView.as_view(), name='availability_update'),
    path('availabilities/<int:pk>/delete/', views.AvailabilityDeleteView.as_view(), name='availability_delete'),
    
    # Vues des feedbacks
    path('sessions/<int:pk>/feedback/', views.FeedbackCreateView.as_view(), name='feedback_create'),
] 