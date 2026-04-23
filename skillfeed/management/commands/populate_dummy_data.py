from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from skillfeed.models import UserProfile, Skill


class Command(BaseCommand):
    help = "Populate database with 5 dummy students and their skills"

    def handle(self, *args, **options):
        # Clear existing data (optional)
        # User.objects.all().delete()
        
        # Define 5 students with their details
        students_data = [
            {
                "username": "alex_tech",
                "email": "alex@campus.edu",
                "first_name": "Alex",
                "last_name": "Chen",
                "bio": "Full-stack developer passionate about web technologies",
                "location": "Computer Science Building",
            },
            {
                "username": "emma_creative",
                "email": "emma@campus.edu",
                "first_name": "Emma",
                "last_name": "Rodriguez",
                "bio": "Graphic designer and digital artist with 3 years experience",
                "location": "Arts Center",
            },
            {
                "username": "marcus_fit",
                "email": "marcus@campus.edu",
                "first_name": "Marcus",
                "last_name": "Thompson",
                "bio": "Personal trainer and fitness enthusiast. Let's get fit together!",
                "location": "Sports Complex",
            },
            {
                "username": "sarah_music",
                "email": "sarah@campus.edu",
                "first_name": "Sarah",
                "last_name": "Kim",
                "bio": "Piano teacher and music composition student",
                "location": "Music Hall",
            },
            {
                "username": "james_languages",
                "email": "james@campus.edu",
                "first_name": "James",
                "last_name": "Wilson",
                "bio": "Fluent in Spanish and French, studying linguistics",
                "location": "Language Center",
            },
        ]

        # Skills data: each student gets 2-3 skills with variety
        skills_data = [
            # Alex's Tech Skills
            {
                "owner_username": "alex_tech",
                "title": "Python Programming Tutoring",
                "description": "Learn Python from basics to advanced. I focus on clean code and best practices. Sessions are 1 hour each.",
                "category": "tech",
                "price_type": "exchange",
                "contact_preference": "zoom",
            },
            {
                "owner_username": "alex_tech",
                "title": "Web Development with Django",
                "description": "Build full-stack web applications using Django and React. Great for beginners and intermediate learners.",
                "category": "tech",
                "price_type": "paid",
                "price_amount": "25.00",
                "contact_preference": "zoom",
            },
            {
                "owner_username": "alex_tech",
                "title": "JavaScript & React Help",
                "description": "Debug your React code, learn hooks, state management. Flexible scheduling available.",
                "category": "tech",
                "price_type": "free",
                "contact_preference": "chat",
            },
            # Emma's Creative Skills
            {
                "owner_username": "emma_creative",
                "title": "Logo Design & Branding",
                "description": "Need a professional logo? I create custom designs tailored to your brand identity.",
                "category": "design",
                "price_type": "paid",
                "price_amount": "50.00",
                "contact_preference": "email",
            },
            {
                "owner_username": "emma_creative",
                "title": "Digital Art Lessons",
                "description": "Learn digital drawing and painting using Photoshop and Procreate. All skill levels welcome!",
                "category": "creativity",
                "price_type": "exchange",
                "contact_preference": "inperson",
            },
            {
                "owner_username": "emma_creative",
                "title": "Adobe Creative Suite Training",
                "description": "Master Photoshop, Illustrator, and InDesign. Customized lessons based on your goals.",
                "category": "tech",
                "price_type": "paid",
                "price_amount": "35.00",
                "contact_preference": "zoom",
            },
            # Marcus's Fitness Skills
            {
                "owner_username": "marcus_fit",
                "title": "Personal Training Sessions",
                "description": "1-on-1 fitness coaching. I create customized workout plans based on your goals and fitness level.",
                "category": "sports",
                "price_type": "paid",
                "price_amount": "30.00",
                "contact_preference": "inperson",
            },
            {
                "owner_username": "marcus_fit",
                "title": "Basketball Coaching",
                "description": "Improve your basketball skills: ball handling, shooting, defense. All levels from beginner to advanced.",
                "category": "sports",
                "price_type": "exchange",
                "contact_preference": "inperson",
            },
            {
                "owner_username": "marcus_fit",
                "title": "Nutrition & Meal Planning",
                "description": "Get customized nutrition advice and meal plans to achieve your fitness goals.",
                "category": "other",
                "price_type": "free",
                "contact_preference": "chat",
            },
            # Sarah's Music Skills
            {
                "owner_username": "sarah_music",
                "title": "Piano Lessons for Beginners",
                "description": "Learn to play piano from scratch. Lessons include music theory and practice techniques.",
                "category": "music",
                "price_type": "paid",
                "price_amount": "20.00",
                "contact_preference": "inperson",
            },
            {
                "owner_username": "sarah_music",
                "title": "Music Composition & Theory",
                "description": "Create original music pieces. I teach music theory, composition, and songwriting fundamentals.",
                "category": "music",
                "price_type": "exchange",
                "contact_preference": "zoom",
            },
            {
                "owner_username": "sarah_music",
                "title": "Advanced Piano Techniques",
                "description": "For experienced pianists: classical repertoire, improvisation, and advanced technique refinement.",
                "category": "music",
                "price_type": "paid",
                "price_amount": "35.00",
                "contact_preference": "inperson",
            },
            # James's Language Skills
            {
                "owner_username": "james_languages",
                "title": "Spanish Conversation Practice",
                "description": "Improve your Spanish speaking skills through real conversations. Native-level pronunciation guidance.",
                "category": "languages",
                "price_type": "exchange",
                "contact_preference": "zoom",
            },
            {
                "owner_username": "james_languages",
                "title": "French Language Tutoring",
                "description": "Learn French from A1 to B2 level. Grammar, vocabulary, pronunciation, and cultural insights included.",
                "category": "languages",
                "price_type": "paid",
                "price_amount": "22.00",
                "contact_preference": "zoom",
            },
            {
                "owner_username": "james_languages",
                "title": "TOEFL & IELTS Test Prep",
                "description": "Prepare for standardized English tests. I focus on test-taking strategies and all four skills.",
                "category": "languages",
                "price_type": "paid",
                "price_amount": "28.00",
                "contact_preference": "zoom",
            },
        ]

        # Create users and profiles
        for student in students_data:
            # Create or get user
            user, created = User.objects.get_or_create(
                username=student["username"],
                defaults={
                    "email": student["email"],
                    "first_name": student["first_name"],
                    "last_name": student["last_name"],
                },
            )

            # Create or update profile
            profile, profile_created = UserProfile.objects.get_or_create(user=user)
            profile.bio = student["bio"]
            profile.location = student["location"]
            profile.save()

            status = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{status} user: {user.get_full_name()} ({user.username})"
                )
            )

        # Create skills
        for skill_data in skills_data:
            owner = User.objects.get(username=skill_data.pop("owner_username"))
            skill, created = Skill.objects.get_or_create(
                owner=owner, title=skill_data["title"], defaults=skill_data
            )
            status = "Created" if created else "Already exists"
            self.stdout.write(
                self.style.SUCCESS(f"{status} skill: {skill.title} by {owner.username}")
            )

        self.stdout.write(
            self.style.SUCCESS(
                "\n✅ Successfully populated database with 5 students and 15 skills!"
            )
        )
