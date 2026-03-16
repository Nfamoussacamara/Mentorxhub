from django.urls import path
from . import views, api_views

app_name = 'mentoring'

urlpatterns = [
    # URLs pour la liste des mentors
    path('mentors/', views.MentorListView.as_view(), name='mentor_list'),
    
    # URLs pour les profils
    path('mentor/<int:pk>/', views.PublicMentorProfileView.as_view(), name='mentor_detail'),
    path('mentor/profile/update/', views.MentorProfileUpdateView.as_view(), name='mentor_profile_update'),
    path('student/profile/', views.StudentProfileView.as_view(), name='student_profile'),
    path('student/profile/update/', views.StudentProfileUpdateView.as_view(), name='student_profile_update'),

    # URLs pour les disponibilités
    path('mentor/availabilities/', views.AvailabilityListView.as_view(), name='availability_list'),
    path('mentor/availabilities/create/', views.AvailabilityCreateView.as_view(), name='availability_create'),
    path('mentor/availabilities/<int:pk>/update/', views.AvailabilityUpdateView.as_view(), name='availability_update'),
    path('mentor/availabilities/<int:pk>/delete/', views.AvailabilityDeleteView.as_view(), name='availability_delete'),

    # URLs pour les sessions de mentorat
    path('sessions/', views.MentoringSessionListView.as_view(), name='session_list'),
    path('available-sessions/', views.AvailableSessionListView.as_view(), name='available_sessions'),
    path('sessions/<int:pk>/', views.MentoringSessionDetailView.as_view(), name='session_detail'),
    path('sessions/create/<int:mentor_id>/', views.MentoringSessionCreateView.as_view(), name='session_create'),
    path('mentor/sessions/create/', views.MentorMentoringSessionCreateView.as_view(), name='mentor_session_create'),
    path('mentor/sessions/create-available/', views.MentorCreateAvailableSessionView.as_view(), name='mentor_create_available_session'),
    path('sessions/<int:pk>/update/', views.MentoringSessionUpdateView.as_view(), name='session_update'),
    path('sessions/<int:pk>/delete/', views.MentoringSessionDeleteView.as_view(), name='session_delete'),
    path('sessions/<int:pk>/approve/', views.SessionApproveView.as_view(), name='session_approve'),
    path('sessions/<int:pk>/reject/', views.SessionRejectView.as_view(), name='session_reject'),
    path('sessions/<int:pk>/feedback/', views.SessionFeedbackView.as_view(), name='session_feedback'),
    path('sessions/<int:pk>/book/', views.BookSessionView.as_view(), name='book_session'),
    
    # Onboarding
    path('onboarding/mentee/', views.MenteeOnboardingView.as_view(), name='mentee_onboarding'),
    path('onboarding/mentee/skip/', views.SkipMenteeOnboardingView.as_view(), name='skip_mentee_onboarding'),
    path('onboarding/mentor/', views.MentorOnboardingView.as_view(), name='mentor_onboarding'),
    
    # API
    path('api/mentors/', api_views.MentorListAPIView.as_view(), name='mentor_list_api'),
] 