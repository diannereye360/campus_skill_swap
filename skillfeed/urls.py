# ============================================================================
# URL Routing for Skillfeed App
# ============================================================================
# Purpose: Map URL patterns to view functions
# How it works: When user visits /skills/browse/, Django finds the matching
# path and calls the associated view function
# ============================================================================

from django.urls import path
from . import views

# URL configuration for skillfeed app
# Note: No app_name to keep URLs simple for beginners

urlpatterns = [
    # ===== HOME/PUBLIC PAGES =====
    path("", views.home, name="home"),
    path("skills/browse/", views.skill_list, name="skill_list"),
    path("skills/<int:pk>/", views.skill_detail, name="skill_detail"),
    
    # ===== AUTHENTICATION PAGES =====
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    
    # ===== USER PROFILE =====
    path("profile/", views.profile, name="profile"),
    path("dashboard/", views.dashboard, name="dashboard"),
    
    # ===== SKILL MANAGEMENT (CRUD) =====
    # Create
    path("skills/create/", views.skill_create, name="skill_create"),
    # Update (Edit)
    path("skills/<int:pk>/edit/", views.skill_edit, name="skill_edit"),
    # Delete
    path("skills/<int:pk>/delete/", views.skill_delete, name="skill_delete"),
    
    # ===== SKILL REQUESTS =====
    path("skills/<int:pk>/request/", views.request_skill, name="request_skill"),
    path("requests/<int:pk>/respond/", views.respond_to_request, name="respond_request"),
    path("skills/<int:pk>/rate/", views.rate_skill, name="rate_skill"),
]
