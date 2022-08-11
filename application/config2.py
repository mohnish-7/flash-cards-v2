# Setting the configuration
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

	DEBUG = False
	SQLITE_DB_DIR = None
	SQLALCHEMY_DATABASE_URI = None
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	CELERY_BROKER_URL = "redis://localhost:6379/1"
	CELERY_RESULT_BACKEND = "redis://localhost:6379/2"

class DevelopmentConfig(Config):

	DEBUG = True
	SQLITE_DB_DIR = os.path.join(basedir,'../db_directory')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(SQLITE_DB_DIR,'flashcards.sqlite3')
	SECRET_KEY = "asfdkjni1knbkj45k2i224b7nks9012n4bbf97"
	SECURITY_PASSWORD_HASH = "bcrypt"
	SECURITY_PASSWORD_SALT = "KJKJkjkj365k2kjb1k246kn"
	SECURITY_REGISTERABLE = True
	SECURITY_SEND_REGISTER_EMAIL = False
	SECURTIY_UNAUTHORIZED_VIEW = None
	WTF_CSRF_ENABLED = False
	CELERY_BROKER_URL = "redis://localhost:6379/1"
	CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
