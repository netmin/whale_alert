import asyncio
import structlog

log = structlog.get_logger(__name__)


async def poll(settings) -> None:
    """Placeholder polling for Bitquery API."""
    log.info("bitquery_poll_start")
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        log.info("bitquery_poll_stop")
        raise
