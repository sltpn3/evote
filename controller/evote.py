from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import pemilih, calon
from flask.globals import session


class EvoteController():

    def __init__(self, config_file='config.conf'):
        self.config_file = config_file
        self.config = ConfigParser()
        self.config.read(self.config_file)
        self.engine_config = 'mysql://{}:{}@{}/{}?charset=utf8mb4'.format(self.config.get('database', 'user'),
                                                                          self.config.get('database', 'pass'),
                                                                          self.config.get('database', 'host'),
                                                                          self.config.get('database', 'name'))
        self.engine = create_engine(self.engine_config, pool_recycle=1)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
#         self.session = sessionmaker(bind=self.engine)

    def pilihan_choices(self):
        choices = [(e.id, e.nama) for e in self.session.query(calon.Calon).order_by('id')]
        return choices
