# Campus Skill Swap - Complete Django Student Marketplace

Welcome to **Campus Skill Swap**! A fully functional Django web application where students can post, discover, and exchange skills and services.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Virtual environment (included: `.venv`)

### Running the Server

```bash
# Navigate to project directory
cd c:\Users\diann\Documents\AIPython\campus_skill_swap

# Activate virtual environment (Windows)
.venv\Scripts\Activate.ps1

# Start development server
python manage.py runserver

# Access the app
# Home page: http://localhost:8000
# Admin panel: http://localhost:8000/admin
```

## 📋 Project Structure

```
campus_skill_swap/
├── skillswap_project/          # Django project configuration
│   ├── settings.py             # Configuration file
│   ├── urls.py                 # Main URL routing
│   ├── wsgi.py                 # Production server
│   └── asgi.py                 # Async server
│
├── skillfeed/                  # Main Django app
│   ├── models.py               # Database models
│   ├── views.py                # View functions (business logic)
│   ├── forms.py                # Django forms (400+ lines)
│   ├── urls.py                 # App URL routing
│   ├── admin.py                # Admin panel configuration
│   └── migrations/             # Database migration files
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template (all pages extend this)
│   └── skillfeed/
│       ├── home.html          # Home page
│       ├── skill_list.html    # Browse skills with search/filter
│       ├── skill_detail.html  # Individual skill page
│       ├── skill_form.html    # Create/edit skill form
│       ├── username_delete.html    # Confirm deletion
│       ├── login.html         # Login page
│       ├── register.html      # Registration page
│       ├── profile.html       # User profile edit
│       ├── dashboard.html     # User dashboard
│       ├── request_skill.html # Request a skill
│       └── respond_request.html # Respond to request
│
├── static/                     # Static files
│   └── css/
│       └── style.css          # Custom Bootstrap CSS (500+ lines)
│
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django CLI tool
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔑 Key Features

### ✅ User Authentication
- **Sign Up**: Create account with email validation
- **Log In**: Secure session-based authentication
- **Log Out**: Destroy session safely
- **Profile Management**: Edit bio, photo, phone, location

### 🎓 Skill Management (CRUD)
- **Create**: Post new skills with full details
- **Read**: Browse skills with search and filtering
- **Update**: Edit your skill posts
- **Delete**: Remove skills with confirmation
- **Details**: View comprehensive skill information

### 🔗 Skill Requests
- **Request Skills**: Send requests to other students
- **Respond**: Accept or decline requests with messages
- **Dashboard**: Track sent and received requests
- **Notifications**: See pending requests at a glance

### 🔍 Search & Filter
- Search by skill title or description
- Filter by category (Tutoring, Tech, Creative, Sports, etc.)
- Filter by price type (Free, Skill Exchange, Paid)
- Pagination with 12 skills per page

### 💰 Pricing Options
- **Free**: No charge for the skill
- **Skill Exchange**: Trade skills for other skills
- **Paid**: Set your own price per session

## 👤 Admin Account

Access the admin panel at: `http://localhost:8000/admin`

```
Username: admin
Password: admin123
```

### Admin Features
- Manage users and profiles
- Review all skill posts
- Monitor skill requests
- Delete inappropriate content

## 📱 Database Models Explained

### 1. **UserProfile**
Extends Django's built-in User model with extra fields:
- Bio, profile picture, phone, location
- Created timestamp for account age

### 2. **Skill**
The core marketplace item:
- Title, description, category
- Price type (free/exchange/paid) and amount
- Owner (ForeignKey to User)
- Contact preference and availability
- View counter for popularity

### 3. **SkillRequest**
Represents student-to-student connections:
- Requester (student asking) & responder (student offering)
- Message and status (pending/accepted/declined/completed)
- Response with reply message
- Timestamps for both request and response

## 🎯 Common Workflows

### Posting a Skill

1. Log in (if not already)
2. Click "Post Skill" in navbar
3. Fill in skill details:
   - Title: "Python Tutoring"
   - Description: What you offer
   - Category: Select category
   - Price: free/exchange/paid
   - Contact: How to reach you
4. Click "Create Skill"
5. Skill appears on the Browse page

### Requesting a Skill

1. Browse skills: `http://localhost:8000/skills/browse/`
2. Find a skill you want
3. Click "View" to see details
4. Click "Request This Skill"
5. Write a message explaining your interest
6. Click "Send Request"
7. Skill owner receives notification in Dashboard

### Responding to a Request

1. Go to Dashboard
2. View "Requests Received" tab
3. Click "Respond" on a pending request
4. Choose: Accept or Decline
5. Write your response message
6. Click "Send Response"

## 🛠️ Development Tips

### Creating Superusers for Testing
```bash
python manage.py createsuperuser
# Username: testadmin
# Email: test@example.com
# Password: [enter password]
```

### Creating Sample Data
```bash
python manage.py shell

# Inside the shell:
from django.contrib.auth.models import User
from skillfeed.models import UserProfile, Skill

# Create a test user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='password123',
    first_name='Test',
    last_name='User'
)

# Create their profile
profile = UserProfile.objects.create(user=user)

# Create a skill
skill = Skill.objects.create(
    owner=user,
    title='Web Development Tutoring',
    description='Learn HTML, CSS, and JavaScript',
    category='tech',
    price_type='free',
    contact_preference='email'
)
```

### View Database Using Django Shell
```bash
python manage.py shell

# See all skills
from skillfeed.models import Skill
Skill.objects.all()

# See all users
from django.contrib.auth.models import User
User.objects.all()

# See skill requests
from skillfeed.models import SkillRequest
SkillRequest.objects.all()
```

### Reset Database
```bash
# DELETE all data and start fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 🔒 Security Features

✅ **CSRF Protection**: All forms include {% csrf_token %}
✅ **Password Hashing**: Django's built-in password security
✅ **SQL Injection Prevention**: ORM protects against injection attacks
✅ **Permission Checks**: Users can only edit/delete their own content
✅ **Authentication Required**: Login required for protected views
✅ **Session Security**: Secure session cookies
✅ **XSS Protection**: Template auto-escaping prevents script injection

## 🐛 Common Errors & Solutions

### Error: "No module named 'skillfeed'"
**Solution**: Make sure virtual environment is activated and skillfeed is in INSTALLED_APPS

### Error: "TemplateDoesNotExist"
**Solution**: Check templates folder structure:
```
templates/
├── base.html
└── skillfeed/
    ├── home.html
    ├── login.html
    └── ... other templates
```

### Error: "migrate: table already exists"
**Solution**: 
```bash
rm db.sqlite3
python manage.py migrate
```

### Error: "No such table: skillfeed_skill"
**Solution**: 
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📚 Understanding the Code

### Views (skillfeed/views.py)
- **Function-based views**: Each function handles one URL/feature
- **@login_required**: Decorator ensures only logged-in users access
- **get_object_or_404()**: Returns 404 if object doesn't exist
- **messages framework**: Shows success/error notifications to users
- **Permission checks**: Verify user owns the resource before editing

### Forms (skillfeed/forms.py)
- **UserCreationForm**: Built-in Django form for user registration
- **ModelForm**: Auto-generates form from model definition
- **Custom validation**: clean_() methods validate data before saving
- **Bootstrap classes**: All inputs styled with Bootstrap

### Templates
- **Template inheritance**: All pages extend base.html
- **Django template tags**: {% if %}, {% for %}, {% url %}, {% load static %}
- **Template filters**: |truncatewords, |date, |pluralize
- **Bootstrap components**: Cards, modals, forms, pagination

## 🚀 Next Steps / Enhancements

Consider adding these features:

1. **Email Notifications**: Notify users when they get requests
2. **Ratings & Reviews**: Students rate each other after exchanges
3. **Messaging System**: Direct messaging between students
4. **Skill Recommendations**: Suggest similar skills
5. **Advanced Search**: Filter by date, rating, distance
6. **Image Upload**: Profile pictures and skill galleries
7. **Calendar Integration**: Schedule skill sessions
8. **Payment Integration**: Stripe for paid skills
9. **Mobile App**: React Native or Flutter app
10. **API**: REST API for mobile and third-party integration

## 📖 Django Concepts Used

- **ORM (Object-Relational Mapping)**: Query database with Python objects
- **Models**: Define database structure
- **Views**: Handle HTTP requests, return responses
- **Forms**: Validate user input
- **Templates**: HTML with template tags
- **URL Routing**: Map URLs to views
- **Middleware**: Process requests before reaching views
- **Authentication**: Built-in user login system
- **Admin Site**: Automatic admin interface
- **Migrations**: Version control for database schema
- **Messages Framework**: User notifications
- **Pagination**: Split large lists into pages
- **Decorators**: @login_required, @admin_required

## 🎓 Learning Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django for Beginners**: A complete book (free online)
- **Real Python Django Tutorials**: https://realpython.com/tutorials/django/
- **MDN Web Docs**: Django backend development

## 💡 Best Practices Implemented

1. ✅ **DRY (Don't Repeat Yourself)**: Code reuse through template inheritance
2. ✅ **MVC Pattern**: Models, Views, Templates separation
3. ✅ **SOLID Principles**: Single responsibility, open/closed
4. ✅ **Clean Code**: Meaningful names, comments, readable structure
5. ✅ **Security First**: CSRF tokens, password hashing, permission checks
6. ✅ **User-Centric Design**: Clear navigation, helpful messages
7. ✅ **Responsive Design**: Works on mobile and desktop
8. ✅ **Performance**: Database query optimization, pagination

## 📞 Troubleshooting

**Server won't start?**
```bash
# Kill existing process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Try different port
python manage.py runserver 8001
```

**Database issues?**
```bash
# Check migrations
python manage.py showmigrations

# Create missing migrations
python manage.py makemigrations

# Apply all migrations
python manage.py migrate
```

**Static files not loading?**
```bash
# Collect static files for production
python manage.py collectstatic --noinput

# For development, they should load automatically
```

## 📄 License

This educational project is free to use and modify.

---

**Happy skill swapping! 🎓**
