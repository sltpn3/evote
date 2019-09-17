from model.base import Base
from sqlalchemy import Column, Integer, String


class Keys(Base):
    __tablename__ = 'keys'

    key = Column(String(5), primary_key=True)
    status = Column(String(32))  # tidak aktif, aktif, terpakai
