from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from src.database.model.observing_directory_model import ObservingDirectoryModel
from src.database.schema import Base
from src.database.schema.observing_directory_table import ObservingDirectory
from typing import Optional, Sequence

# Define the client class for interacting with ObservingDirectory.
class ObservingDirectoryClient:
    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri)
        self.session = self.create_session()

    def create_session(self):
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        return Session()

    def upsert_observing_directory(self, path: str, active: bool = True) -> ObservingDirectoryModel:
        """Insert or update an observing directory."""
        observing_directory = ObservingDirectory(path=path, active=active)
        try:
            self.session.merge(observing_directory)
            self.session.commit()
            return ObservingDirectoryModel(path=path, active=active)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Invalid data provided.")

    def get_observing_directory_by_path(self, path: str, active: Optional[bool]) -> Optional[ObservingDirectoryModel]:
        """Get an observing directory by path."""
        query = self.session.query(ObservingDirectory).filter(ObservingDirectory.path == path)
        if active is not None:
            query = query.filter(ObservingDirectory.active == active)
        try:
            observing_directory = query.one()
            return ObservingDirectoryModel(path=observing_directory.path, active=observing_directory.active)
        except NoResultFound:
            return None

    def get_all(self) -> Sequence[ObservingDirectoryModel]:
        """Get all observing directories."""
        observing_directories = self.session.query(ObservingDirectory).all()
        return [
            ObservingDirectoryModel(path=observing_directory.path, active=observing_directory.active)
            for observing_directory in observing_directories
        ]

    def delete_all(self) -> None:
        """Delete all observing directories."""
        self.session.query(ObservingDirectory).delete()
        self.session.commit()
