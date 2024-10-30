import os


class Config:
  SQLALCHEMY_DATABASE_URI = 'sqlite:///example.db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = 'FLASK_SQL_TEST'
  UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
  # MAX_CONTENT_LENGTH = 16 * 1024 * 1024