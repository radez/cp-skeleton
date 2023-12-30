from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, Integer, String, Text

from model import Base, MetaBase


# Notification Can be shortened to n10n
class Notification(Base, MetaBase):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    type = Column(String(32), nullable=False)
    meta = Column(Text, nullable=False)
    stamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed = Column(DateTime(timezone=True))

    def __repr__(self):
        return 'Notification(id={}, type={}, meta={})'.format(self.id, self.type, self.meta)
