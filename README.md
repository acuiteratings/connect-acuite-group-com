# Acuite Connect

Acuité Connect is the employee network for Acuité Ratings & Research. This repository contains the front-end experience, Django backend, moderation controls, audit logging, analytics capture, and deployment blueprint for the production app.

## Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/acuiteratings/connect-acuite-group-com)

## Production target

- App URL: `connect.acuite-group.com`
- Runtime: Django + Gunicorn/Uvicorn
- Database: PostgreSQL
- Static assets: Render static site (`acuite-connect-static`)

## Local commands

```bash
npm run backend:migrate
npm run backend:seed
npm run backend:dev
```

## Employee access workflow

- Accounts are provisioned manually by Acuité administrators.
- Employee SSO is now the primary identity provider for Acuité Connect.
- Employee SSO answers "Who is this user?" and Acuité Connect answers "What can this user do in Connect?"
- Acuité Connect links SSO logins to local users by email and preserves Connect-specific local roles, posting rights, moderation rights, and admin rights.
- If a user is authenticated by Employee SSO but does not yet have local Connect authorization, the app shows a dedicated access-denied page.
- Existing local password and OTP code remains relevant only for legacy/manual auth flows and operational fallback, not as the primary production login path.
- Bulk roster imports are supported with:

```bash
cd backend
../.venv/bin/python manage.py import_employee_accounts /path/to/employees.csv --temporary-password 'TempPass@123'
```

## Employee SSO configuration

Set these environment variables in `.env` for local work and in Render for production:

- `EMPLOYEE_SSO_BASE_URL`
- `EMPLOYEE_SSO_CLIENT_ID`
- `EMPLOYEE_SSO_CLIENT_SECRET`
- `EMPLOYEE_SSO_AUTHORIZE_URL`
- `EMPLOYEE_SSO_TOKEN_URL`
- `EMPLOYEE_SSO_USERINFO_URL`
- `EMPLOYEE_SSO_CALLBACK_URL`
- `EMPLOYEE_SSO_POST_LOGOUT_REDIRECT_URL`

## People directory sync configuration

Connect uses the People app as the source of truth for employee master data and keeps a local synced snapshot for fast directory reads.

Set these environment variables in `.env` for local work and in Render for production:

- `PEOPLE_DIRECTORY_API_BASE_URL`
- `PEOPLE_DIRECTORY_API_TOKEN`
- `PEOPLE_DIRECTORY_API_TIMEOUT_SECONDS`

Manual sync commands:

```bash
cd backend
../.venv/bin/python manage.py sync_people_directory
../.venv/bin/python manage.py sync_people_directory --full
```

Directory API responses are paginated with a maximum `page_size` of 500 records. The frontend keeps using the local snapshot cache for quick repeat visits.

## Production checks and retention

- GitHub Actions runs a production smoke check after pushes to `main`.
- Render runs `prune_operational_events` weekly to trim old analytics, audit, error, and reported-error records.

Production callback URL:

- `https://connect.acuite-group.com/api/accounts/auth/employee-sso/callback/`

Local callback URL:

- `http://127.0.0.1:8240/api/accounts/auth/employee-sso/callback/`

## Email OTP configuration

Legacy/manual auth flow support still uses SMTP configuration:

Set the SMTP-related environment variables in `.env` or Render before using live OTP delivery:

- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`

## Important note

For local development, OTP preview can be enabled with `AUTH_DEBUG_OTP_PREVIEW=true` if the legacy/manual auth path is being tested. Employee SSO is the intended primary login path in production.

## Battleship module

Acuité Connect includes an intranet-safe 2-player Battleship module for off-peak employee engagement.

### Architecture

- Backend app: `backend/battleship`
- Frontend panel: `index.html` + `assets/js/battleship.js` + `assets/css/app.css`
- Real-time model: reliable polling against authoritative server state
- Persistence: every invitation, ship layout, shot, pause, resume and result is stored in the database

### Setup

Run the standard migration flow after pulling changes:

```bash
cd backend
../.venv/bin/python manage.py migrate
../.venv/bin/python manage.py test battleship
```

Optional server-side settings:

- `BATTLESHIP_TIMEZONE`
- `BATTLESHIP_BLOCK_WINDOWS`
- `BATTLESHIP_INVITE_TTL_MINUTES`
- `BATTLESHIP_INACTIVITY_TIMEOUT_MINUTES`
- `BATTLESHIP_POLL_INTERVAL_SECONDS`

Example:

```bash
BATTLESHIP_TIMEZONE=Asia/Kolkata
BATTLESHIP_BLOCK_WINDOWS=10:00-13:00,14:00-18:30
```

### Office-hour restrictions

- Battleship is blocked during:
  - `10:00 AM - 1:00 PM`
  - `2:00 PM - 6:30 PM`
- Time is evaluated on the server using the configured office timezone.
- During blocked windows:
  - new invites cannot be sent
  - invites cannot be accepted
  - ships cannot be placed
  - no turns can be fired

### One-active-match rule

- Multiple pending invitations are allowed.
- Only one accepted Battleship match may occupy the live intranet slot at a time.
- The slot is claimed when a match moves into `ship_placement`.
- The slot remains occupied through:
  - `ship_placement`
  - `active`
  - `paused_office_hours`
- The slot is released when the match becomes:
  - `completed`
  - `resigned`
  - `abandoned`

This rule is enforced in the business layer and at the database level with a partial unique constraint on the `occupies_global_slot` flag.

### Pause and resume behavior

- If a live match is running when a blocked office window begins, the server moves it to `paused_office_hours`.
- While paused, no placement or firing actions are accepted.
- The next state sync after office hours resume moves the match back to its previous live phase.
- Inactivity timing is reset around pause/resume so a legitimate match is not abandoned just because office hours intervened.

### Integrity and concurrency

- The server owns turn order, shot resolution, win detection and sunk-ship reveal state.
- Duplicate turns and duplicate target cells are rejected server-side.
- Match transitions, acceptance, firing, resignation and global-slot claiming run inside transactions.
- Only players in a match can access or act on that match.
