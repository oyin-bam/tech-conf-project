import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="techconf-db-server.postgres.database.azure.com"
    POSTGRES_USER="bambam@techconf-db-server"
    POSTGRES_PW="Akinyemi1#"
    POSTGRES_DB="techconfdb"
    POSTGRES_PORT="5432"
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://techconf-servicebus.servicebus.windows.net/;SharedAccessKeyName=RootManagedSharedAccessKey;SharedAccessKey=pRXSa0b/dIMEY9Mi3oJFlcL/pPSshmzevXW5gQ/+FP8=;EntityPath=notificationqueue'
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'harjacober@gmail.com'
    SENDGRID_API_KEY = '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' 

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False