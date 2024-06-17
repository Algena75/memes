from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, FileUrl


class MemBase(BaseModel):
    description: Optional[str] = None


class MemCreate(MemBase):
    pass


class MemDB(MemCreate):
    id: int
    name: str | FileUrl = Field(None, min_length=1, max_length=254)
    uploaded_at: datetime

    class Config:
        from_attributes = True
