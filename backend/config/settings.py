import os
import secrets
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

try:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
except ImportError:  # pragma: no cover - optional dependency for production only
    sentry_sdk = None
    DjangoIntegration = None

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")


def env_list(name, default=""):
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]

def _load_build_number():
    build_number_file = PROJECT_ROOT / ".build-number"
    if build_number_file.exists():
        return build_number_file.read_text(encoding="utf-8").strip()
    return ""


render_external_host = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
database_url = os.getenv("DATABASE_URL", "").strip()
RUNNING_LOCALLY = not (render_external_host or database_url or os.getenv("RENDER", "").strip())
DEBUG = os.getenv("DJANGO_DEBUG", "true" if RUNNING_LOCALLY else "false").lower() == "true"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "").strip()
if not SECRET_KEY:
    if RUNNING_LOCALLY or DEBUG:
        SECRET_KEY = secrets.token_urlsafe(32)
    else:
        raise RuntimeError("DJANGO_SECRET_KEY must be set when DEBUG is false.")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        ",".join(
            host
            for host in [
                "127.0.0.1",
                "localhost",
                "testserver",
                "connect.acuite-group.com",
                render_external_host,
            ]
            if host
        ),
    ).split(",")
    if host.strip()
]
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
SENTRY_DSN = os.getenv("SENTRY_DSN", "").strip()
SENTRY_ENVIRONMENT = os.getenv("SENTRY_ENVIRONMENT", "development").strip() or "development"
SENTRY_TRACES_SAMPLE_RATE = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0"))
SENTRY_ENABLED = bool(SENTRY_DSN and sentry_sdk)
APP_BUILD_NUMBER = (
    _load_build_number()
    or os.getenv("APP_BUILD_NUMBER", "1.0000001").strip()
    or "1.0000001"
)
APP_BUILD_CREDIT = os.getenv(
    "APP_BUILD_CREDIT",
    "Built with care by Sankar Chakraborti",
).strip() or "Built with care by Sankar Chakraborti"
AUTH_PASSWORD_MAX_AGE_DAYS = int(os.getenv("AUTH_PASSWORD_MAX_AGE_DAYS", "90"))
AUTH_OTP_TTL_MINUTES = int(os.getenv("AUTH_OTP_TTL_MINUTES", "10"))
AUTH_OTP_CODE_LENGTH = int(os.getenv("AUTH_OTP_CODE_LENGTH", "6"))
AUTH_OTP_RESEND_COOLDOWN_SECONDS = int(
    os.getenv("AUTH_OTP_RESEND_COOLDOWN_SECONDS", "60")
)
AUTH_OTP_MAX_ATTEMPTS = int(os.getenv("AUTH_OTP_MAX_ATTEMPTS", "5"))
AUTH_PASSWORD_MAX_ATTEMPTS = int(os.getenv("AUTH_PASSWORD_MAX_ATTEMPTS", "5"))
AUTH_FIRST_TIME_PASSWORD = os.getenv("AUTH_FIRST_TIME_PASSWORD", "314159")
AUTH_DEBUG_OTP_PREVIEW = (
    os.getenv("AUTH_DEBUG_OTP_PREVIEW", "true" if DEBUG else "false").lower() == "true"
)
TRUSTED_SSO_CODE_TTL_SECONDS = int(os.getenv("TRUSTED_SSO_CODE_TTL_SECONDS", "120"))
TRUSTED_SSO_CLIENTS = {}
trusted_sso_karma_secret = os.getenv("TRUSTED_SSO_KARMA_CLIENT_SECRET", "").strip()
trusted_sso_karma_redirect_uris = env_list("TRUSTED_SSO_KARMA_REDIRECT_URIS", "")
if trusted_sso_karma_secret and trusted_sso_karma_redirect_uris:
    TRUSTED_SSO_CLIENTS["karma"] = {
        "client_secret": trusted_sso_karma_secret,
        "redirect_uris": trusted_sso_karma_redirect_uris,
        "name": "Acuité Karma",
    }
if SENTRY_ENABLED:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENVIRONMENT,
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        send_default_pii=True,
        integrations=[DjangoIntegration()],
    )


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "battleship",
    "directory",
    "feed",
    "learning",
    "recognition",
    "store",
    "operations",
    "voice",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "operations.middleware.RequestContextMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "accounts.middleware.SessionDeadlineMiddleware",
    "operations.middleware.ErrorMonitoringMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_ROOT],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASE_ENGINE = os.getenv("DATABASE_ENGINE", "sqlite").lower()

if not database_url and os.getenv("POSTGRES_DB"):
    database_url = (
        f"postgresql://{os.getenv('POSTGRES_USER', '')}:{os.getenv('POSTGRES_PASSWORD', '')}"
        f"@{os.getenv('POSTGRES_HOST', '127.0.0.1')}:{os.getenv('POSTGRES_PORT', '5432')}"
        f"/{os.getenv('POSTGRES_DB')}"
    )

if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
elif DATABASE_ENGINE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "acuite_connect"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "Asia/Kolkata")
BATTLESHIP_TIMEZONE = os.getenv("BATTLESHIP_TIMEZONE", TIME_ZONE)
BATTLESHIP_INVITE_TTL_MINUTES = int(os.getenv("BATTLESHIP_INVITE_TTL_MINUTES", "120"))
BATTLESHIP_INACTIVITY_TIMEOUT_MINUTES = int(
    os.getenv("BATTLESHIP_INACTIVITY_TIMEOUT_MINUTES", "30")
)
BATTLESHIP_POLL_INTERVAL_SECONDS = int(os.getenv("BATTLESHIP_POLL_INTERVAL_SECONDS", "4"))
BATTLESHIP_BLOCK_WINDOWS = []
for raw_window in env_list(
    "BATTLESHIP_BLOCK_WINDOWS",
    "10:00-13:00,14:00-18:30",
):
    if "-" not in raw_window:
        continue
    start, end = raw_window.split("-", 1)
    if start.strip() and end.strip():
        BATTLESHIP_BLOCK_WINDOWS.append((start.strip(), end.strip()))
if not BATTLESHIP_BLOCK_WINDOWS:
    BATTLESHIP_BLOCK_WINDOWS = [("10:00", "13:00"), ("14:00", "18:30")]

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "/login.html"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login.html"

FRONTEND_ASSET_ROOT = PROJECT_ROOT / "assets"
STATIC_URL = "/static/"
STATIC_ROOT = PROJECT_ROOT / "staticfiles"
STATICFILES_DIRS = [FRONTEND_ASSET_ROOT]
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "false").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "15"))
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "connect@acuite-group.com")
SERVER_EMAIL = os.getenv("SERVER_EMAIL", DEFAULT_FROM_EMAIL)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}

SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CSRF_COOKIE_HTTPONLY = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = os.getenv(
    "USE_X_FORWARDED_HOST",
    "true" if not DEBUG else "false",
).lower() == "true"
SECURE_SSL_REDIRECT = os.getenv(
    "SECURE_SSL_REDIRECT",
    "true" if not DEBUG else "false",
).lower() == "true"
SESSION_COOKIE_SECURE = os.getenv(
    "SESSION_COOKIE_SECURE",
    "true" if not DEBUG else "false",
).lower() == "true"
CSRF_COOKIE_SECURE = os.getenv(
    "CSRF_COOKIE_SECURE",
    "true" if not DEBUG else "false",
).lower() == "true"
SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
CSRF_COOKIE_SAMESITE = os.getenv("CSRF_COOKIE_SAMESITE", "Lax")
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0" if DEBUG else "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    "true" if not DEBUG else "false",
).lower() == "true"
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "false").lower() == "true"
SECURE_REFERRER_POLICY = os.getenv("SECURE_REFERRER_POLICY", "same-origin")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
