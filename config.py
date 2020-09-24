import os

base_dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, "database.db")
class Config(object):
    MS_TRANSLATOR_KEY = "409640cd5bmsh04d2c025714ba4fp1e1eafjsncc3296416d7b"
    LANGUAGES = ['en','es']
    POSTS_PER_PAGE  = 4
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kanjurus'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{data_dir}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    #mail server setup
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587) 
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or False
    MAIL_DEBUG = os.environ.get('MAIL_DEBUG') or False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAX_EMAIL = int(os.environ.get('MAX_EMAIL')  or 2 ) 
    MAIL_SUPPRESS_SEND = os.environ.get('MAIL_SUPPRESS_SEND') or False
    MAIL_ASCII_ATTACHMENTS = os.environ.get('MAIL_ASCII_ATTACHMENTS') or False
    ADMINS = ['kanjurus8@gmail.com', 'vivianwanga@gmail.com', 'kanjurus@yahoo.com', 'kanjurus30@gmail.com', 'faithwangechi86@yahoo.com ']
    
    
    