from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class Event:
    ts: datetime
    chain: str
    from_addr: str
    to_addr: str
    amount_native: Decimal
    amount_usd: Decimal
    tx_hash: str
    meta: Mapping[str, Any] = field(default_factory=dict)
