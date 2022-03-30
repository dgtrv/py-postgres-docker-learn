from os import getenv, path, makedirs

LOG_LEVEL = getenv('LOG_LEVEL', default='DEBUG')
LOG_FILE = getenv('LOG_FILE', default='/usr/src/app/logs/log.txt')
LOGS_DIR = path.dirname(LOG_FILE)

makedirs(LOGS_DIR, exist_ok=True)


