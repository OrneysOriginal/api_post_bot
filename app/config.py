import os
from dotenv import load_dotenv


load_dotenv()


DB_NAME = os.getenv("POSTGRES_DB", "*")
DB_PORT = os.getenv("POSTGRES_PORT", "*")
DB_HOST = os.getenv("POSTGRES_HOST", "*")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "*")
DB_USER = os.getenv("POSTGRES_USER", "*")
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "*")
WEB_HOST = os.getenv("WEB_HOST", "*")
WEB_PORT = os.getenv("WEB_PORT", "*")
EXPIRE_MINUTES = int(os.getenv('EXPIRE_MINUTES', '1'))
SECRET_KEY = os.getenv('SECRET_KEY', '*')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
