from model.base import Base
from sqlalchemy import Column, Integer, String


class Pemilih(Base):
    __tablename__ = 'pemilih'

    id = Column(Integer, primary_key=True)
    nama = Column(String(256))
    alamat = Column(String(512))
    no_hp = Column(String(16))
    no_ktp = Column(String(64))
    key = Column(String(5))
    status_memilih = Column(String(32))  # tidak aktif, aktif, sudah memilih
