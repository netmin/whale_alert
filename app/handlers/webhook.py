from decimal import Decimal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core import parser, processor

router = APIRouter()


class AlchemyWebhookPayload(BaseModel):
    event: dict
    price_usd: Decimal | None = None


@router.post("/alchemy")
async def alchemy_webhook(payload: AlchemyWebhookPayload):
    try:
        evt = parser.from_alchemy(payload.model_dump(), payload.price_usd)
    except Exception as exc:  # pragma: no cover - simple validation
        raise HTTPException(status_code=400, detail="invalid payload") from exc

    await processor.process_event(evt)
    return {"status": "ok"}
