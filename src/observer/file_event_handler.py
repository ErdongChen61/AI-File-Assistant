import os
import threading
import time

from collections import defaultdict, deque
from enum import Enum
from src.extractor.text_extractor_factory import TextExtractorFactory
from typing import Dict, Tuple, Deque
from watchdog.observers import Observer
from watchdog.events import FileCreatedEvent, FileDeletedEvent, FileModifiedEvent, FileMovedEvent, FileSystemEventHandler

class FileEventType(Enum):
    MODIFICATION = 1
    DELETION = 2

class FileEventHandler(FileSystemEventHandler):
    """File event handler that groups events by file path and processes them asynchronously."""

    DEBOUNCE_SECONDS = 5

    def __init__(self) -> None:
        """Initialize the handler with an event queue and a worker thread."""
        self.event_queue: Dict[str, Deque[Tuple[FileEventType, float]]] = defaultdict(deque)
        self.event_worker = threading.Thread(target=self.process_events)
        self.stop_event = threading.Event()
        self.event_worker.start()

    def on_modified(self, event: FileModifiedEvent) -> None:
        """Handle a file modified event."""
        if not event.is_directory and ".DS_Store" not in event.src_path:
            self.event_queue[event.src_path].append((FileEventType.MODIFICATION, time.time()))

    def on_created(self, event: FileCreatedEvent) -> None:
        """Handle a file created event."""
        if not event.is_directory and ".DS_Store" not in event.src_path:
            self.event_queue[event.src_path].append((FileEventType.MODIFICATION, time.time()))

    def on_deleted(self, event: FileDeletedEvent) -> None:
        """Handle a file deleted event."""
        if not event.is_directory and ".DS_Store" not in event.src_path:
            self.event_queue[event.src_path].append((FileEventType.DELETION, time.time()))

    def on_moved(self, event: FileMovedEvent) -> None:
        """Handle a file moved event."""
        if not event.is_directory and ".DS_Store" not in event.src_path:
            cur_time = time.time()
            self.event_queue[event.src_path].append((FileEventType.DELETION, cur_time))
            self.event_queue[event.dest_path].append((FileEventType.MODIFICATION, cur_time))

    def _calculate_debounce_end_time(self) -> float:
        """Calculate debounce end time."""
        return time.time() - self.DEBOUNCE_SECONDS
    
    def _handle_event(self, path: str, event_type: FileEventType) -> None:
        """Handle a file event."""
        text_extractor = TextExtractorFactory.get_text_extractor(path)
        if text_extractor is None:
            return
        
        dir_name = os.path.dirname(path)
        file_name = os.path.basename(path)
        if event_type == FileEventType.MODIFICATION:
            # Handle file modification
            try:
                texts = text_extractor.extract_texts(path)
                print ("_handle_event MOD: " + path + " " + str(texts))
            except FileNotFoundError as e:
                print ("FileNotFoundError: " + str(e))
        elif event_type == FileEventType.DELETION:
            # Handle file deletion
            print ("_handle_event DEL: " + path)

    def _process_events(self) -> None:
        """Process all the events before debounce_end_time and handle the most recent event."""
        debounce_end_time = self._calculate_debounce_end_time()
        for file_path, events in list(self.event_queue.items()):
            event_type = None
            while events and events[0][1] < debounce_end_time:
                event_type, _ = events.popleft()
            if event_type:
                self._handle_event(file_path, event_type)
                

    def process_events(self) -> None:
        """Process events in a separate thread."""
        while not self.stop_event.is_set():
            self._process_events()
            time.sleep(2)

    def stop(self) -> None:
        """Stop processing events."""
        self.stop_event.set()
        self.event_worker.join()
