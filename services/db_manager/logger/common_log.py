import logging
from logging.handlers import RotatingFileHandler
from logger import LOG_LEVEL, LOG_FILE


logging.basicConfig(
    format='%(asctime)s: %(name)-12s: %(levelname)-8s: %(message)s',
    datefmt='%Y.%m.%d %H:%M:%S',
    level=logging.INFO
)

logging.info('Log session started')

log_manage_py = logging.getLogger('manage.py')
log_model_init = logging.getLogger('model/__init__.py')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

file_handler_with_rotation = RotatingFileHandler(
    filename=LOG_FILE,
    mode='a',
    maxBytes=5e6,
    backupCount=10
)
file_handler_with_rotation.setLevel(logging.getLevelName(LOG_LEVEL))
logging.getLogger('').addHandler(file_handler_with_rotation)
