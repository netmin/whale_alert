import httpx

from app.config import settings
from app.core.models import Event

_API = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"

async def send_telegram(evt: Event) -> None:
    usd = f"${evt.amount_usd:,.0f}"
    native = f"{evt.amount_native.normalize():f}"
    msg = (
        f"🐳 [{evt.chain}] {usd} ({native})\n"
        f"{evt.from_addr[:6]}… → {evt.to_addr[:6]}…\n"
        f"https://debank.com/tx/{evt.chain.lower()}/{evt.tx_hash}"
    )
    async with httpx.AsyncClient() as client:
        await client.post(_API, json={"chat_id": settings.telegram_chat_id, "text": msg})
