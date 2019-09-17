from model.base import Base
from sqlalchemy import Column, Integer, String


class Pilihan(Base):
    __tablename__ = 'pilihan'

    key = Column(String(5), primary_key=True)
    pilihan = Column(Integer)
