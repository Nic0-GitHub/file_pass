from pathlib import Path
from flask_login import UserMixin
import os.path
from utils import DOWNLOAD_DIR, UPLOAD_DIR, ICONS_DIR, get_files

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
        self.name = self.path.name
        self.raw_name = self.path.stem
        self.ext = self.path.suffix
        self.icon = self.select_icon()

    def validate_path(self) -> None:
        """ Raise FileNotFoundError if the path do not exist """
        if not (self.path.exists() or
                (Path(DOWNLOAD_DIR) / self.path).exists() or
                (Path(UPLOAD_DIR) / self.path).exists()):
            raise FileNotFoundError(f"El archivo no se encuentra en la ruta especificada: {self.path}")


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
