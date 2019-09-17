from model.base import Base
from sqlalchemy import Column, Integer, String


class Calon(Base):
    __tablename__ = 'calon'

    id = Column(Integer, primary_key=True)
    nama = Column(String(512))
