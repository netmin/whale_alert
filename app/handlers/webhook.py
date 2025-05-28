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
    log.info("webhook_payload_received", payload=payload)

    if "event" in payload:
        event_payload = payload["event"]
        # GraphQL log webhooks send log data as ``event.data``
        if isinstance(event_payload, dict) and "data" in event_payload:
            try:
                model = AlchemyLogsWebhookPayload(
                    data=event_payload["data"],
                    price_usd=payload.get("price_usd"),
                )
            except Exception as exc:  # pragma: no cover - validation
                log.debug("parse_logs_failed", err=str(exc))
                raise HTTPException(
                    status_code=400, detail="invalid log payload"
                ) from exc

            log.info("parsed_log_payload")
            evt = parser.from_alchemy_logs(model.data, model.price_usd)
        else:
            try:
                model = AlchemyWebhookPayload(**payload)
            except Exception as exc:  # pragma: no cover - validation
                log.debug("parse_event_failed", err=str(exc))
                raise HTTPException(
                    status_code=400, detail="invalid event payload"
                ) from exc

            log.info("parsed_event_payload")
            evt = parser.from_alchemy(model.event, model.price_usd)

    elif "data" in payload:
        try:
            model = AlchemyLogsWebhookPayload(**payload)
        except Exception as exc:  # pragma: no cover - validation
            log.debug("parse_logs_failed", err=str(exc))
            raise HTTPException(status_code=400, detail="invalid log payload") from exc

        log.info("parsed_log_payload")
        evt = parser.from_alchemy_logs(model.data, model.price_usd)

    else:
        log.warning("invalid_payload", err="missing event or data")
        raise HTTPException(status_code=400, detail="invalid payload")

    await processor.process_event(evt)
    log.info("event_processed")
    return {"status": "ok"}
