import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Use for local database
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mh4913@localhost:5432/postgres'
    # New database
    # SQLALCHEMY_DATABASE_URI = 'postgresql://flaskuser:mh4913@localhost:5432/flaskdb'
    # Use for Heroku database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['mark.hoffman9@gmail.com']
    POSTS_PER_PAGE = 25
    LANGUAGES =  ['en', 'es']
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    UPLOAD_FOLDER = '/home/mark/PythonFlaskVertica'