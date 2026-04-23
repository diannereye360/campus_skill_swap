# ============================================================================
# Django Admin Configuration
# ============================================================================
# Purpose: Make models manageable through Django admin interface
# Access it at: http://localhost:8000/admin/
# ============================================================================

from django.contrib import admin
from .models import UserProfile, Skill, SkillRequest


# ============================================================================
# UserProfile Admin
# ============================================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    
    @admin.register() decorator is shorthand for:
        admin.site.register(UserProfile, UserProfileAdmin)
    """
    
    list_display = ("user", "phone_number", "location", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "user__email", "phone_number")
    
    fieldsets = (
        ("User Info", {
            "fields": ("user",)
        }),
        ("Personal Info", {
            "fields": ("bio", "profile_picture", "phone_number", "location")
        }),
        ("System Info", {
            "fields": ("created_at",),
            "classes": ("collapse",)  # Hide by default
        }),
    )
    
    readonly_fields = ("created_at",)


# ============================================================================
# Skill Admin
# ============================================================================

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Admin interface for Skill model.
    Organize information with fieldsets to make it easier to navigate.
    """
    
    list_display = ("title", "owner", "category", "price_type", "is_available", "created_at", "view_count")
    list_filter = ("category", "price_type", "is_available", "created_at")
    search_fields = ("title", "description", "owner__username")
    
    # FIELDSETS organize the form into sections
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "description", "category", "owner")
        }),
        ("Pricing", {
            "fields": ("price_type", "price_amount"),
            "description": "Set price_type to 'free' to ignore price_amount"
        }),
        ("Contact & Availability", {
            "fields": ("contact_preference", "is_available")
        }),
        ("Statistics", {
            "fields": ("view_count", "created_at", "updated_at"),
            "classes": ("collapse",)  # Hidden by default
        }),
    )
    
    readonly_fields = ("created_at", "updated_at", "view_count")
    
    # Auto-set owner when creating in admin
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new (not editing)
            obj.owner = request.user
        super().save_model(request, obj, form, change)


# ============================================================================
# SkillRequest Admin
# ============================================================================

@admin.register(SkillRequest)
class SkillRequestAdmin(admin.ModelAdmin):
    """
    Admin interface for SkillRequest model.
    Track requests between students.
    """
    
    list_display = ("requester", "skill", "responder", "status", "requested_at")
    list_filter = ("status", "requested_at")
    search_fields = ("requester__username", "responder__username", "skill__title")
    
    fieldsets = (
        ("Request Info", {
            "fields": ("requester", "skill", "responder", "message")
        }),
        ("Response", {
            "fields": ("status", "response_message", "responded_at")
        }),
        ("Timestamps", {
            "fields": ("requested_at",),
            "classes": ("collapse",)
        }),
    )
    
    readonly_fields = ("requested_at",)
    
    # Prevent editing requester/skill after creation
    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing
            return self.readonly_fields + ("requester", "skill", "responder")
        return self.readonly_fields
