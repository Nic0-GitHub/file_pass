from logging import Formatter, FileHandler, StreamHandler, LogRecord
import os, shutil
from dotenv import load_dotenv
import json

load_dotenv('.env')
USERS_FILE = os.getenv('USERS_FILE', './users.json')
USERS_FILE_EXAMPLE = os.getenv('USERS_FILE_EXAMPLE', './users.example.json')
LOGS_DIR = os.getenv('LOGS_DIR', './logs')

def get_users_from_json(users_file: str = USERS_FILE) -> dict:
    if not os.path.isfile(users_file):
        print(f"User file not found at '{users_file}', using default")
        # if users not set yet
        if not os.path.isfile(USERS_FILE):
            shutil.copy(USERS_FILE_EXAMPLE, USERS_FILE)
        users_file = USERS_FILE

    with open(users_file, 'r') as file:
        return json.load(file)
        
def get_files(dir:str) -> list[str]:
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
bsc_formatter = Formatter("[%(levelname)s] -> [%(asctime)s]: %(message)s", '%d/%m/%Y %H:%M')

file_handler = FileHandler(os.path.join(LOGS_DIR, 'app.log'))
stream_handler = StreamHandler()

file_handler.setFormatter(bsc_formatter)
stream_handler.setFormatter(bsc_formatter)