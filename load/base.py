from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Viene instlado en python
engine = create_engine('sqlite:///newspaper.db')

Session = sessionmaker(bind=engine)

Base = declarative_base()