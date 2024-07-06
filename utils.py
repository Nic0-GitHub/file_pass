from logging import Formatter, FileHandler, StreamHandler
import os, shutil
from dotenv import load_dotenv
import json
from classes import FileTypes, ProvidedItem
from constants import *



def get_users_from_json(users_file: str = USERS_FILE) -> dict:
    """ Gets the users from the path passed (if exists), uses USERS_FILE_EXAMPLE otherwise """
    if not os.path.isfile(users_file):
        print(f"User file not found at '{users_file}', using default")
        # if users not set yet
        if not os.path.isfile(USERS_FILE):
            shutil.copy(USERS_FILE_EXAMPLE, USERS_FILE)
        users_file = USERS_FILE

    with open(users_file, 'r') as file:
        return json.load(file)
        
def get_files(dir: str, with_path=False, sort_by_birth_date=False) -> list[str]:
    with_path_enabled = lambda f: f if not with_path else os.path.join(dir, f)
    
    try:
        paths_in_dir = os.listdir(dir)
        files = [f for f in paths_in_dir if os.path.isfile(os.path.join(dir, f))]
        
        if sort_by_birth_date:
            files.sort(key=lambda f: os.path.getctime(os.path.join(dir, f)))
            
        ret = [with_path_enabled(f) for f in files]
    except NotADirectoryError:
        return []
    return ret


def group_provided_items_by_type(provided_items: list[ProvidedItem]) -> dict[FileTypes, list[ProvidedItem]]:
    grouped_items = {
        FileTypes.CODE: [],
        FileTypes.IMAGE: [],
        FileTypes.VIDEO: [],
        FileTypes.DOCUMENT: [],
        FileTypes.COMPRESS: [],
        FileTypes.AUDIO: []
    }
    for item in provided_items:
        grouped_items[item.file_type].append(item)
    return grouped_items

# Logger
bsc_formatter = Formatter("[%(levelname)s] -> [%(asctime)s]: %(message)s", '%d/%m/%Y %H:%M')

file_handler = FileHandler(os.path.join(LOGS_DIR, 'app.log'))
stream_handler = StreamHandler()

file_handler.setFormatter(bsc_formatter)
stream_handler.setFormatter(bsc_formatter)
