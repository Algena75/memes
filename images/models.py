from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from images.core.db import Base


class Mem(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(254), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), default=datetime.now)

    def __str__(self):
        return self.name[:30]

    def dict(self):
        return dict(name=self.name,
                    id=self.id,
                    description=self.description,
                    uploaded_at=self.uploaded_at)
