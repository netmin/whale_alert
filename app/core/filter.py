from app.config import settings
from app.core.models import Event

WATCH = {addr.lower() for addr in settings.watch_addresses}
IGNORE = {addr.lower() for addr in settings.ignore_addresses}

def is_interesting(evt: Event) -> bool:
    if evt.from_addr in IGNORE and evt.to_addr in IGNORE:
        return False

    if evt.from_addr in WATCH or evt.to_addr in WATCH:
        return True

    if evt.chain == "ETH":
        return evt.amount_usd >= settings.eth_threshold_usd
    if evt.chain == "BTC":
        return evt.amount_native >= settings.btc_threshold_btc
    return True