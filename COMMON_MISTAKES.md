# ⚠️ Common Beginner Mistakes (And How to Avoid Them)

This guide shows common errors beginners make with Django and how to avoid them.

---

## 1. ❌ Forgetting {% csrf_token %} in Forms

### The Mistake
```html
<!-- WRONG - No CSRF token -->
<form method="POST" action="/skills/create/">
    <input type="text" name="title">
    <button type="submit">Create</button>
</form>
```

**Result:** Form won't submit, get 403 Forbidden error.

### The Fix
```html
<!-- CORRECT - With CSRF token -->
<form method="POST">
    {% csrf_token %}  <!-- Add this line! -->
    <input type="text" name="title">
    <button type="submit">Create</button>
</form>
```

**Why:** Protects against hackers trick-posting requests.

---

## 2. ❌ Storing Passwords in Plain Text

### The Mistake
```python
# NEVER DO THIS!
user.password = "mypassword123"
user.save()
```

**Result:** If database is hacked, all passwords exposed.

### The Fix
```python
# ALWAYS use this method
user.set_password("mypassword123")
user.save()
```

**Why:** `set_password()` hashes the password so even you can't read it.

---

## 3. ❌ Hardcoding URLs in Templates

### The Mistake
```html
<!-- WRONG - Hardcoded URL -->
<a href="/skills/browse/">Browse</a>
<a href="/skills/5/edit/">Edit</a>
<a href="/user/profile/">Profile</a>
```

**Problem:** If you change URLs in `urls.py`, links break everywhere.

### The Fix
```html
<!-- CORRECT - Dynamic URLs -->
<a href="{% url 'skill_list' %}">Browse</a>
<a href="{% url 'skill_edit' skill.id %}">Edit</a>
<a href="{% url 'profile' %}">Profile</a>
```

**Why:** Automatically updates when you change URLs.

---

## 4. ❌ Missing Permission Checks

### The Mistake
```python
# WRONG - Anyone can delete any skill!
def skill_delete(request, pk):
    skill = Skill.objects.get(pk=pk)
    skill.delete()
    return redirect('home')
```

**Problem:** User A can delete User B's skills!

### The Fix
```python
# CORRECT - Check ownership first
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    
    # Permission check
    if skill.owner != request.user:
        return HttpResponseForbidden("Not your skill!")
    
    skill.delete()
    return redirect('home')
```

**Why:** Prevents unauthorized access.

---

## 5. ❌ Not Using @login_required Decorator

### The Mistake
```python
# WRONG - Anyone can access, even not logged in
def dashboard(request):
    user_skills = request.user.skills.all()
    # What if request.user is AnonymousUser?
    return render(request, "dashboard.html", ...)
```

**Problem:** Crashes if not logged in. Confusing error.

### The Fix
```python
# CORRECT - Requires login
@login_required(login_url="login")
def dashboard(request):
    user_skills = request.user.skills.all()
    return render(request, "dashboard.html", ...)
```

**Why:** Automatically redirects to login if not authenticated.

---

## 6. ❌ Incorrect Foreign Key Management

### The Mistake
```python
# WRONG - Storing copies of data
class Skill(models.Model):
    title = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=100)  # Duplicates User!
    owner_email = models.CharField(max_length=100)  # Duplicate again!
```

**Problem:**
- Data duplication
- If user changes email, skill still has old one
- Lots of wasted database space

### The Fix
```python
# CORRECT - Use ForeignKey
class Skill(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # Access user info: skill.owner.username, skill.owner.email
```

**Why:** Single source of truth, automatic data consistency.

---

## 7. ❌ Migrations Problems

### The Mistake
```bash
# WRONG - Skip migrations, Django won't recognize new fields
# Install new package
pip install pillow

# Add field to model
# ... model code ...

# SKIP migrations and try to use immediately
python manage.py runserver
```

**Result:** "Column does not exist" error.

### The Fix
```bash
# CORRECT - Always run migrations after model changes
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

**Why:** Migrations create/modify database tables.

---

## 8. ❌ Using get() When You Don't Know If Object Exists

### The Mistake
```python
# WRONG - Crashes if skill doesn't exist
def skill_detail(request, pk):
    skill = Skill.objects.get(pk=pk)  # Raises error if not found
    return render(request, "detail.html", {"skill": skill})
```

**Result:** If user visits /skills/99999/, app crashes with ugly error.

### The Fix
```python
# CORRECT - Returns 404 if not found
def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk)  # Nice 404 page
    return render(request, "detail.html", {"skill": skill})
```

**Why:** User sees a proper 404 page, not a Python error.

---

## 9. ❌ Saving (commit=False) Without Calling save()

### The Mistake
```python
# WRONG - Changes not saved to database!
def create_view(request):
    form = MyForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)  # Don't save yet
        obj.owner = request.user
        # FORGOT to call obj.save()!
        return redirect('home')
```

**Result:** User thinks it's saved but nothing in database.

### The Fix
```python
# CORRECT - Call save() after modifying
def create_view(request):
    form = MyForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.owner = request.user
        obj.save()  # Don't forget!
        return redirect('home')
```

**Why:** Without this final `save()`, changes are lost.

---

## 10. ❌ Modifying QuerySets in Loops

### The Mistake
```python
# WRONG - Inefficient, hundreds of database queries!
for skill in Skill.objects.all():
    skill.view_count += 1
    skill.save()  # Database query for each skill!
```

### The Fix
```python
# CORRECT - Update all at once
Skill.objects.all().update(view_count=F('view_count') + 1)
# Just 1 database query!
```

**Why:** Much faster for large datasets.

---

## 11. ❌ Storing Files in the Media Folder (Production)

### The Mistake
```python
# Development might work, production will fail
class UserProfile(models.Model):
    profile_picture = models.ImageField(upload_to="profile_pics/")
```

In production, uploaded files disappear after each deployment!

### The Fix
Use external storage:
```python
# Use Django-storages with AWS S3, Azure, or Google Cloud
# Set in settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

**Why:** Production servers don't save local files permanently.

---

## 12. ❌ DEBUG = True in Production

### The Mistake
```python
# settings.py production
DEBUG = True  # HUGE SECURITY RISK!
```

**Problems:**
- Shows sensitive information on error pages
- Exposes secret key
- Hackers can see your code
- Reveals database structure

### The Fix
```python
# settings.py production
DEBUG = False
ALLOWED_HOSTS = ['yoursite.com']
```

**Why:** Production must hide all debug information.

---

## 13. ❌ Using Raw SQL Instead of ORM

### The Mistake
```python
# WRONG - Vulnerable to SQL injection!
search = request.GET.get('q')
results = Skill.objects.raw(f"SELECT * FROM skillfeed_skill WHERE title LIKE '%{search}%'")
# If search = "'; DROP TABLE skills; --" = DISASTER!
```

### The Fix
```python
# CORRECT - ORM parameterizes queries
search = request.GET.get('q')
results = Skill.objects.filter(title__icontains=search)
```

**Why:** ORM escapes special characters automatically.

---

## 14. ❌ Not Validating on Server Side

### The Mistake
```html
<!-- Wrong: Only validates on frontend -->
<form>
    <input type="email" required>
    <button>Submit</button>
</form>
```

Hackers can bypass frontend validation!

### The Fix
```python
# CORRECT: Server-side validation with Django Forms
class ContactForm(forms.Form):
    email = forms.EmailField()  # Validates on server
```

**Why:** Frontend validation is just for UX. Real validation happens on server.

---

## 15. ❌ Global Variables Instead of Database

### The Mistake
```python
# WRONG - Resets every time server restarts!
users_online = []

def track_user(request):
    users_online.append(request.user)  # Disappears on restart
```

### The Fix
```python
# CORRECT - Use database
class Activity(models.Model):
    user = models.ForeignKey(User)
    last_seen = models.DateTimeField(auto_now=True)

def track_user(request):
    activity, _ = Activity.objects.get_or_create(user=request.user)
    activity.save()  # Persists
```

**Why:** Database survives server restarts.

---

## 16. ❌ {% safe %} Without Escaping User Input

### The Mistake
```html
<!-- DANGEROUS! -->
{% load markdown %}
<div>{{ user_content|markdown|safe }}</div>
```

If user enters `<script>alert('hacked')</script>`, it runs!

### The Fix
```html
<!-- SAFE -->
<div>{{ user_content|markdown }}</div>
<!-- Django auto-escapes HTML -->
```

**Why:** Never use `|safe` with user input.

---

## 17. ❌ Mutable Default Arguments

### The Mistake
```python
# WRONG - Same list shared across all calls!
def add_skill(owner, tags=[]):
    tags.append("new-tag")
    return Skill.objects.create(owner=owner, tags=tags)

# First call: tags = ["new-tag"]
# Second call: tags = ["new-tag", "new-tag"]  # Unexpected!
```

### The Fix
```python
# CORRECT - Create new list each time
def add_skill(owner, tags=None):
    if tags is None:
        tags = []
    tags.append("new-tag")
    return Skill.objects.create(owner=owner, tags=tags)
```

**Why:** Mutable defaults are shared across calls.

---

## 18. ❌ Not Handling Empty/Null Data

### The Mistake
```python
# WRONG - Crashes if profile_picture is None
def show_picture(request):
    url = request.user.profile.profile_picture.url  # ERROR if None!
```

### The Fix
```html
<!-- CORRECT - Check if exists -->
{% if user.profile.profile_picture %}
    <img src="{{ user.profile.profile_picture.url }}">
{% else %}
    <img src="{% static 'images/default-avatar.png' %}">
{% endif %}
```

**Why:** Optional fields might be empty.

---

## 19. ❌ N+1 Query Problem

### The Mistake
```python
# WRONG - Multiple queries!
for skill in Skill.objects.all():
    print(skill.owner.username)  # Query database for EACH skill!
# If 1000 skills = 1001 queries!
```

### The Fix
```python
# CORRECT - One query with join
for skill in Skill.objects.select_related('owner'):
    print(skill.owner.username)  # Already have owner data
# Just 1 query!
```

**Why:** Much faster for large datasets.

---

## 20. ❌ Testing in Production

### The Mistake
```python
# WRONG - Testing directly on live site
# Create test accounts with real emails
# Post test skills
# Create test requests
```

**Problems:**
- Real users see test data
- Might accidentally delete real data
- Other developers confused

### The Fix
```bash
# Use separate database for testing
python manage.py test skillfeed.tests
```

**Why:** Tests should be isolated from real data.

---

## 🎓 Summary: 3 Golden Rules

1. **Always Check Permissions**: Before edit/delete, verify user owns resource
2. **Always Use Server-Side Validation**: Never trust frontend
3. **Always Use Django ORM**: Never raw SQL

Follow these and you'll avoid 80% of common Django mistakes!

---

**Questions?** Check `DJANGO_BEST_PRACTICES.md` for more details.
