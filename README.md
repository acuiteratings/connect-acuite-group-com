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

## Important note

The current public `connect.acuite-group.com` site may still point to the older static Cloudflare Pages deployment until the Render service is created and the DNS target is updated.
