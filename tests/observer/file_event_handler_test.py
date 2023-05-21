import pytest
import time

from collections import deque
from src.observer.file_event_handler import FileEventHandler, FileEventType  
from watchdog.events import FileModifiedEvent, FileCreatedEvent, FileDeletedEvent, FileMovedEvent
from unittest.mock import patch, MagicMock

class TestFileEventHandler:
    @pytest.fixture
    def handler(self):
        return FileEventHandler()

    @pytest.fixture
    def mock_time(self):
        with patch('time.time', return_value=12345):
            yield

    def test_on_modified(self, handler, mock_time):
        event = FileModifiedEvent("/path/to/file")
        handler.on_modified(event)
        assert handler.event_queue[event.src_path] == deque([(FileEventType.MODIFICATION, 12345)])

    def test_on_created(self, handler, mock_time):
        event = FileCreatedEvent("/path/to/file")
        handler.on_created(event)
        assert handler.event_queue[event.src_path] == deque([(FileEventType.MODIFICATION, 12345)])

    def test_on_deleted(self, handler, mock_time):
        event = FileDeletedEvent("/path/to/file")
        handler.on_deleted(event)
        assert handler.event_queue[event.src_path] == deque([(FileEventType.DELETION, 12345)])

    def test_on_moved(self, handler, mock_time):
        event = FileMovedEvent("/path/from/file", "/path/to/file")
        handler.on_moved(event)
        assert handler.event_queue[event.src_path] == deque([(FileEventType.DELETION, 12345)])
        assert handler.event_queue[event.dest_path] == deque([(FileEventType.MODIFICATION, 12345)])

    def test_calculate_debounce_end_time(self, handler, mock_time):
        assert handler._calculate_debounce_end_time() == 12345 - handler.DEBOUNCE_SECONDS

    def test_process_events(self, handler, mock_time):
        event_path = "/path/to/file"
        handler.event_queue[event_path] = deque([(FileEventType.MODIFICATION, 12345 - handler.DEBOUNCE_SECONDS - 1)])
        with patch.object(handler, "_handle_event") as mock_handle_event:
            handler._process_events()
        mock_handle_event.assert_called_once_with(event_path, FileEventType.MODIFICATION)