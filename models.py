from datetime import datetime, date
from pydantic import BaseModel, Field

class Info(BaseModel):
    sender: str
    message: str
    sended: datetime = Field(default_factory=datetime.now)

