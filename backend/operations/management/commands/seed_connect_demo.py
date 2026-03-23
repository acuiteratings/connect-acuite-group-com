from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from directory.models import DirectoryProfile
from feed.models import Comment, Post
from operations.models import AnalyticsEvent
from operations.services import record_analytics_event


class Command(BaseCommand):
    help = "Seed local Acuite Connect demo data for users, directory records, posts, and comments."

    def handle(self, *args, **options):
        users = {}
        user_specs = [
            {
                "email": "rahul.mehta@acuite.in",
                "first_name": "Rahul",
                "last_name": "Mehta",
                "title": "Senior Analyst - Ratings",
                "department": "Ratings",
                "location": "Mumbai",
                "employee_code": "ACU1001",
                "access_level": User.AccessLevel.MANAGER,
            },
            {
                "email": "neha.srinivasan@acuite.in",
                "first_name": "Neha",
                "last_name": "Srinivasan",
                "title": "VP - Research",
                "department": "Research",
                "location": "Mumbai",
                "employee_code": "ACU1021",
                "access_level": User.AccessLevel.MODERATOR,
                "is_staff": True,
            },
            {
                "email": "karthik.iyer@acuite.in",
                "first_name": "Karthik",
                "last_name": "Iyer",
                "title": "Associate Analyst - Ratings",
                "department": "Ratings",
                "location": "Mumbai",
                "employee_code": "ACU1048",
            },
            {
                "email": "priya.sharma@acuite.in",
                "first_name": "Priya",
                "last_name": "Sharma",
                "title": "Senior Analyst - Financial Institutions",
                "department": "Ratings",
                "location": "Delhi",
                "employee_code": "ACU1007",
            },
            {
                "email": "people.team@acuite.in",
                "first_name": "People",
                "last_name": "Team",
                "display_name": "People Team",
                "title": "People Operations",
                "department": "HR",
                "location": "Mumbai",
                "employee_code": "ACUHR01",
                "access_level": User.AccessLevel.MODERATOR,
                "is_staff": True,
            },
        ]

        for spec in user_specs:
            email = spec["email"]
            defaults = {key: value for key, value in spec.items() if key != "email"}
            user, _ = User.objects.update_or_create(email=email, defaults=defaults)
            user.set_unusable_password()
            user.save(update_fields=["password"])
            users[email] = user

        profile_specs = [
            {
                "email": "rahul.mehta@acuite.in",
                "manager": None,
                "city": "Mumbai",
                "office_location": "Head Office",
                "work_mode": DirectoryProfile.WorkMode.HYBRID,
                "phone_extension": "214",
                "expertise": "Infrastructure and structured credit",
                "skills": ["rating committees", "credit memos", "portfolio reviews"],
                "bio": "Leads surveillance workflows and mentors new analysts.",
            },
            {
                "email": "neha.srinivasan@acuite.in",
                "manager": None,
                "city": "Mumbai",
                "office_location": "Head Office",
                "work_mode": DirectoryProfile.WorkMode.HYBRID,
                "phone_extension": "109",
                "expertise": "Sector research and institutional knowledge systems",
                "skills": ["research notes", "knowledge management", "comms"],
                "bio": "Owns research publishing standards and editorial reviews.",
            },
            {
                "email": "karthik.iyer@acuite.in",
                "manager": "rahul.mehta@acuite.in",
                "city": "Mumbai",
                "office_location": "Head Office",
                "work_mode": DirectoryProfile.WorkMode.ONSITE,
                "phone_extension": "217",
                "expertise": "NBFC and financial institution analysis",
                "skills": ["spread analysis", "rating packs", "monitoring"],
                "bio": "Focuses on NBFC surveillance and committee support.",
            },
            {
                "email": "priya.sharma@acuite.in",
                "manager": "rahul.mehta@acuite.in",
                "city": "Delhi",
                "office_location": "Delhi Office",
                "work_mode": DirectoryProfile.WorkMode.HYBRID,
                "phone_extension": "311",
                "expertise": "Financial institutions coverage",
                "skills": ["bank ratings", "mentoring", "client discussions"],
                "bio": "Five-year Acuite veteran supporting financial institutions coverage.",
            },
        ]

        for spec in profile_specs:
            manager_email = spec.pop("manager")
            DirectoryProfile.objects.update_or_create(
                user=users[spec.pop("email")],
                defaults={
                    **spec,
                    "manager": users.get(manager_email) if manager_email else None,
                },
            )

        post_specs = [
            {
                "title": "Town Hall - Q4 results presentation",
                "body": (
                    "Join us on March 25 at 4:00 PM in the Mumbai auditorium. "
                    "Leadership will share Q4 results, priorities for the new quarter, "
                    "and the first roadmap for Acuite Connect."
                ),
                "kind": Post.PostType.ANNOUNCEMENT,
                "visibility": Post.Visibility.COMPANY,
                "moderation_status": Post.ModerationStatus.PUBLISHED,
                "pinned": True,
                "author": users["people.team@acuite.in"],
            },
            {
                "title": "Infrastructure outlook for FY27 is now live",
                "body": (
                    "The capex cycle is showing real momentum and there are important "
                    "credit quality signals emerging in mid-market infrastructure. "
                    "The note is now in the research portal."
                ),
                "kind": Post.PostType.RESOURCE,
                "visibility": Post.Visibility.COMPANY,
                "moderation_status": Post.ModerationStatus.PUBLISHED,
                "author": users["neha.srinivasan@acuite.in"],
            },
            {
                "title": "Welcome aboard, Arjun Nair",
                "body": (
                    "Arjun joins as Analyst - Structured Finance in Mumbai. "
                    "Previously with CRISIL, he brings three years of securitisation ratings experience."
                ),
                "kind": Post.PostType.UPDATE,
                "visibility": Post.Visibility.COMPANY,
                "moderation_status": Post.ModerationStatus.PUBLISHED,
                "author": users["people.team@acuite.in"],
            },
        ]

        for spec in post_specs:
            post, _ = Post.objects.update_or_create(
                title=spec["title"],
                defaults={
                    **spec,
                    "allow_comments": True,
                    "published_at": timezone.now(),
                },
            )
            if post.title == "Infrastructure outlook for FY27 is now live":
                Comment.objects.update_or_create(
                    post=post,
                    author=users["rahul.mehta@acuite.in"],
                    body="Please pin this in the Knowledge Hub shortlist for the beta.",
                    defaults={"moderation_status": Comment.ModerationStatus.PUBLISHED},
                )
            if post.title == "Town Hall - Q4 results presentation":
                Comment.objects.update_or_create(
                    post=post,
                    author=users["karthik.iyer@acuite.in"],
                    body="Can we add five minutes for a Connect walkthrough in the agenda?",
                    defaults={"moderation_status": Comment.ModerationStatus.PUBLISHED},
                )

        pending_post, _ = Post.objects.update_or_create(
            title="Need review: Chennai office seating feedback",
            defaults={
                "author": users["rahul.mehta@acuite.in"],
                "body": "Sharing initial seating feedback from the Chennai visit before broad circulation.",
                "kind": Post.PostType.UPDATE,
                "visibility": Post.Visibility.COMPANY,
                "allow_comments": True,
                "moderation_status": Post.ModerationStatus.PENDING_REVIEW,
                "published_at": None,
            },
        )
        Comment.objects.update_or_create(
            post=pending_post,
            author=users["karthik.iyer@acuite.in"],
            body="Happy to tighten this note once leadership guidance is in.",
            defaults={"moderation_status": Comment.ModerationStatus.PENDING_REVIEW},
        )
        if not AnalyticsEvent.objects.filter(
            category="seed",
            event_name="demo_data_loaded",
        ).exists():
            record_analytics_event(
                "seed",
                "demo_data_loaded",
                actor=users["people.team@acuite.in"],
                metadata={"users": len(users), "posts": Post.objects.count()},
            )
        self.stdout.write(self.style.SUCCESS("Acuité Connect demo data seeded successfully."))
