from decimal import Decimal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core import parser, processor
from app.core.alchemy_models import AlchemyEvent, AlchemyLogsPayload

router = APIRouter()


class AlchemyWebhookPayload(BaseModel):
    event: AlchemyEvent
    price_usd: Decimal | None = None


class AlchemyLogsWebhookPayload(BaseModel):
    data: AlchemyLogsPayload
    price_usd: Decimal | None = None


@router.post("/alchemy")
async def alchemy_webhook(
    payload: AlchemyWebhookPayload | AlchemyLogsWebhookPayload,
):
    try:
        if isinstance(payload, AlchemyWebhookPayload):
            evt = parser.from_alchemy(payload.event, payload.price_usd)
        else:
            evt = parser.from_alchemy_logs(payload.data, payload.price_usd)
    except Exception as exc:  # pragma: no cover - simple validation
        raise HTTPException(status_code=400, detail="invalid payload") from exc

    await processor.process_event(evt)
    return {"status": "ok"}
