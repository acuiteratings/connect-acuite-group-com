# Acuite Connect Backend

This Django service adds the first real backend for Acuite Connect while preserving the existing static UI files at the project root.

## Local setup

1. Create and activate the virtual environment from the project root.
2. Install dependencies from `backend/requirements.txt`.
3. Copy `.env.example` to `.env` and adjust values if needed.
4. Run `../.venv/bin/python manage.py migrate` from the `backend` directory.
5. Create an admin user with `../.venv/bin/python manage.py createsuperuser`.
6. Start the server with `../.venv/bin/python manage.py runserver`.

## Included modules

- `accounts`: custom user model and employee identity data
- `directory`: employee profile and directory records
- `feed`: posts and comments with moderation states
- `operations`: audit logs and health checks

## API surface

All `/api/` endpoints require an authenticated active employee session except `/api/accounts/me/`, `/api/accounts/auth/*`, and `/api/ops/health/`.

- `GET /api/accounts/me/`
- `GET|POST /api/feed/posts/`
- `GET|POST /api/feed/posts/<post_id>/comments/`
- `GET /api/directory/`
- `GET /api/ops/health/`
- `GET /api/ops/summary/`
- `GET /api/ops/moderation/queue/`
- `POST /api/ops/moderation/posts/<post_id>/decision/`
- `POST /api/ops/moderation/comments/<comment_id>/decision/`
- `GET /api/ops/audit/`
- `GET /api/ops/analytics/`
- `POST /api/ops/analytics/ingest/`
- `GET /api/ops/errors/`

## Monitoring and controls

- Request tracing via `X-Request-ID`
- Audit logging for feed creation and moderation actions
- Analytics ingestion endpoint for product events
- Database-backed error capture with optional Sentry forwarding when `SENTRY_DSN` is configured
