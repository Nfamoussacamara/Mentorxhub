from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    
    # Pages publiques
    path('pricing/', views.pricing_view, name='pricing'),
    path('top-mentors/', views.top_mentors_view, name='top_mentors'),
    path('about/', views.about_view, name='about'),
    path('how-it-works/', views.how_it_works_view, name='how_it_works'),
    path('careers/', views.careers_view, name='careers'),
    path('blog/', views.blog_view, name='blog'),
    
    # Pages légales
    path('privacy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms/', views.terms_of_service_view, name='terms_of_service'),
    
    # Documentation / Développement
    path('all-links/', views.all_links_view, name='all_links'),
]