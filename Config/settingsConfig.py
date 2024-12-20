#Config/settings.py
from dotenv import load_dotenv
import os

# Carga las variables de entorno
load_dotenv(".env.development")

class settingsConfig:
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    HOST = os.getenv("HOST")
    SERVICE_NAME = os.getenv("SERVICE_NAME")
    PORT = os.getenv("PORT")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    APIHOST= os.getenv("HOSTAPI")
    APIPORT= os.getenv("HOSTPORT")
    DEBUG= os.getenv("DEBUG")

settings = settingsConfig()