from asyncio.log import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logger.common_log import log_model_init
from os import getenv

from .model import Base, Hero, Side, Story, Motto, Interaction

log = log_model_init

log.info('trying to create db engine')

db_user = getenv('POSTGRES_USER')
db_password = getenv('POSTGRES_PASSWORD')
db_name = getenv('POSTGRES_DB')
sql_host = getenv('SQL_HOST')
sql_port = getenv('SQL_PORT')

engine = create_engine(f'postgresql://{db_user}:{db_password}@{sql_host}:{sql_port}/{db_name}')

log.info('engine created')

log.info('trying to create session with engine')
Session = sessionmaker(bind=engine)
log.info('session created')
