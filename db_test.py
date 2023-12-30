# add your model classes here and run
# python -i db_test.py
# this will open python with the SQLAlchemy
# loaded into the `session` variable
from model.user import User # noqa F401

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import parse_config

cfg = parse_config('PROJECTNAME.conf')

engine = create_engine(cfg['db']['url'], echo=True)
session = sessionmaker(bind=engine)()
