from logging import LogRecord
from logging.handlers import HTTPHandler
from os import getenv
import logging


TELEGRAM_HOST = 'api.telegram.org'
TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_SEND_URL = '/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage'
TELEGRAM_CHAT_ID = getenv('TELEGRAM_CHAT_ID', default='')


class TelegramLoggingHandler(HTTPHandler):
    def mapLogRecord(self, log_record: LogRecord) -> dict:
        result_dict = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': log_record.msg % log_record.args,
            'parse_mode': '',
            'disable_web_page_preview': True,
            'disable_notification': False,
            'reply_to_message_id': '',
            'reply_markup': ''
        }
        return result_dict

telegram_handler = TelegramLoggingHandler(
    host=TELEGRAM_HOST,
    url=TELEGRAM_SEND_URL,
    secure=True,
    method='POST'
)

telegram_handler.setLevel(logging.INFO)

