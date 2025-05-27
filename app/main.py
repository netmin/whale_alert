# app/main.py
import asyncio
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from app.config import settings
from app.handlers import webhook
from app.logging_config import configure_logging
from app.sources import btc_mempool, infura, bitquery

configure_logging()
log = structlog.get_logger()

background_tasks: list[asyncio.Task] = []


@asynccontextmanager
async def lifespan(_: FastAPI):
    # startup
    if settings.sources.eth_infura:
        background_tasks.append(asyncio.create_task(infura.listen(settings)))
    if settings.sources.btc_ws:
        background_tasks.append(asyncio.create_task(btc_mempool.listen(settings)))
    if settings.sources.bitquery:
        background_tasks.append(asyncio.create_task(bitquery.poll(settings)))

    log.info("service_started")
    try:
        yield
    finally:
        # shutdown
        for task in background_tasks:
            task.cancel()
        await asyncio.gather(*background_tasks, return_exceptions=True)
        log.info("service_stopped")


app = FastAPI(title="Whale-Alert", lifespan=lifespan)
app.include_router(webhook.router, prefix="/webhook")
