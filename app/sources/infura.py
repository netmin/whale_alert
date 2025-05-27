import asyncio
import structlog

log = structlog.get_logger(__name__)


async def listen(settings) -> None:
    """Placeholder listener for Infura websocket."""
    log.info("infura_listen_start")
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:  # graceful shutdown
        log.info("infura_listen_stop")
        raise
