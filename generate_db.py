from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

from model import base
from model import pemilih
from model import keys
from model import calon
from model import vote

engine = create_engine('mysql://aditya:rahasia123@localhost/evote')
print(base.Base.metadata.create_all(engine, checkfirst=True))
