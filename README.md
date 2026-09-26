# submit-app

Password-protected text submission form for Agent 86.

- **Domain:** submit.agent86.cloud
- **Password:** Set via `FORM_PASSWORD` env var (default: `Coffee123!`)
- **Discord delivery:** Configure webhooks via env vars

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FORM_PASSWORD` | No | `Coffee123!` | Password to access the form |
| `N8N_WEBHOOK_URL` | No | — | n8n webhook to forward submissions |
| `DISCORD_WEBHOOK_URL` | No | — | Discord webhook for direct delivery |
| `SECRET_KEY` | No | Auto-generated | Flask session encryption key |
| `PORT` | No | `5000` | Internal port |