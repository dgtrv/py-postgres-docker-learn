import logging
from logger import LOG_LEVEL, LOG_FILE

logging.basicConfig(
    format='%(asctime)s: %(name)-12s: %(levelname)-8s: %(message)s',
    datefmt='%Y.%m.%d %H:%M:%S',
    filename=LOG_FILE,
    filemode='a',
    level=logging.getLevelName(LOG_LEVEL)
)

logging.info('Log session started')

log_manage_py = logging.getLogger('manage.py')
log_model_init = logging.getLogger('model/__init__.py')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

