from sqlalchemy import (
    Column,
    Integer,
    Text,
    TIMESTAMP,
)
import sqlalchemy.sql.functions as func

from .meta import Base


class Reminder(Base):
    __tablename__ = 'reminder'
    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    created = Column(TIMESTAMP, server_default=func.now(), nullable=False)