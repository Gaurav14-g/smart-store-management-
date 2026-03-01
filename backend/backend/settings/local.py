from .base import *
import os
from dotenv import load_dotenv
load_dotenv(override=True)

# Determine which database to use based on flags
if os.getenv("USE_LOCAL") == "true":
    USER = os.getenv("L_USER")
    HOST = os.getenv("L_HOST")
    PORT = os.getenv("L_PORT")
    DB = os.getenv("L_DB")
    PASS = os.getenv("L_PASS")
elif os.getenv("USE_DEV") == "true":
    USER = os.getenv("D_USER")
    HOST = os.getenv("D_HOST")
    PORT = os.getenv("D_PORT")
    DB = os.getenv("D_DB")
    PASS = os.getenv("D_PASS")
elif os.getenv("USE_STAGE") == "true":
    USER = os.getenv("S_USER")
    HOST = os.getenv("S_HOST")
    PORT = os.getenv("S_PORT")
    DB = os.getenv("S_DB")
    PASS = os.getenv("S_PASS")
elif os.getenv("USE_PROD") == "true":
    USER = os.getenv("P_USER")
    HOST = os.getenv("P_HOST")
    PORT = os.getenv("P_PORT")
    DB = os.getenv("P_DB")
    PASS = os.getenv("P_PASS")
else:
    # Default to local if no flag is set
    USER = os.getenv("L_USER")
    HOST = os.getenv("L_HOST")
    PORT = os.getenv("L_PORT")
    DB = os.getenv("L_DB")
    PASS = os.getenv("L_PASS")

DEBUG = True
ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [ 
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB,
        'USER': USER,
        'PASSWORD': PASS,
        'HOST': HOST,
        'PORT':PORT,
    }
}

BASE_URL = os.getenv("BASE_URL")