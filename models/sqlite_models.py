from sqlalchemy import Column, ForeignKey, PickleType
from sqlalchemy import String, Integer, Float, Sequence, DateTime, Boolean
from database.sqlite_connection import Base
from sqlalchemy.orm import relationship
from sqlalchemy import JSON, TEXT, Column, DateTime, String, Date, Numeric, func, Integer, ARRAY
from sqlalchemy.orm import deferred, relationship
from models.mixins_model import Timestamp

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(TEXT, nullable=True)
    password = deferred(Column(TEXT, nullable=False))
    primary_email = Column(TEXT, unique=True, nullable=False)
    first_name = Column(TEXT, nullable=False)
    last_name = Column(TEXT, nullable=False)

class Audio(Timestamp, Base):
    __tablename__ = "audios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(TEXT, nullable=True)
    path = Column(TEXT, nullable=False)

    type = Column(Integer, nullable=False) # 1 -> uploaded audio (original), 2 -> text to speech audio, 3 -> modified audio

    user_id = Column(Integer, ForeignKey(
        "users.id"), nullable=False, unique=False)

    user = relationship("User")