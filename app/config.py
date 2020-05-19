class Config:
    SECRET_KEY = '6f430236b96d75aa5c3708d15ddcf345'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://demo:password@localhost/crud'    #dbSysName://user:password@host/dbname
    SQLALCHEMY_TRACK_MODIFICATIONS = False
