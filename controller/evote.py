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
        self.session = None
#         self.session = sessionmaker(bind=self.engine)

    def inititate_connection(self):
        self.session = self.Session()

    def pilihan_choices(self):
        self.inititate_connection()
        choices = [(e.id, e.nama) for e in self.session.query(calon.Calon).order_by('id')]
        self.session.close()
        return choices

    def search_voters_by_name(self, _filter):
        _filter = '%{}%'.format(_filter)
        self.inititate_connection()
        voters = self.session.query(pemilih.Pemilih).filter(pemilih.Pemilih.nama.like(_filter)).order_by('id').all()
#         voters = [e for e in self.session.query(pemilih.Pemilih).filter(pemilih.Pemilih.nama.like(_filter)).order_by('id')]
        self.session.close()
        return voters

    def get_voter(self, _id):
        self.inititate_connection()
        voter = self.session.query(pemilih.Pemilih).filter_by(id=_id).first()
        self.session.close()
        return voter
