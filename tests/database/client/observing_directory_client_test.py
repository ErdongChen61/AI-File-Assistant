import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.client.observing_directory_client import ObservingDirectoryClient

class TestObservingDirectoryClient:
    @pytest.fixture
    def observing_directory_client(self):
        db_uri = "sqlite:///:memory:"
        client = ObservingDirectoryClient(db_uri)
        yield client
        client.delete_all()

    def test_upsert_observing_directory(self, observing_directory_client):
        path = "/path/to/directory"
        active = True

        # Insert a new observing directory
        result = observing_directory_client.upsert_observing_directory(path, active)
        assert result.path == path
        assert result.active == active

        # Update the observing directory
        new_active = False
        result = observing_directory_client.upsert_observing_directory(path, new_active)
        assert result.path == path
        assert result.active == new_active

    def test_get_all(self, observing_directory_client):
        path1 = "/path/to/directory1"
        active1 = True
        path2 = "/path/to/directory2"
        active2 = False

        # Insert observing directories
        observing_directory_client.upsert_observing_directory(path1, active1)
        observing_directory_client.upsert_observing_directory(path2, active2)

        # Get all observing directories
        result = observing_directory_client.get_all()
        assert len(result) == 2
        assert result[0].path == path1
        assert result[0].active == active1
        assert result[1].path == path2
        assert result[1].active == active2

    def test_delete_all(self, observing_directory_client):
        path = "/path/to/directory"
        active = True

        # Insert an observing directory
        observing_directory_client.upsert_observing_directory(path, active)

        # Get the observing directory by path
        observing_directory_client.delete_all()
        result = observing_directory_client.get_all()
        assert len(result) == 0
