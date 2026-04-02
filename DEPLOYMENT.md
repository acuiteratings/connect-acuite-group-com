# Acuite Connect Deployment

Acuité Connect now includes a Django backend and PostgreSQL-ready data layer, so the production deployment target should be a Python host with a managed database. This repo includes a Render Blueprint for that setup.

## Recommended production target

- App host: Render web service
- Database: Render PostgreSQL
- Domain: `connect.acuite-group.com`
- Static assets: WhiteNoise from Django
- Error monitoring: optional Sentry via `SENTRY_DSN`

## Deployment files

- `render.yaml`
- `build.sh`
- `backend/config/settings.py`
- `backend/requirements.txt`

## Render deploy flow

1. Push Acuité Connect to its own Git repository.
2. In Render, create a new Blueprint from that repository.
3. Let Render provision:
   - `acuite-connect` web service
   - `acuite-connect-db` PostgreSQL database
4. Add `connect.acuite-group.com` as the custom domain in Render.
5. Point Cloudflare DNS for `connect.acuite-group.com` to the Render hostname.

## Commands Render runs

```bash
./build.sh
cd backend && python manage.py migrate
cd backend && python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
```

## Local backend preview

```bash
cd /Users/headit/Documents/GitHub/connect-acuite-group-com/backend
../.venv/bin/python manage.py runserver 127.0.0.1:8241 --noreload
```

## Employee SSO production settings

Render must define these environment variables for live Employee SSO login:

- `EMPLOYEE_SSO_BASE_URL=https://sso.acuite-group.com`
- `EMPLOYEE_SSO_CLIENT_ID=acuite-connect`
- `EMPLOYEE_SSO_CLIENT_SECRET=...`
- `EMPLOYEE_SSO_AUTHORIZE_URL=https://sso.acuite-group.com/oauth/authorize`
- `EMPLOYEE_SSO_TOKEN_URL=https://sso.acuite-group.com/oauth/token`
- `EMPLOYEE_SSO_USERINFO_URL=https://sso.acuite-group.com/oauth/userinfo`
- `EMPLOYEE_SSO_CALLBACK_URL=https://connect.acuite-group.com/api/accounts/auth/employee-sso/callback/`
- `EMPLOYEE_SSO_POST_LOGOUT_REDIRECT_URL=https://connect.acuite-group.com/login.html`

## Authorization model

- Employee SSO is the central identity provider.
- Acuité Connect remains the source of truth for Connect-specific authorization.
- Existing Connect users should be linked by email so their local role and posting access continue after SSO login.
- The one-time local backfill command for existing users is:

```bash
./.venv/bin/python backend/manage.py backfill_employee_sso_access --all-users
```

## Important note

The existing Cloudflare Pages deployment can still serve the older static MVP, but it cannot host the Django backend, database, moderation APIs, or real authentication. To make `connect.acuite-group.com` the real source of truth, the domain should move from Pages to the Render web service after that service is live.
