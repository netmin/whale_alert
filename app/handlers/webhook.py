from decimal import Decimal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
import structlog

from app.core import parser, processor
from app.core.alchemy_models import AlchemyEvent, AlchemyLogsPayload

log = structlog.get_logger(__name__)
router = APIRouter()


class AlchemyWebhookPayload(BaseModel):
    model_config = ConfigDict(union_mode="smart")
    event: AlchemyEvent
    price_usd: Decimal | None = None


class AlchemyLogsWebhookPayload(BaseModel):
    model_config = ConfigDict(union_mode="smart")
    data: AlchemyLogsPayload
    price_usd: Decimal | None = None


@router.post("/alchemy")
async def alchemy_webhook(payload: dict):
<<<<<<< HEAD
    log.debug("webhook_payload_received", payload=payload)
    try:
        model = AlchemyWebhookPayload(**payload)
        log.debug("parsed_event_payload")
=======
    try:
        model = AlchemyWebhookPayload(**payload)
>>>>>>> f0ee4aa (Restore manual parsing for Alchemy webhooks)
        evt = parser.from_alchemy(model.event, model.price_usd)
    except Exception as exc:
        log.debug("parse_event_failed", err=str(exc))
        try:
            model = AlchemyLogsWebhookPayload(**payload)
<<<<<<< HEAD
            log.debug("parsed_log_payload")
=======
>>>>>>> f0ee4aa (Restore manual parsing for Alchemy webhooks)
            evt = parser.from_alchemy_logs(model.data, model.price_usd)
        except Exception as exc2:  # pragma: no cover - simple validation
            log.warning("invalid_payload", err=str(exc2))
            raise HTTPException(status_code=400, detail="invalid payload") from exc2

    await processor.process_event(evt)
    log.debug("event_processed")
    return {"status": "ok"}
