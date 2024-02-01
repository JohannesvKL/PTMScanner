import shutil
from pathlib import Path

class DirectoryManager:
    # Methods related to directory management
    def __init__(self):
        pass

    def ensure_directory_exists(self, directory: str, reset: bool = False) -> str:
        if reset:
            shutil.rmtree(directory, ignore_errors=True)
        if not Path(directory).exists():
            Path(directory).mkdir(parents=True, exist_ok=True)
        return directory