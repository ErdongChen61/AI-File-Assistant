from pydantic import BaseModel

# Define the Pydantic model for ObservingDirectory table.
class ObservingDirectoryModel(BaseModel):
    path: str
    active: bool
