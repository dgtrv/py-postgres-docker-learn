from os import getenv, path, makedirs

app_path = getenv('DB_MANAGER_APP_PATH', default='/usr/src/app/')
logs_dir_name = getenv('DB_MANAGER_APP_LOGS_DIR', default='logs')
logs_file_name = getenv('DB_MANAGER_LOGS_FILE', default='logs.txt')

LOGS_DIR = path.join(app_path, logs_dir_name)
LOG_FILE = path.join(LOGS_DIR, logs_file_name)
LOG_LEVEL = getenv('LOG_LEVEL', default='DEBUG')

makedirs(LOGS_DIR, exist_ok=True)


