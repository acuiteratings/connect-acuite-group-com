import uuid
from datetime import timedelta

from django.conf import settings
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
        extra_fields.setdefault("must_change_password", False)
        extra_fields.setdefault("password_changed_at", timezone.now())

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
    can_post_in_connect = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=True)
    password_changed_at = models.DateTimeField(blank=True, null=True)
    last_seen_at = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("email",)
        permissions = [
            ("manage_access_rights", "Can assign Connect access rights"),
            ("post_as_company", "Can post on behalf of the company"),
            ("disable_connect_posting", "Can disable posting access in Connect"),
        ]

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

    @property
    def password_due_at(self):
        if not self.password_changed_at:
            return None
        return self.password_changed_at + timedelta(
            days=getattr(settings, "AUTH_PASSWORD_MAX_AGE_DAYS", 90)
        )

    @property
    def password_change_required(self):
        if self.must_change_password:
            return True
        if not self.password_changed_at:
            return True
        return timezone.now() >= self.password_due_at

    @property
    def password_days_until_expiry(self):
        due_at = self.password_due_at
        if due_at is None:
            return None
        delta = due_at - timezone.now()
        return max(0, delta.days)

    @property
    def login_allowed(self):
        return (
            self.is_active
            and self.employment_status == self.EmploymentStatus.ACTIVE
        )

    @property
    def has_employee_access(self):
        if self.is_superuser:
            return True
        return self.login_allowed and self.access_level in {
            self.AccessLevel.EMPLOYEE,
            self.AccessLevel.MANAGER,
            self.AccessLevel.MODERATOR,
            self.AccessLevel.ADMIN,
        }

    @property
    def can_comment_in_connect(self):
        return self.has_employee_access

    @property
    def can_react_in_connect(self):
        return self.has_employee_access

    @property
    def can_create_connect_posts(self):
        return self.has_employee_access and self.can_post_in_connect

    @property
    def can_moderate_connect(self):
        if self.is_superuser:
            return True
        if not self.has_employee_access:
            return False
        if self.access_level in {self.AccessLevel.MODERATOR, self.AccessLevel.ADMIN}:
            return True
        if not self.is_staff:
            return False
        return self.has_perm("feed.moderate_post") or self.has_perm("feed.moderate_comment")

    @property
    def can_administer_connect(self):
        if self.is_superuser:
            return True
        if not self.has_employee_access:
            return False
        if self.access_level == self.AccessLevel.ADMIN:
            return True
        if not self.is_staff:
            return False
        return self.has_perm("accounts.manage_access_rights")

    @property
    def can_manage_access_rights(self):
        return self.can_administer_connect

    @property
    def can_post_as_company(self):
        if self.is_superuser:
            return True
        if not self.has_employee_access:
            return False
        if self.access_level == self.AccessLevel.ADMIN:
            return True
        if not self.is_staff:
            return False
        return self.has_perm("accounts.post_as_company")


class ExitProcess(models.Model):
    class Stage(models.TextChoices):
        NOTICE_RECEIVED = "notice_received", "Notice received"
        KNOWLEDGE_TRANSFER = "knowledge_transfer", "Knowledge transfer"
        CLEARANCE = "clearance", "Clearance"
        ALUMNI_CONVERSION = "alumni_conversion", "Alumni conversion"
        COMPLETED = "completed", "Completed"

    employee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exit_process",
    )
    initiated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="initiated_exit_processes",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="updated_exit_processes",
        null=True,
        blank=True,
    )
    resignation_date = models.DateField()
    last_working_day = models.DateField()
    stage = models.CharField(
        max_length=32,
        choices=Stage.choices,
        default=Stage.NOTICE_RECEIVED,
    )
    resignation_acknowledged = models.BooleanField(default=False)
    knowledge_transfer_completed = models.BooleanField(default=False)
    assets_returned = models.BooleanField(default=False)
    access_review_completed = models.BooleanField(default=False)
    alumni_transition_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "-created_at")
        permissions = [
            ("manage_exit_process", "Can manage employee exit processes"),
        ]

    def __str__(self):
        return f"Exit process for {self.employee.full_name}"

    @property
    def can_finalize(self):
        return (
            self.resignation_acknowledged
            and self.knowledge_transfer_completed
            and self.assets_returned
            and self.access_review_completed
        )

    def mark_completed(self):
        self.stage = self.Stage.COMPLETED
        self.alumni_transition_completed = True
        self.completed_at = timezone.now()


class LoginChallenge(models.Model):
    class Purpose(models.TextChoices):
        LOGIN = "login", "Login"

    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="login_challenges",
    )
    email = models.EmailField(db_index=True)
    purpose = models.CharField(max_length=16, choices=Purpose.choices, default=Purpose.LOGIN)
    code_hash = models.CharField(max_length=255)
    expires_at = models.DateTimeField(db_index=True)
    otp_sent_at = models.DateTimeField(default=timezone.now)
    otp_verified_at = models.DateTimeField(blank=True, null=True)
    password_verified_at = models.DateTimeField(blank=True, null=True)
    consumed_at = models.DateTimeField(blank=True, null=True)
    otp_attempts = models.PositiveSmallIntegerField(default=0)
    password_attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.email} challenge {self.public_id}"

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    @property
    def masked_email(self):
        local_part, _, domain = self.email.partition("@")
        if len(local_part) <= 2:
            masked_local = f"{local_part[:1]}*"
        else:
            masked_local = f"{local_part[:2]}{'*' * max(1, len(local_part) - 2)}"
        return f"{masked_local}@{domain}"


class TrustedAppLoginGrant(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trusted_login_grants",
    )
    client_id = models.CharField(max_length=80, db_index=True)
    redirect_uri = models.URLField(max_length=500)
    expires_at = models.DateTimeField(db_index=True)
    consumed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.client_id} grant {self.public_id}"

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at
