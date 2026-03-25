# Acuite Connect

Acuité Connect is the employee network for Acuité Ratings & Research. This repository contains the front-end experience, Django backend, moderation controls, audit logging, analytics capture, and deployment blueprint for the production app.

## Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/acuiteratings/connect-acuite-group-com)

## Production target

- App URL: `connect.acuite-group.com`
- Runtime: Django + Gunicorn/Uvicorn
- Database: PostgreSQL
- Static assets: WhiteNoise

## Local commands

```bash
npm run backend:migrate
npm run backend:seed
npm run backend:dev
```

## Employee access workflow

- Accounts are provisioned manually by Acuité administrators.
- Login order is fixed: employee email -> email OTP -> password.
- First login and every 90-day password expiry force an inline password change before access completes.
- Bulk roster imports are supported with:

```bash
cd backend
../.venv/bin/python manage.py import_employee_accounts /path/to/employees.csv --temporary-password 'TempPass@123'
```

## Email OTP configuration

Set the SMTP-related environment variables in `.env` or Render before using live OTP delivery:

- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`

## Important note

For local development, OTP preview can be enabled with `AUTH_DEBUG_OTP_PREVIEW=true`. It is disabled by default in the Render blueprint.

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
../.venv/bin/python manage.py test battleship.tests
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
