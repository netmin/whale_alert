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
