import os

SQLALCHEMY_DATABASE_URI = f'sqlite:///alarm-app-db.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SOUND_FILE_DIR = f'{os.getcwd()}/resources/mp3'
