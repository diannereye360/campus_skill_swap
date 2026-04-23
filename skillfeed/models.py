from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ============================================================================
# UserProfile Model
# ============================================================================
# Purpose: Extends Django's built-in User model with extra profile information
# Why? Django User model has username, password, email but we need more fields
# Best Practice: Always create a separate profile model rather than subclassing User
# ============================================================================

class UserProfile(models.Model):
    """
    Extended user profile with additional information.
    This connects to Django's built-in User model using a OneToOneField.
    
    OneToOneField means: each User has exactly ONE profile, and each profile belongs to ONE User
    on_delete=models.CASCADE means: if user is deleted, their profile is deleted too
    """
    
    # Link to Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    # Additional fields for student profile
    bio = models.TextField(blank=True, null=True, help_text="Tell other students about yourself")
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
        help_text="Upload a profile picture"
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Set once when created
    
    class Meta:
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        """Display format: 'John Doe (johndoe)'"""
        return f"{self.user.get_full_name() or self.user.username}"


# ============================================================================
# Skill Model
# ============================================================================
# Purpose: Represents a skill or service a student can offer
# This is the main model for the marketplace
# ============================================================================

class Skill(models.Model):
    """
    A skill or service offered by a student.
    
    ForeignKey('User') means: many Skills belong to ONE User
    Every skill must have an owner (the student offering it)
    """
    
    # Category choices - what type of skill is this?
    CATEGORY_CHOICES = [
        ("tutoring", "Tutoring"),
        ("tech", "Technology"),
        ("creativity", "Creative Skills"),
        ("sports", "Sports & Fitness"),
        ("languages", "Languages"),
        ("music", "Music"),
        ("writing", "Writing"),
        ("design", "Design"),
        ("other", "Other"),
    ]
    
    # Price type choices
    PRICE_CHOICES = [
        ("free", "Free"),
        ("exchange", "Skill Exchange"),
        ("paid", "Paid"),
    ]
    
    # Contact preference choices - how should people reach out?
    CONTACT_CHOICES = [
        ("email", "Email"),
        ("phone", "Phone"),
        ("zoom", "Video Call (Zoom)"),
        ("inperson", "In-Person"),
        ("chat", "Chat/Messaging"),
    ]
    
    # IMPORTANT: ForeignKey connects Skill to User
    # If a user is deleted, all their skills are deleted (CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    
    # Basic skill information
    title = models.CharField(
        max_length=200,
        help_text="e.g., 'Python Programming Tutoring'"
    )
    description = models.TextField(
        help_text="Detailed description of what you offer, how long it takes, etc."
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other"
    )
    
    # Pricing information
    price_type = models.CharField(
        max_length=20,
        choices=PRICE_CHOICES,
        default="free"
    )
    price_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Leave blank if not paid"
    )
    
    # Contact and availability
    contact_preference = models.CharField(
        max_length=20,
        choices=CONTACT_CHOICES,
        default="email"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Is this skill available right now?"
    )
    
    # Metadata - when created/updated
    created_at = models.DateTimeField(auto_now_add=True)  # Set once, never changes
    updated_at = models.DateTimeField(auto_now=True)  # Updated every time saved
    view_count = models.IntegerField(default=0, help_text="Track popularity")
    
    class Meta:
        ordering = ["-created_at"]  # Show newest skills first
        indexes = [
            models.Index(fields=["owner", "-created_at"]),  # Speed up owner queries
        ]
    
    def __str__(self):
        """Display format: 'Python Tutoring by johndoe'"""
        return f"{self.title} by {self.owner.username}"
    
    def is_free(self):
        """Quick check if this skill is offered for free"""
        return self.price_type == "free"
    
    def get_price_display(self):
        """Format price nicely for templates"""
        if self.price_type == "free":
            return "FREE"
        elif self.price_type == "exchange":
            return "Skill Exchange"
        elif self.price_type == "paid":
            return f"${self.price_amount}"
        return "Contact for details"


# ============================================================================
# SkillRequest Model
# ============================================================================
# Purpose: When someone wants to use a skill, they send a request
# This tracks the conversation flow
# ============================================================================

class SkillRequest(models.Model):
    """
    A request from one student to another to use their skill.
    
    This creates a connection between:
    - requester (Student who wants the skill)
    - skill (The skill being requested)
    - responder (Student who offers the skill)
    """
    
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("completed", "Completed"),
        ("declined", "Declined"),
    ]
    
    # The student requesting the skill
    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skill_requests_made"
    )
    
    # The skill being requested
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="requests"
    )
    
    # Student who OFFERS the skill (convenience field - same as skill.owner)
    responder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skill_requests_received"
    )
    
    # Request details
    message = models.TextField(help_text="Why do you want this skill?")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    response_message = models.TextField(
        blank=True,
        null=True,
        help_text="Responder's reply"
    )
    
    # Timestamps
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ["-requested_at"]
        # IMPORTANT: Prevent duplicate requests
        unique_together = ["requester", "skill"]
    
    def __str__(self):
        return f"{self.requester.username} requested {self.skill.title}"


# ============================================================================
# SkillRating Model
# ============================================================================

class SkillRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings_given")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "skill"]

    def __str__(self):
        return f"{self.user.username} rated {self.skill.title} {self.rating}/5"
