import os
import configparser
from itertools import chain

API_NAME = 'Timesheet Rest API'

SECRET_KEY = 'xs4G5ZD9SwNME6nWRWrK_aq6Yb9H8VJpdwCzkTErFPw='

UUID_LENGTH = 10

UUID_ALPHABET = ''.join(map(chr, list(range(48, 58))))

TOKEN_EXPIRATION_TIME = 60 * 60 * 24 * 7

APP_ENV = os.environ.get('APP_ENV') or "local"

INI_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../conf/{}.ini'.format(APP_ENV)
)

CONFIG = configparser.ConfigParser()

CONFIG.read(INI_FILE_PATH)

POSTGRES = CONFIG['postgres']
if APP_ENV == 'dev' or APP_ENV == 'prod':
    DB_CONFIG = (
        POSTGRES['user'],
        POSTGRES['password'],
        POSTGRES['host'],
        POSTGRES['database']
    )
    DATABASE_URL = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_CONFIG)
else:
    DATABASE_URL = 'sqlite:///app.db'

DB_ECHO = True if CONFIG["database"]["echo"] == "yes" else False
DB_AUTOCOMMIT = True

LOG_LEVEL = CONFIG["logging"]["level"]
