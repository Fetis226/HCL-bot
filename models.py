from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy_serializer import SerializerMixin
class Base(DeclarativeBase, SerializerMixin): pass
class event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key= True, index= True, autoincrement= True)
    name = Column(String(45), default="-")
    description = Column(String(45), default="-")
    region = Column(String(45), default="-")
    languages = Column(String(45), default="-")
    fighters = Column(String(255), default="-")
    status = Column(Boolean, default=0)
    start = Column(DateTime)
    end = Column(DateTime)
    yt_link = Column(String(100), default="-")
    twitch_link = Column(String(100), default="-")
class member(Base):
    __tablename__ = "member"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(16), default="-")
    region = Column(String(45), default="-")
    ping = Column(String(45), default="-")
    affiliation = Column(String(45), default="-")
    language = Column(String(45), default="-")
    discord_username = Column(String(100), unique=True)
    discord_id = Column(String(100), unique=True)
    wins = Column(Integer, default= 0)
    loses = Column(Integer, default= 0)
    fighter_pic = Column(String(300), default = "-")
    reg = Column(Boolean, default = 0)