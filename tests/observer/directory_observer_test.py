import os
import pytest
from unittest.mock import Mock, patch

from src.observer.directory_observer import DirectoryObserver
from src.observer.file_event_handler import FileEventHandler
from watchdog.observers import Observer

class TestDirectoryObserver:
    def setup_method(self):
        self.observer = DirectoryObserver()

    @patch('os.path.isdir')
    @patch('src.observer.directory_observer.FileEventHandler')
    @patch('src.observer.directory_observer.Observer')
    def test_register_path(self, mock_observer_class, mock_event_handler_class, mock_isdir):
        mock_observer = Mock(spec=Observer)
        mock_observer_class.return_value = mock_observer
        mock_event_handler = Mock(spec=FileEventHandler)
        mock_event_handler_class.return_value = mock_event_handler
        mock_isdir.return_value = True

        self.observer.register_path('/test/path')

        mock_observer_class.assert_called_once_with()
        mock_event_handler_class.assert_called_once_with()
        mock_observer.schedule.assert_called_once_with(mock_event_handler, '/test/path', recursive=True)
        mock_observer.start.assert_called_once_with()

        assert self.observer.observers['/test/path'] == (mock_observer, mock_event_handler)

    def test_register_path_invalid_directory(self):
        with pytest.raises(ValueError) as e:
            self.observer.register_path('/invalid/path')

        assert str(e.value) == 'Path is not valid: /invalid/path'

    @patch('os.path.isdir')
    @patch('src.observer.directory_observer.FileEventHandler')
    @patch('src.observer.directory_observer.Observer')
    def test_unregister_path(self, mock_observer_class, mock_event_handler_class, mock_isdir):
        mock_observer = Mock(spec=Observer)
        mock_observer_class.return_value = mock_observer
        mock_event_handler = Mock(spec=FileEventHandler)
        mock_event_handler_class.return_value = mock_event_handler
        mock_isdir.return_value = True

        self.observer.register_path('/test/path')
        self.observer.unregister_path('/test/path')

        mock_observer.stop.assert_called_once_with()
        mock_event_handler.stop.assert_called_once()
        mock_observer.join.assert_called_once_with()
        assert '/test/path' not in self.observer.observers

    def test_unregister_path_not_present(self):
        # This should not raise any exceptions.
        self.observer.unregister_path('/test/path')
