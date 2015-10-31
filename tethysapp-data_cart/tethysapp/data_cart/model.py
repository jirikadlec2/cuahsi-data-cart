from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from .app import CuahsiDataCartDemo as app

# DB Engine, sessionmaker and base
engine = app.get_persistent_store_engine('datacart_db')
SessionMaker = sessionmaker(bind=engine)
Base = declarative_base()

class DataCart(Base):
    '''
    Example SQLAlchemy DB Model
    '''
    __tablename__ = 'datacart'

    # Columns
    id = Column(Integer, primary_key=True)
    res_id = Column(String)
    bytes = Column(Integer)
    url = Column(String)

    def __init__(self, res_id, bytes, url):
        self.res_id = res_id
        self.bytes = bytes
        self.url = url
