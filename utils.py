
import os


def get_files(dir:str) -> list[str]:
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]