from flask_login import UserMixin
from os.path import exists, basename, split
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class ProvidedItem():
    """ This object is used to be passed and be represented in index"""
    def __init__(self, path: str, icon:str) -> None:
        assert exists(path) and exists(icon), f"incorrect paths passed to file: '{path}', '{icon}'"
        self.name, _ = split(basename(path))
        self.path = path
        self.icon = icon
    
    