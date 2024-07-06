from datetime import datetime
from pathlib import Path
from flask_login import UserMixin
from constants import *
from enum import Enum
import os.path

class FileTypes(Enum):
    CODE = 1
    IMAGE = 2
    VIDEO = 3
    DOCUMENT = 4
    COMPRESS = 5
    AUDIO = 6

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class ProvidedItem():
    """ This object is used to be passed and be represented in index"""
    def __init__(self, path: str) -> None:
        # assert that the file exist it self or if is in UPLOAD/DOWNLOAD DIRS
        self.path = Path(path)
        self.validate_path()
        self.full_path = self.get_full_path()
        self.name = self.path.name
        self.raw_name = self.path.stem
        
        creation_timestamp = self.full_path.stat().st_ctime
        self.birth_date = datetime.fromtimestamp(creation_timestamp)
        self.birth_date_str = self.birth_date.strftime("%Y/%m/%d %H:%M")
   
        self.ext = self.path.suffix
        self.file_type = self.select_file_type()
        self.icon = self.select_icon()

    def get_full_path(self) -> Path:
        a = self.path
        b = Path(DOWNLOAD_DIR) / self.path
        c = Path(UPLOAD_DIR) / self.path
        if (a.exists()):
            return a
        if (b.exists()):
            return b
        if (c.exists()):
            return c       
    def validate_path(self) -> Path:
        """ Raise FileNotFoundError if the path do not exist """
        a = self.path
        b = Path(DOWNLOAD_DIR) / self.path
        c = Path(UPLOAD_DIR) / self.path
        
        if not (a.exists() or b.exists() or c.exists()):
            raise FileNotFoundError(f"El archivo no se encuentra en la ruta especificada: {self.path}")
        

        
    def select_file_type(self) -> FileTypes:
        ext_to_type = {
            '.c': FileTypes.CODE, '.py': FileTypes.CODE, '.cpp': FileTypes.CODE, 
            '.java': FileTypes.CODE, '.js': FileTypes.CODE, '.ts': FileTypes.CODE, 
            '.php': FileTypes.CODE, '.rb': FileTypes.CODE, '.go': FileTypes.CODE, 
            '.rs': FileTypes.CODE, '.css': FileTypes.CODE, '.png': FileTypes.IMAGE, 
            '.jpg': FileTypes.IMAGE, '.jpeg': FileTypes.IMAGE, '.gif': FileTypes.IMAGE, 
            '.bmp': FileTypes.IMAGE, '.svg': FileTypes.IMAGE, '.mp4': FileTypes.VIDEO, 
            '.mkv': FileTypes.VIDEO, '.flv': FileTypes.VIDEO, '.avi': FileTypes.VIDEO, 
            '.mov': FileTypes.VIDEO, '.txt': FileTypes.DOCUMENT, '.doc': FileTypes.DOCUMENT, 
            '.docx': FileTypes.DOCUMENT, '.xls': FileTypes.DOCUMENT, '.xlsx': FileTypes.DOCUMENT, 
            '.ppt': FileTypes.DOCUMENT, '.pptx': FileTypes.DOCUMENT, '.pdf': FileTypes.DOCUMENT, 
            '.zip': FileTypes.COMPRESS, '.tar': FileTypes.COMPRESS, '.rar': FileTypes.COMPRESS, 
            '.tar.gz': FileTypes.COMPRESS, '.bz2': FileTypes.COMPRESS, '.mp3': FileTypes.AUDIO, 
            '.wav': FileTypes.AUDIO, '.aac': FileTypes.AUDIO, '.flac': FileTypes.AUDIO, 
            '.ogg': FileTypes.AUDIO, '.wma': FileTypes.AUDIO
        }
        
        return ext_to_type.get(self.ext, FileTypes.DOCUMENT)

    def select_icon(self) -> str:
        if self.path.is_dir():
            return 'folder.png'
        
        ext_to_icon = {
            'code.png': ('.c', '.py', '.cpp', '.java', '.js', '.ts', '.php', '.rb', '.go', '.rs', '.css'),
            'image.png': ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg'),
            'video.png': ('.mp4', '.mkv', '.flv', '.avi', '.mov'),
            'document.png': ('.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf'),
            'compress.png': ('.zip', '.tar', '.rar', 'tar.gz', '.zip2'),
            'audio.png': ('.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma')
        }

        file_ext = self.ext.lower()
        for icon, extensions in ext_to_icon.items():
            if file_ext in extensions:
                return icon
        return 'default.png'
    
    def __str__(self):
        t = f"""\
        \npath: {self.path.resolve()}\
        \nname: {self.name}\
        \nicon: {self.icon}\
        \nbirth_date:{self.birth_date}\
        \nbirth_date_str:{self.birth_date_str}
        """
        
        return t


if __name__ == '__main__':
    p = ProvidedItem("./static/templates/login.html")
    print(p)