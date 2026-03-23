from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email field must be set.")

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.full_clean(exclude=["last_login"])
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("access_level", User.AccessLevel.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class EmploymentStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        PENDING = "pending", "Pending activation"
        SUSPENDED = "suspended", "Suspended"
        ALUMNI = "alumni", "Alumni"

    class AccessLevel(models.TextChoices):
        EMPLOYEE = "employee", "Employee"
        MANAGER = "manager", "Manager"
        MODERATOR = "moderator", "Moderator"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    display_name = models.CharField(max_length=150, blank=True)
    employee_code = models.CharField(max_length=32, blank=True)
    title = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=120, blank=True)
    phone_number = models.CharField(max_length=32, blank=True)
    employment_status = models.CharField(
        max_length=16,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.ACTIVE,
    )
    access_level = models.CharField(
        max_length=16,
        choices=AccessLevel.choices,
        default=AccessLevel.EMPLOYEE,
    )
    is_directory_visible = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_seen_at = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("email",)

    def save(self, *args, **kwargs):
        self.email = (self.email or "").lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.email

    @property
    def full_name(self):
        if self.display_name:
            return self.display_name
        joined = " ".join(part for part in [self.first_name, self.last_name] if part).strip()
        return joined or self.email

    @property
    def initials(self):
        if self.first_name or self.last_name:
            return f"{self.first_name[:1]}{self.last_name[:1]}".upper() or self.email[:2].upper()
        return self.full_name[:2].upper()

# Create your models here.
