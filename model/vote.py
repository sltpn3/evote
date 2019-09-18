from model.base import Base
from sqlalchemy import Column, Integer, String


class Vote(Base):
    __tablename__ = 'vote'

    key = Column(String(5), primary_key=True)
    pilihan = Column(Integer)
