from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .model import Base, Hero, Side, Story, Motto, Interaction

engine = create_engine('postgresql://dgtrv:dgtrv@db:5432/heroes_db')
Session = sessionmaker(bind=engine)
