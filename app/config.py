import datetime

class Config(object):
    SECRET_KEY = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
    SQLALCHEMY_DATABASE_URI = "sqlite:///base.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

QUESTIONS_AMOUNT = 30
MAX_SCORE = 90
GAME_START_TIME = datetime.datetime(2023, 9, 1, 9, 30, 00)
ADMIN_CODE = "hamapa23"