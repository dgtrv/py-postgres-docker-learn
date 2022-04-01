import logging
from os import path
from logger import LOGS_DIR
from logger.telegram import telegram_handler, TELEGRAM_BOT_TOKEN


log_for_interactions = logging.getLogger('interactions')

interactions_log_file = path.join(LOGS_DIR, 'interactions_log.txt')
interactions_log_file_handler = logging.FileHandler(
    filename=interactions_log_file,
    mode='a'
)
interactions_log_formatter = logging.Formatter('%(asctime)s: %(name)-12s: %(levelname)-8s: %(message)s')
interactions_log_file_handler.formatter = interactions_log_formatter
interactions_log_file_handler.setLevel(logging.INFO)
log_for_interactions.addHandler(interactions_log_file_handler)

if TELEGRAM_BOT_TOKEN != '':
    log_for_interactions.addHandler(telegram_handler)

