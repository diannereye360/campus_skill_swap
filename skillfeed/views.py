# ============================================================================
# Views for Campus Skill Swap
# ============================================================================
# Purpose: Handle all business logic and page rendering
# In Django: Views = functions that receive HTTP requests, return HTTP responses
# BEST PRACTICE: Keep views simple, put complex logic in models or services
# ============================================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

from django.db.models import Avg
from .models import Skill, SkillRequest, UserProfile, SkillRating
from .forms import (
    UserRegistrationForm,
    SkillForm,
    UserProfileForm,
    SkillRequestForm,
    SkillRequestResponseForm,
)


# ============================================================================
# HOME PAGE
# ============================================================================

def home(request):
    """
    Home page view - public view, no login required.
    Shows featured skills and general information.
    """
    # Get recent skills
    recent_skills = Skill.objects.filter(is_available=True).order_by("-created_at")[:6]
    
    # Count statistics
    total_skills = Skill.objects.count()
    total_users = UserProfile.objects.count()
    total_requests = SkillRequest.objects.count()
    
    context = {
        "recent_skills": recent_skills,
        "total_skills": total_skills,
        "total_users": total_users,
        "total_requests": total_requests,
    }
    
    return render(request, "skillfeed/home.html", context)


# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================
# Purpose: Handle user registration, login, logout

def user_register(request):
    """
    User registration view.
    GET: Show registration form
    POST: Process registration
    
    BEST PRACTICE: Always validate form data on the server, not just frontend!
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()
            
            # Create a UserProfile for this user (signals could do this automatically)
            UserProfile.objects.create(user=user)
            
            # Show success message
            messages.success(
                request,
                f"Welcome {user.username}! You can now log in."
            )
            return redirect("login")
        else:
            # Form has errors - they're automatically shown in template
            messages.error(request, "Registration failed. Check the errors below.")
    else:
        form = UserRegistrationForm()
    
    context = {"form": form}
    return render(request, "skillfeed/register.html", context)


def user_login(request):
    """
    User login view.
    GET: Show login form
    POST: Authenticate user
    
    SECURITY NOTE: Never store passwords in plain text!
    Django's authenticate() function handles this securely.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Django's authenticate function checks credentials safely
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Credentials are correct
            login(request, user)  # Creates session
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("dashboard")
        else:
            # Credentials are wrong
            messages.error(request, "Invalid username or password.")
    
    return render(request, "skillfeed/login.html")


@login_required(login_url="login")
def user_logout(request):
    """
    User logout view.
    
    @login_required decorator ensures only logged-in users can access.
    If not logged in, redirects to login page.
    """
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect("home")


# ============================================================================
# PROFILE VIEWS
# ============================================================================

@login_required(login_url="login")
def profile(request):
    """
    View and edit user profile.
    GET: Show profile
    POST: Update profile
    """
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)
    
    # Get user's skills
    user_skills = request.user.skills.all()
    
    context = {
        "profile": profile,
        "form": form,
        "user_skills": user_skills,
    }
    return render(request, "skillfeed/profile.html", context)


# ============================================================================
# SKILL VIEWS - LIST, DETAIL, CREATE, EDIT, DELETE
# ============================================================================

def skill_list(request):
    """
    Browse all available skills (public view).
    Includes search and filter functionality.
    
    PAGINATION BEST PRACTICE: Always paginate lists to improve performance
    """
    # Get all available skills, annotated with average rating
    skills = Skill.objects.filter(is_available=True).annotate(avg_rating=Avg("ratings__rating"))
    
    # SEARCH: Filter by title or description
    search_query = request.GET.get("search", "").strip()
    if search_query:
        skills = skills.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # FILTER by category
    category = request.GET.get("category", "").strip()
    if category:
        skills = skills.filter(category=category)
    
    # FILTER by price type
    price_type = request.GET.get("price", "").strip()
    if price_type:
        skills = skills.filter(price_type=price_type)
    
    # Pagination: 12 skills per page
    paginator = Paginator(skills, 12)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "category": category,
        "price_type": price_type,
    }
    
    return render(request, "skillfeed/skill_list.html", context)


def skill_detail(request, pk):
    """
    View details of a specific skill.
    pk = primary key (id)
    
    BEST PRACTICE: Use get_object_or_404 to return 404 if skill doesn't exist
    This is better than manually checking if object exists and raising error
    """
    skill = get_object_or_404(Skill, pk=pk)
    
    # Increment view count
    skill.view_count += 1
    skill.save(update_fields=["view_count"])
    
    # Get recent requests on this skill
    requests = skill.requests.all()[:5]
    
    # Check if current user has already requested this skill
    user_has_requested = False
    if request.user.is_authenticated:
        user_has_requested = SkillRequest.objects.filter(
            requester=request.user,
            skill=skill
        ).exists()
    
    avg_rating = skill.ratings.aggregate(avg=Avg("rating"))["avg"]
    avg_rating_int = round(avg_rating) if avg_rating else 0
    rating_count = skill.ratings.count()

    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = SkillRating.objects.get(user=request.user, skill=skill).rating
        except SkillRating.DoesNotExist:
            pass

    context = {
        "skill": skill,
        "requests": requests,
        "user_has_requested": user_has_requested,
        "avg_rating": avg_rating_int,
        "rating_count": rating_count,
        "user_rating": user_rating,
        "star_range": range(1, 6),
    }

    return render(request, "skillfeed/skill_detail.html", context)


@login_required(login_url="login")
def skill_create(request):
    """
    Create a new skill post.
    
    IMPORTANT: Only logged-in users can create skills.
    The @login_required decorator enforces this automatically.
    """
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            # Create skill but don't save yet... we need to set the owner!
            skill = form.save(commit=False)
            skill.owner = request.user  # Set current user as owner
            skill.save()
            
            messages.success(request, "Your skill has been posted!")
            return redirect("skill_detail", pk=skill.pk)
    else:
        form = SkillForm()
    
    context = {"form": form, "action": "Create"}
    return render(request, "skillfeed/skill_form.html", context)


@login_required(login_url="login")
def skill_edit(request, pk):
    """
    Edit an existing skill post.
    
    SECURITY IMPORTANT: Check that user owns this skill!
    Otherwise, anyone could edit anyone's skills.
    """
    skill = get_object_or_404(Skill, pk=pk)
    
    # PERMISSION CHECK: Only owner can edit
    if skill.owner != request.user:
        messages.error(request, "You can't edit skills you don't own!")
        return HttpResponseForbidden("You cannot edit this skill.")
    
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Your skill has been updated!")
            return redirect("skill_detail", pk=skill.pk)
    else:
        form = SkillForm(instance=skill)
    
    context = {"form": form, "skill": skill, "action": "Edit"}
    return render(request, "skillfeed/skill_form.html", context)


@login_required(login_url="login")
def skill_delete(request, pk):
    """
    Delete a skill post.
    
    SECURITY: Same permission check as edit - only owner can delete!
    """
    skill = get_object_or_404(Skill, pk=pk)
    
    # PERMISSION CHECK
    if skill.owner != request.user:
        messages.error(request, "You can't delete skills you don't own!")
        return HttpResponseForbidden("You cannot delete this skill.")
    
    if request.method == "POST":
        # Deletion is confirmed
        skill.delete()
        messages.success(request, "Your skill has been deleted.")
        return redirect("dashboard")
    
    # GET request - show confirmation page
    context = {"skill": skill}
    return render(request, "skillfeed/skill_confirm_delete.html", context)


# ============================================================================
# DASHBOARD VIEW
# ============================================================================

@login_required(login_url="login")
def dashboard(request):
    """
    User's personal dashboard - overview of their skills and requests.
    
    This shows:
    - Skills they've posted
    - Requests they've received
    - Requests they've made
    """
    user = request.user
    
    # User's skills
    user_skills = user.skills.all()
    
    # Requests this user received (someone wants their skill)
    received_requests = SkillRequest.objects.filter(responder=user).order_by("-requested_at")
    
    # Requests this user made (they want someone else's skill)
    made_requests = SkillRequest.objects.filter(requester=user).order_by("-requested_at")
    
    # Statistics
    skill_count = user_skills.count()
    received_count = received_requests.filter(status="pending").count()
    made_count = made_requests.count()
    
    context = {
        "user_skills": user_skills,
        "received_requests": received_requests,
        "made_requests": made_requests,
        "skill_count": skill_count,
        "received_count": received_count,
        "made_count": made_count,
    }
    
    return render(request, "skillfeed/dashboard.html", context)


# ============================================================================
# SKILL REQUEST VIEWS
# ============================================================================

@login_required(login_url="login")
def request_skill(request, pk):
    """
    User requests to use another student's skill.
    """
    skill = get_object_or_404(Skill, pk=pk)
    
    # Can't request your own skills!
    if skill.owner == request.user:
        messages.error(request, "You can't request your own skills!")
        return redirect("skill_detail", pk=skill.pk)
    
    # Check if already requested
    if SkillRequest.objects.filter(requester=request.user, skill=skill).exists():
        messages.warning(request, "You've already requested this skill!")
        return redirect("skill_detail", pk=skill.pk)
    
    if request.method == "POST":
        form = SkillRequestForm(request.POST)
        if form.is_valid():
            # Create request
            skill_request = form.save(commit=False)
            skill_request.requester = request.user
            skill_request.skill = skill
            skill_request.responder = skill.owner
            skill_request.save()
            
            messages.success(request, "Your request has been sent!")
            return redirect("dashboard")
    else:
        form = SkillRequestForm()
    
    context = {"form": form, "skill": skill}
    return render(request, "skillfeed/request_skill.html", context)


@login_required(login_url="login")
def rate_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == "POST":
        try:
            rating_value = int(request.POST.get("rating", 0))
        except (ValueError, TypeError):
            rating_value = 0
        if 1 <= rating_value <= 5:
            SkillRating.objects.update_or_create(
                user=request.user,
                skill=skill,
                defaults={"rating": rating_value},
            )
            messages.success(request, "Your rating has been saved!")
        else:
            messages.error(request, "Please select a rating between 1 and 5.")
    return redirect("skill_detail", pk=pk)


@login_required(login_url="login")
def respond_to_request(request, pk):
    """
    Respond to a skill request (accept or decline).
    
    SECURITY: User can only respond to requests they received!
    """
    skill_request = get_object_or_404(SkillRequest, pk=pk)
    
    # PERMISSION CHECK: Only the skill owner can respond
    if skill_request.responder != request.user:
        messages.error(request, "You can't respond to this request!")
        return HttpResponseForbidden("You cannot respond to this request.")
    
    if request.method == "POST":
        form = SkillRequestResponseForm(request.POST)
        if form.is_valid():
            # Update the request
            skill_request.status = form.cleaned_data["status"]
            skill_request.response_message = form.cleaned_data["response_message"]
            skill_request.response_at = timezone.now()
            skill_request.save()
            
            # Show appropriate message
            if skill_request.status == "accepted":
                messages.success(
                    request,
                    f"You accepted {skill_request.requester.username}'s request!"
                )
            else:
                messages.info(
                    request,
                    f"You declined {skill_request.requester.username}'s request."
                )
            
            return redirect("dashboard")
    else:
        form = SkillRequestResponseForm()
    
    context = {"form": form, "skill_request": skill_request}
    return render(request, "skillfeed/respond_request.html", context)
