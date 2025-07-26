from datetime import datetime

from pydantic import BaseModel


class PingResponse(BaseModel):
    message: str
    status: str
    timestamp: datetime
