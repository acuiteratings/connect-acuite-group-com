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
