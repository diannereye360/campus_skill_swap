# Getting Started with Campus Skill Swap

A step-by-step guide for running, testing, and understanding the application.

## 🎯 Step 1: Start the Server

Open PowerShell in the project directory:

```powershell
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Start server
python manage.py runserver
```

You should see:
```
Django version 4.2, using settings 'skillswap_project.settings'
Starting development server at http://127.0.0.1:8000/
```

**✅ Server is running!** Leave this window open.

---

## 🌐 Step 2: Access the Application

Open your browser and visit these URLs:

### Home Page
http://localhost:8000

Shows recent skills and statistics.

### Admin Panel
http://localhost:8000/admin

**Login with:**
- Username: `admin`
- Password: `admin123`

From here you can:
- View all users
- View all skills
- Delete inappropriate content
- Manage the entire database

---

## 👤 Step 3: Create Your First User Account

### Option A: Using the Web App (Recommended for Testing)

1. Go to http://localhost:8000
2. Click "Sign Up"
3. Fill in the form:
   - Username: `john_doe`
   - Email: `john@example.com`
   - Password: `SecurePass123!`
   - Confirm password: `SecurePass123!`
4. Click "Create Account"
5. You should be redirected to login page
6. Log in with your new credentials
7. You should see your dashboard

### Option B: Using Django Admin

1. Go to http://localhost:8000/admin
2. Log in with admin credentials
3. Click "Users" in the left sidebar
4. Click "Add User+"
5. Enter username and password
6. Save and you can add more information

---

## 📝 Step 4: Post Your First Skill

1. Make sure you're logged in
2. Click "Post Skill" in the navigation bar
3. Fill in the skill details:

```
Skill Title: "Python Programming Tutoring"
Description: "I can teach you Python basics including:
  - Variables and data types
  - Functions and classes
  - Web frameworks like Django
  
  I have 3 years of programming experience.
  Sessions are 1 hour each."

Category: "Technology"
Price Type: "Free"
Contact Preference: "Email"
☑ This skill is available now
```

4. Click "Create Skill"
5. You'll see your new skill posted!

---

## 🔍 Step 5: Browse and Search Skills

1. Click "Browse Skills" in navbar
2. Try these searches:
   - Search for skills: type "Python"
   - Filter by category: select "Technology"
   - Filter by price: select "Free"
3. Click "Filter" to apply
4. Click "View" on any skill to see details

---

## 📬 Step 6: Request a Skill

### On Another Account (for testing):

1. Create a second test account:
   - Username: `jane_doe`
   - Password: `SecurePass123!`
2. Log in as jane_doe
3. Click "Browse Skills"
4. Find the skill posted by john_doe
5. Click "View"
6. Click "Request This Skill"
7. Write a message:
   ```
   Hi! I'm very interested in learning Python.
   I'm available weekends after 2 PM.
   Can we meet for 1-hour sessions?
   Thanks!
   ```
8. Click "Send Request"
9. Notification appears in your dashboard

---

## ✅ Step 7: Respond to Requests

### Responding as the Skill Owner:

1. Log back in as john_doe
2. Click "Dashboard"
3. Click "Requests Received" tab
4. You should see jane_doe's request
5. Click "Respond"
6. Choose "Accept Request"
7. Write your response:
   ```
   Great! I'd love to teach you Python.
   I'm available Saturdays at 3 PM.
   Let's meet at the library or via Zoom.
   Here's my email: john@example.com
   ```
8. Click "Send Response"
9. jane_doe will see your acceptance in her dashboard

---

## 👤 Step 8: Edit Your Profile

1. Click your username in navbar (top right)
2. Click "My Profile"
3. You can fill in:
   - Bio: "Computer Science student interested in teaching"
   - Phone: "+1-555-123-4567" (optional)
   - Location: "Downtown Campus"
   - Profile Picture: Upload a photo
4. Click "Save Changes"

---

## 🔐 Step 9: Log Out and Back In

Test the authentication system:

1. Click your username in navbar
2. Click "Logout"
3. You should be on home page (logged out)
4. Click "Log In"
5. Enter your credentials
6. Click "Log In"
7. You should be in your dashboard

---

## 📊 Understanding the Dashboard

Your dashboard shows:

### Quick Stats (Top)
- **Skills Posted**: How many you've created
- **Pending Requests**: Requests waiting for your response
- **Requests Made**: How many you've sent to others

### Requests Received
Skills you've posted that others want to use:
- Shows requester name and skill
- Shows status: Pending, Accepted, Declined
- Click "Respond" to reply

### Requests Made
Skills you've requested from others:
- Shows the skill you want
- Shows status: Pending, Accepted, Declined
- See their response message

### My Skills
All skills you've posted:
- View, Edit, or Delete each skill
- See if it's available or not
- See view count

---

## 🎓 Understanding the Database

### Models (Defined in skillfeed/models.py)

```
User (Django built-in)
├── username: "john_doe"
├── email: "john@example.com"
└── Profile (UserProfile - one per user)
    └── bio: "CS student"

User
└── Skills (can have many)
    ├── Skill 1: "Python Tutoring"
    ├── Skill 2: "Guitar Lessons"
    └── Skill 3: "Math Help"
        ├── SkillRequest 1: From jane_doe
        ├── SkillRequest 2: From bob_smith
        └── SkillRequest 3: From alice_wang
```

### How Data Is Connected

1. Every Skill has an owner (User)
2. Every SkillRequest connects:
   - A requester (User who wants)
   - A skill (What they want)
   - A responder (User who offers) = skill owner
3. Every User can have one Profile

---

## 🧪 Testing Features

### Test 1: Can't Edit Others' Skills

1. Post a skill as john_doe
2. Log in as jane_doe
3. View john_doe's skill
4. Try to manually visit: `/skills/1/edit/`
5. You should see: "You can't edit skills you don't own!"

**Why?** Permission check in the view prevents unauthorized access.

### Test 2: Search/Filter Works

1. Go to "Browse Skills"
2. Type: "Python" in search
3. Should show only skills with "Python"
4. Try filtering by category, then price type
5. Combinations work together

**Why?** Database queries with Q() objects filter results.

### Test 3: Form Validation

1. Try posting a skill but leave required fields blank
2. Form shows errors
3. Try posting with paid price type but no price amount
4. Custom validation prevents this

**Why?** Django forms validate before saving to database.

---

## 📁 Project File Structure Explained

### Where to Find Things

| Want to... | Look in... |
|-----------|-----------|
| Change database fields | `skillfeed/models.py` |
| Add new views/pages | `skillfeed/views.py` |
| Modify forms | `skillfeed/forms.py` |
| Change URLs | `skillfeed/urls.py` + `skillswap_project/urls.py` |
| Edit HTML pages | `templates/skillfeed/` |
| Style pages | `static/css/style.css` |
| Admin customization | `skillfeed/admin.py` |

---

## 🐛 Troubleshooting

### Problem: "Page not found (404)"
**Solution:** Check URL spelling. Visit `/admin` to see what URLs exist.

### Problem: "TemplateDoesNotExist"
**Solution:** Make sure file is in correct folder structure:
```
templates/
└── skillfeed/
    └── page_name.html  ← Must be in skillfeed folder!
```

### Problem: Form won't submit
**Solution:** 
1. Check you included {% csrf_token %}
2. Inspect the form - do required fields have values?
3. Check console for JavaScript errors

### Problem: Can't upload profile picture
**Solution:** 
1. Check Pillow is installed: `pip list | grep Pillow`
2. File size should be < 5MB
3. File should be JPG, PNG, or GIF

### Problem: Changes don't appear
**Solution:** 
1. Reload browser: Ctrl+Shift+R (hard refresh)
2. Clear browser cache
3. Restart Django server: Ctrl+C then re-run command

---

## 🎨 Customization Ideas

### Change Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #0d6efd;  /* Change this */
}
```

### Add New Skill Category
Edit `skillfeed/models.py`:
```python
CATEGORY_CHOICES = [
    ("tutoring", "Tutoring"),
    ("tech", "Technology"),
    ("cooking", "Cooking"),  # Add this line
]
```
Then run:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Change Contact Preferences
Edit `skillfeed/models.py`:
```python
CONTACT_CHOICES = [
    ("email", "Email"),
    ("phone", "Phone"),
    ("telegram", "Telegram"),  # Add this
]
```

---

## 📚 Next Learning Steps

1. **Understand Models**: Read `skillfeed/models.py` and comments
2. **Understand Views**: Trace through `skillfeed/views.py`
3. **Understand Templates**: Look at `templates/skillfeed/home.html`
4. **Try Modifying Code**: Add a new field to Skill model
5. **Create Test Data**: Use Django shell to create users/skills
6. **Read Best Practices**: Check `DJANGO_BEST_PRACTICES.md`

---

## 🎓 Learning by Doing

### Challenge 1: Add "Rating" Feature
- Modify Skill model: add `avg_rating` field
- Users can rate skills from 1-5 stars
- Total rating shows on skill detail page

### Challenge 2: Add "Favorites"
- Create a new model: `FavoriteSkill`
- Users can favorite skills
- View favorites in dashboard

### Challenge 3: Add User Search
- Create a "Find Students" page
- Search users by username
- View other users' profiles and skills

---

## 💬 Key Terminology

| Term | Meaning |
|------|---------|
| **View** | Function that handles a request and returns HTML |
| **Model** | Python class that defines database table structure |
| **Form** | Class that validates user input and generates HTML |
| **Migration** | File that changes database structure |
| **Slug** | URL-friendly version of a name (e.g., "python-tutoring") |
| **QuerySet** | List of database records from a query |
| **Template** | HTML file with Django template tags |
| **Decorator** | Function modifier (e.g., @login_required) |
| **ForeignKey** | Reference to another table's record |
| **Context** | Dictionary of data passed to template |

---

## 🎯 Success Checklist

- ✅ Server starts without errors
- ✅ Can create account
- ✅ Can log in and out
- ✅ Can post a skill
- ✅ Can browse and filter skills
- ✅ Can request a skill
- ✅ Can respond to requests
- ✅ Admin panel works with admin account
- ✅ Can edit your profile
- ✅ Dashboard shows all your data

**If all ✅, your app is working! 🎉**

---

Enjoy building with Django! 🚀
