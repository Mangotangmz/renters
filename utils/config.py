import redis

from utils.functions import get_db_uri
from utils.settings import DATABASE


class Config():

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'secret_key'

    SESSION_TYPE = 'redis'

    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379')