from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column, String, Integer, DateTime, LargeBinary,
)

db = SQLAlchemy()
Base = db.Model


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    format = Column(String(180))
    content = Column(String(180))
    card_front = Column(String(180))
    card_back = Column(String(180))
    date_create = Column(DateTime, default=datetime.now())
