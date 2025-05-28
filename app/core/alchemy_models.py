from pydantic import BaseModel
from typing import List, Union

class AlchemyActivity(BaseModel):
    rawValue: str
    timestamp: Union[str, int]
    fromAddress: str
    toAddress: str
    hash: str
    blockNumber: str

class AlchemyEvent(BaseModel):
    activity: List[AlchemyActivity]

class LogTransaction(BaseModel):
    hash: str

class LogEntry(BaseModel):
    index: int
    data: str
    topics: list[str]
    transaction: LogTransaction

class LogBlock(BaseModel):
    number: int
    timestamp: int
    logs: list[LogEntry]

class AlchemyLogsPayload(BaseModel):
    """Payload data for log webhooks."""

    block: LogBlock
