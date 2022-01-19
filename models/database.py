from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_NAME = 'experiment.sqlite'
path = 'sqlite:///' + os.path.join(basedir, DATABASE_NAME)

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)