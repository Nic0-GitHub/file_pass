import os
from dotenv import load_dotenv


load_dotenv('.env')
USERS_FILE = os.getenv('USERS_FILE', './users.json')
USERS_FILE_EXAMPLE = os.getenv('USERS_FILE_EXAMPLE', './users.example.json')
LOGS_DIR = os.getenv('LOGS_DIR', './logs')
UPLOAD_DIR = os.getenv("UPLOAD_DIR", './upload')
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", './download')
ICONS_DIR = os.getenv("ICONS_DIR", './icons')
SECRET_KEY = os.getenv("SECRET_KEY", '124-568-790')

# Create dirs if not created yet
os.makedirs(UPLOAD_DIR,   exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(LOGS_DIR,     exist_ok=True)