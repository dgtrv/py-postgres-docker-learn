from asyncio.log import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logger.common_log import log_model_init
from os import getenv

from .model import Base, Hero, Side, Story, Motto, Interaction

log = log_model_init

log.info('trying to create db engine')
engine = create_engine('postgresql://dgtrv:dgtrv@db:5432/heroes_db')
log.info('engine created')

log.info('trying to create session with engine')
Session = sessionmaker(bind=engine)
log.info('session created')
