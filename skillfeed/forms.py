# ============================================================================
# Django Forms for Campus Skill Swap
# ============================================================================
# Purpose: Forms handle data validation and CSRF protection automatically
# Why Django Forms? Instead of writing manual validation, Django does it for us
# Common Mistake: Writing HTML forms manually without Django Forms - harder to validate!
# ============================================================================

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Skill, SkillRequest, UserProfile


# ============================================================================
# User Registration Form
# ============================================================================
# Purpose: Handle user registration with password confirmation
# ============================================================================

class UserRegistrationForm(UserCreationForm):
    """
    Custom registration form extending Django's built-in UserCreationForm.
    
    This automatically:
    - Validates password strength
    - Confirms password matches
    - Creates User account
    """
    
    email = forms.EmailField(
        required=True,
        help_text="Enter your institutional or personal email"
    )
    first_name = forms.CharField(
        max_length=100,
        required=False,
        help_text="Optional: Your first name"
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        help_text="Optional: Your last name"
    )
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
    
    def clean_email(self):
        """
        Validation: Make sure email isn't already registered
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered!")
        return email
    
    def clean_username(self):
        """
        Validation: Username must be unique
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken!")
        return username


# ============================================================================
# Skill Form
# ============================================================================
# Purpose: Create and edit skill posts
# ============================================================================

class SkillForm(forms.ModelForm):
    """
    Form for creating and editing skill posts.
    
    ModelForm automatically creates form fields from model fields.
    This means changes to the Skill model automatically update the form!
    
    BEST PRACTICE: Use ModelForm for model-based forms - DRY principle
    (Don't Repeat Yourself - define fields once in the model)
    """
    
    class Meta:
        model = Skill
        fields = [
            "title",
            "description",
            "category",
            "price_type",
            "price_amount",
            "contact_preference",
            "is_available",
        ]
        
        # Customize how fields look in HTML
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g., Python Programming Tutoring",
                "maxlength": "200"
            }),
            
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Describe your skill, experience, how long sessions take, etc."
            }),
            
            "category": forms.Select(attrs={
                "class": "form-select"
            }),
            
            "price_type": forms.Select(attrs={
                "class": "form-select"
            }),
            
            "price_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Only if paid",
                "step": "0.01"
            }),
            
            "contact_preference": forms.Select(attrs={
                "class": "form-select"
            }),
            
            "is_available": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
    
    def clean_price_amount(self):
        """
        Validation: If price_type is 'paid', price_amount is required
        """
        price_type = self.cleaned_data.get("price_type")
        price_amount = self.cleaned_data.get("price_amount")
        
        if price_type == "paid" and not price_amount:
            raise forms.ValidationError(
                "Please enter a price for paid skills."
            )
        
        if price_type != "paid" and price_amount:
            # Clear price if it's not a paid skill
            self.cleaned_data["price_amount"] = None
        
        return price_amount


# ============================================================================
# User Profile Form
# ============================================================================
# Purpose: Let users update their profile information
# ============================================================================

class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile.
    """
    
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_picture", "phone_number", "location"]
        
        widgets = {
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tell other students about yourself"
            }),
            
            "profile_picture": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*"
            }),
            
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Optional: Your phone number",
                "type": "tel"
            }),
            
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your location (city, campus, etc.)"
            }),
        }


# ============================================================================
# Skill Request Form
# ============================================================================
# Purpose: When requesting a skill, allow user to send a message
# ============================================================================

class SkillRequestForm(forms.ModelForm):
    """
    Form for requesting a skill from another student.
    """
    
    class Meta:
        model = SkillRequest
        fields = ["message"]
        
        widgets = {
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Explain why you're interested in this skill...",
            }),
        }


# ============================================================================
# Skill Request Response Form
# ============================================================================
# Purpose: Respond to a skill request (accept/decline with message)
# ============================================================================

class SkillRequestResponseForm(forms.Form):
    """
    Form for responding to a skill request.
    Separate from ModelForm because we need custom logic for status.
    """
    
    STATUS_CHOICES = [
        ("accepted", "Accept Request"),
        ("declined", "Decline Request"),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.RadioSelect(attrs={
            "class": "form-check-input"
        })
    )
    
    response_message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "Your response message..."
        }),
        help_text="Tell them why you accepted/declined and how to proceed"
    )
