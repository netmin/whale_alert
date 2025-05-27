
# Whale Alert

Example FastAPI application.

## Running locally

1. Copy `.env.example` to `.env` and fill in any values you need.
2. Start the app:

```bash
uvicorn app.main:app --reload
```

## Running with Docker

Build and start the application using Docker Compose:

```bash
docker compose up --build
```

## Alchemy Webhook

POST `/webhook/alchemy` accepts JSON with the event payload from Alchemy. The
`price_usd` field is optional and is used to calculate the USD value of the
transfer:

```json
{
  "event": {"activity": [...]},
  "price_usd": 3500
}
```
