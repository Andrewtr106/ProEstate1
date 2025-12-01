import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///proestate.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SITE_NAME = 'ProEstate'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or 'your-openai-api-key-here'
