# Acuite Connect Deployment

Acuité Connect now includes a Django backend and PostgreSQL-ready data layer, so the production deployment target should be a Python host with a managed database. This repo includes a Render Blueprint for that setup.

## Recommended production target

- App host: Render web service
- Database: Render PostgreSQL
- Domain: `connect.acuite-group.com`
- Static assets: WhiteNoise from Django
- Error monitoring: optional Sentry via `SENTRY_DSN`

## Deployment files

- [render.yaml](/Users/sankarchakraborti/Documents/New%20project%203/acuite-connect/render.yaml)
- [build.sh](/Users/sankarchakraborti/Documents/New%20project%203/acuite-connect/build.sh)
- [backend/config/settings.py](/Users/sankarchakraborti/Documents/New%20project%203/acuite-connect/backend/config/settings.py)
- [backend/requirements.txt](/Users/sankarchakraborti/Documents/New%20project%203/acuite-connect/backend/requirements.txt)

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
cd /Users/sankarchakraborti/Documents/New\ project\ 3/acuite-connect/backend
../.venv/bin/python manage.py runserver 127.0.0.1:8241 --noreload
```

## Important note

The existing Cloudflare Pages deployment can still serve the older static MVP, but it cannot host the Django backend, database, moderation APIs, or real authentication. To make `connect.acuite-group.com` the real source of truth, the domain should move from Pages to the Render web service after that service is live.
