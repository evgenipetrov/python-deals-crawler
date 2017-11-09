from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
import datetime

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection.
    Returns sqlalchemy engine instance
    """
    return create_engine('mysql://realgear:LXtWcTAwDw@localhost:3306/realgear')


def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Deals(DeclarativeBase):
    """Sqlalchemy model"""
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True)
    title = Column('title', String(200))
    url = Column('url', String(300), nullable=True)
    image = Column('image', String(200))
    listed_price = Column('listed_price', String(200))
    current_price = Column('current_price', String(200))
    store = Column('store', String(200))
    date = Column('date', DateTime, default=datetime.datetime.utcnow, nullable=True)
