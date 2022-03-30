from os import getenv, path, makedirs
import logging

LOG_LEVEL = getenv('LOG_LEVEL', default='DEBUG')
LOG_FILE = getenv('LOG_FILE', default='/usr/src/app/logs/log.txt')
LOGS_DIR = path.dirname(LOG_FILE)

makedirs(path.dirname(LOG_FILE), exist_ok=True)

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
log_for_interactions = logging.getLogger('interactions')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


interactions_log_file = path.join(LOGS_DIR, 'interactions_log.txt')
interactions_log_file_handler = logging.FileHandler(
    filename=interactions_log_file,
    mode='a'
)
log_for_interactions.addHandler(interactions_log_file_handler)

