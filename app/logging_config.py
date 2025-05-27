import logging
import os
from typing import Any

import structlog
from rich.console import Console
from structlog.processors import (
    JSONRenderer,
    StackInfoRenderer,
    TimeStamper,
)

from app.config import settings

rich_console = Console()

def _rich_processor(logger, method, event_dict: dict[str, Any]) -> str:
    rich_console.print(
        f"[bold cyan]{event_dict.pop('level', method).upper():8s}[/]"
        f"[dim]{event_dict.pop('timestamp')}[/] "
        f"{event_dict.pop('event', '')}",
        *[
            f"[cyan]{k}[/]=[magenta]{v}[/]"
            for k, v in event_dict.items()
        ],
    )
    return ""

_common = [
    StackInfoRenderer(),
    TimeStamper(fmt="iso", utc=True),
]

if settings.log_json:
    _processors = _common + [JSONRenderer()]
else:
    _processors = _common + [_rich_processor]

def configure_logging() -> None:
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        handlers=[logging.StreamHandler()],
    )

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        processors=_processors,
        cache_logger_on_first_use=True,
    )