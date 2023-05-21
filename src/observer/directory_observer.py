import os

from src.observer.file_event_handler import FileEventHandler
from typing import Dict
from watchdog.observers import Observer

class DirectoryObserver:
    """This class will observe directories for any file changes."""
    
    def __init__(self) -> None:
        self.observers: Dict[str, Tuple[Observer, FileEventHandler]] = {}
        
    def register_path(self, path: str) -> None:
        """Register an observing directory."""
        if path in self.observers:
            return
        if not os.path.isdir(path):
            raise ValueError('Path is not valid: {}'.format(path))

        observer = Observer()
        event_handler = FileEventHandler()
        observer.schedule(event_handler, path, recursive=True)
        self.observers[path] = (observer, event_handler)
        observer.start()

    def unregister_path(self, path: str) -> None:
        """Unregister an observing directory."""
        if path not in self.observers:
            return

        observer, event_handler = self.observers.pop(path)
        observer.stop()
        event_handler.stop()
        observer.join()
       
    def stop(self) -> None:
        """Stop observing all directories."""
        for path in list(self.observers.keys()):
            self.unregister_path(path)