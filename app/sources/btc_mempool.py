import asyncio
import structlog

log = structlog.get_logger(__name__)


async def listen(settings) -> None:
    """Placeholder listener for BTC mempool."""
    log.info("btc_mempool_listen_start")
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        log.info("btc_mempool_listen_stop")
        raise
