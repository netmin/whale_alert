import asyncio
from datetime import datetime
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from app.core.models import Event

_BUFFER: list[Event] = []
_LOCK = asyncio.Lock()

DATA_DIR = Path("data/alerts")

async def flush_every(delay: int = 5) -> None:
    while True:
        await asyncio.sleep(delay)
        async with _LOCK:
            if not _BUFFER:
                continue
            to_write = _BUFFER.copy()
            _BUFFER.clear()

        table = pa.Table.from_pylist([e.__dict__ for e in to_write])
        path = _path_for_day(to_write[0].ts)
        path.parent.mkdir(parents=True, exist_ok=True)
        pq.write_to_dataset(table, root_path=str(path.parent), basename_template=path.name)

def _path_for_day(ts: datetime) -> Path:
    return DATA_DIR / f"{ts:%Y/%m/%d}" / "part.parquet"

async def enqueue(evt: Event) -> None:
    async with _LOCK:
        _BUFFER.append(evt)