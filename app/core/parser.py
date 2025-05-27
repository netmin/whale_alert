from decimal import Decimal
from datetime import datetime, timezone
from app.core.models import Event
from app.core.alchemy_models import AlchemyEvent, AlchemyLogsPayload

def _strip_hex(value: str) -> str:
    return value.lower().removeprefix("0x")

def from_alchemy(event: AlchemyEvent, price_usd: Decimal | None) -> Event:
    tx = event.activity[0]
    wei = int(tx.rawValue)
    amount_eth = Decimal(wei) / Decimal(10 ** 18)

    return Event(
        ts=datetime.fromtimestamp(int(tx.timestamp), tz=timezone.utc),
        chain="ETH",
        from_addr=_strip_hex(tx.fromAddress),
        to_addr=_strip_hex(tx.toAddress),
        amount_native=amount_eth,
        amount_usd=amount_eth * price_usd if price_usd is not None else Decimal(0),
        tx_hash=_strip_hex(tx.hash),
        meta={"block": tx.blockNumber},
    )


def from_alchemy_logs(payload: AlchemyLogsPayload, price_usd: Decimal | None) -> Event:
    block = payload.data.block
    log = block.logs[0]

    wei = int(log.data, 16)
    amount_eth = Decimal(wei) / Decimal(10 ** 18)

    return Event(
        ts=datetime.fromtimestamp(int(block.timestamp), tz=timezone.utc),
        chain="ETH",
        from_addr=_strip_hex(log.topics[1][-40:]),
        to_addr=_strip_hex(log.topics[2][-40:]),
        amount_native=amount_eth,
        amount_usd=amount_eth * price_usd if price_usd is not None else Decimal(0),
        tx_hash=_strip_hex(log.transaction.hash),
        meta={"block": str(block.number)},
    )
