# Django Best Practices - Campus Skill Swap Edition

This guide explains the professional practices used in this project and why each one matters.

## 📐 Architecture & Design Patterns

### 1. **Model-View-Template (MVT) Pattern**

**What it is:**
- **Models** (skillfeed/models.py): Define database structure
- **Views** (skillfeed/views.py): Handle logic and request processing
- **Templates** (templates/): Display data to users

**Why it matters:**
- Separation of concerns: Each layer has one job
- Easier to test: Logic separated from presentation
- Scalable: Can change database, UI, or logic independently

**Example from this project:**
```python
# Model: Define what a Skill is
class Skill(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

# View: Get skill and render template
def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    return render(request, "skillfeed/skill_detail.html", {"skill": skill})

# Template: Display the skill
<h1>{{ skill.title }}</h1> by {{ skill.owner.username }}
```

---

## 🎯 Model Design Best Practices

### 1. **Foreign Keys for Relationships**

✅ **Good:**
```python
class Skill(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # If user deleted, all their skills deleted too
```

❌ **Avoid:**
```python
class Skill(models.Model):
    owner_name = models.CharField(max_length=100)  # Wrong! Duplicates data
```

**Why:** Foreign Keys maintain data integrity and prevent duplicates.

### 2. **Meaningful Default Values**

```python
class Skill(models.Model):
    is_available = models.BooleanField(default=True)  # New skills start available
    created_at = models.DateTimeField(auto_now_add=True)  # Set once, never changes
    updated_at = models.DateTimeField(auto_now=True)  # Updates automatically
```

**Benefits:**
- Prevents NULL data
- Automatically tracks timestamps
- Sensible defaults

### 3. **Choices for Limited Options**

```python
class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("tutoring", "Tutoring"),
        ("tech", "Technology"),
        # ...
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other"
    )
```

**Why:**
- Prevents invalid data
- Provides consistent options
- Database can't have typos like "TEKNOLOGY"

### 4. **Database Indexes for Performance**

```python
class Skill(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["owner", "-created_at"]),
        ]
```

**Why:** Speeds up searches filtering by owner and date.

### 5. **Helpful Meta Options**

```python
class Skill(models.Model):
    class Meta:
        ordering = ["-created_at"]  # Newest first by default
        # ...
```

---

## 🔐 Security Best Practices

### 1. **CSRF Protection**

Every form must include {% csrf_token %}:
```html
<form method="POST">
    {% csrf_token %}  <!-- Required! -->
    <input type="text" name="title">
    <button type="submit">Submit</button>
</form>
```

**Why:** Prevents Cross-Site Request Forgery attacks where hackers trick users into submitting forms.

### 2. **Password Security**

```python
# ✅ Good: Let Django hash passwords
user = User.objects.create_user(
    username="john",
    password="secure_password"  # Automatically hashed
)

# ❌ Never do this:
user.password = "plaintext_password"  # Bad! Never stored plain
user.save()
```

**How Django does it:**
- Hashes with PBKDF2 algorithm
- Adds random salt
- Hard to reverse even if database is hacked

### 3. **Permission Checks**

```python
# IMPORTANT: Verify user owns the resource!
@login_required(login_url="login")
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    
    # Permission check before allowing edit
    if skill.owner != request.user:
        return HttpResponseForbidden("Not your skill!")
    
    # ... rest of view
```

**Why:** Prevents users from editing other's skills.

### 4. **SQL Injection Prevention**

✅ **Safe (using ORM):**
```python
skills = Skill.objects.filter(title__icontains=search_query)
```

❌ **Dangerous (raw SQL):**
```python
Skill.objects.raw(f"SELECT * FROM skillfeed_skill WHERE title LIKE '%{search_query}%'")
```

**Why:** Django ORM parameterizes queries automatically.

### 5. **XSS (Cross-Site Scripting) Protection**

✅ **Safe (Django auto-escapes):**
```html
{{ skill.description }}  <!-- HTML entities escaped -->
```

❌ **Dangerous:**
```html
{{ skill.description|safe }}  <!-- Allows HTML tags! -->
```

**Why:** If user enters `<script>alert('hacked')</script>`, Django escapes it.

---

## 📦 Form Handling Best Practices

### 1. **Use ModelForm for Database Models**

✅ **Good: Uses ModelForm**
```python
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['title', 'description', 'category', ...]
```

**Why:** DRY principle - define fields once in model, reuse in form.

### 2. **Custom Validation**

```python
class SkillForm(forms.ModelForm):
    def clean_price_amount(self):
        price_type = self.cleaned_data.get("price_type")
        price_amount = self.cleaned_data.get("price_amount")
        
        # Custom rule: paid skills need a price
        if price_type == "paid" and not price_amount:
            raise forms.ValidationError("Set price for paid skills!")
        
        return price_amount
```

**Why:** Prevents invalid data from reaching database.

### 3. **Form.save(commit=False)**

```python
@login_required
def skill_create(request):
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            # Don't save yet - we need to add the owner
            skill = form.save(commit=False)
            skill.owner = request.user  # Add owner
            skill.save()  # NOW save to database
```

**Why:** Lets us modify the object before saving.

---

## 🎬 View Best Practices

### 1. **Function-Based vs Class-Based Views**

We use **function-based views** because they're:
- Easier for beginners
- More explicit
- Less "magic"
- Perfect for simple views

```python
def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    return render(request, "template.html", {"skill": skill})
```

### 2. **Decorators for Protection**

```python
# Only logged-in users can access
@login_required(login_url="login")
def dashboard(request):
    # ...
```

**Benefits:**
- Clean, readable code
- Automatic redirect to login
- Reusable across views

### 3. **get_object_or_404()**

✅ **Good:**
```python
skill = get_object_or_404(Skill, pk=pk)  # Returns 404 if not found
```

❌ **Avoid:**
```python
try:
    skill = Skill.objects.get(pk=pk)
except Skill.DoesNotExist:
    return HttpResponse("Not found", status=404)  # More code
```

### 4. **Django Messages Framework**

```python
from django.contrib import messages

# Show feedback to user
messages.success(request, "Skill created successfully!")
messages.error(request, "Something went wrong!")
messages.warning(request, "This action cannot be undone")
```

**Why:** User gets instant feedback about actions.

---

## 📝 Template Best Practices

### 1. **Template Inheritance**

✅ **Good structure:**
```html
<!-- base.html - used by ALL pages -->
<html>
    <nav>...</nav>
    {% block content %}{% endblock %}
    <footer>...</footer>
</html>

<!-- home.html - extends base.html -->
{% extends 'base.html' %}
{% block content %}
    <h1>Welcome!</h1>
{% endblock %}
```

**Why:** Avoid repeating HTML on every page.

### 2. **URL Reversing**

```html
<!-- Don't hardcode URLs -->
<a href="/skills/browse/">Browse</a>  <!-- Bad -->

<!-- Use url tag -->
<a href="{% url 'skill_list' %}">Browse</a>  <!-- Good -->
```

**Why:** If URL changes, automatically updates everywhere.

### 3. **Static Files**

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}">
```

**Why:**
- Works in development and production
- Can add versioning for caching

### 4. **Meaningful Block Names**

```html
{% block title %}Page Title{% endblock %}
{% block content %}Page content{% endblock %}
{% block extra_js %}Page-specific JavaScript{% endblock %}
```

**Why:** Clear what each block contains.

---

## 🧪 Testing (Best Practice)

While we haven't written tests here, professional Django apps test:

```python
# skillfeed/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Skill

class SkillModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='test123'
        )
    
    def test_skill_creation(self):
        skill = Skill.objects.create(
            owner=self.user,
            title="Python Tutoring"
        )
        self.assertEqual(skill.title, "Python Tutoring")
        self.assertEqual(skill.owner, self.user)
```

**Why test:**
- Catch bugs before production
- Ensure features don't break
- Easier refactoring

---

## 📊 Performance Best Practices

### 1. **Query Optimization**

✅ **Good:**
```python
# Get user with profile in one query
users = User.objects.select_related('profile').all()
```

❌ **Avoid (N+1 queries):**
```python
for user in User.objects.all():
    print(user.profile.bio)  # Separate query for each user!
```

### 2. **Pagination**

```python
from django.core.paginator import Paginator

# Don't load all 10,000 skills at once!
skills = Skill.objects.filter(is_available=True)
paginator = Paginator(skills, 12)  # 12 per page
page = paginator.get_page(request.GET.get('page'))
```

**Why:** Faster page loads, less memory.

### 3. **Database Indexes**

```python
class Skill(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["owner", "-created_at"]),
        ]
```

**Why:** Queries are 10-100x faster.

---

## 🔄 Code Organization Best Practices

### 1. **Single Responsibility**

Each function does ONE thing:
```python
# Good: Separate concerns
def home(request):
    recent_skills = Skill.objects.all()[:6]
    context = {"skills": recent_skills}
    return render(request, "home.html", context)

# Bad: Doing too much
def home(request):
    # Complex business logic mixed with rendering
```

### 2. **Naming Conventions**

```python
# ✅ Good: Clear what data it contains
user_skills = user.skills.all()
received_requests = SkillRequest.objects.filter(responder=user)

# ❌ Bad: Unclear
skills = user.skills.all()
requests = user.requests  # Which requests? Sent or received?
```

### 3. **Comments**

Use comments sparingly:
```python
# ✅ Good: Explains WHY
skill.view_count += 1  # Track popularity for sorting

# ❌ Bad: Explains WHAT (obvious from code)
view_count = view_count + 1  # Increase view count
```

---

## 🚀 Deployment Best Practices (Future)

When deploying to production:

```python
# settings.py for production
DEBUG = False  # NEVER True in production
ALLOWED_HOSTS = ["skillswap.com"]  # Your domain
SECRET_KEY = os.environ.get('SECRET_KEY')  # Use environment variable
DATABASES['default']['NAME'] = '/path/to/data/db.postgresql'  # PostgreSQL
HTTPS_ONLY = True  # Send HTTPS only
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
```

---

## 💡 Summary: Why These Practices Matter

| Practice | Benefit |
|----------|---------|
| Models/Views/Templates | Code organization |
| Foreign Keys | Data integrity |
| CSRF tokens | Security |
| ModelForm | DRY code |
| @login_required | Access control |
| Messages | User feedback |
| Template inheritance | Less code repetition |
| Pagination | Performance |
| Indexes | Speed |
| get_object_or_404 | Proper HTTP status |

---

## 📚 Further Learning

1. **Django Official Documentation**: Comprehensive and authoritative
2. **"Two Scoops of Django"**: Best practices book
3. **Real Python**: Detailed tutorials on Django topics
4. **Test-Driven Development**: Write tests first, code second

**Happy developing! 🎓**
