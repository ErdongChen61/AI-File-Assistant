from sqlalchemy import Column, String, Boolean
from src.database.schema import Base

# Define the ObservingDirectory schema.
class ObservingDirectory(Base):
    __tablename__ = "observing_directory"

    path = Column(String(255), primary_key=True, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
