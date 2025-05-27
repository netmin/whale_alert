import structlog
from app.core.filter import is_interesting
from app.core.storage import enqueue
from app.core.notifier import send_telegram
from app.core.models import Event

log = structlog.get_logger()

async def process_event(evt: Event) -> None:
    if not is_interesting(evt):
        return

    log.info(
        "whale_event",
        chain=evt.chain,
        usd=float(evt.amount_usd),
        native=float(evt.amount_native),
        tx=evt.tx_hash,
    )
    await enqueue(evt)
    await send_telegram(evt)