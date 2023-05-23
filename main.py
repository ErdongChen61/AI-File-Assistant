import logging
import uvicorn

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from langchain.docstore.document import Document
from pydantic import BaseModel
from src.database.client.observing_directory_client import ObservingDirectoryClient
from src.database.vector_embedding.chroma_client import ImageChromaClient, PdfChromaClient
from src.model.instructor_xl_embedding_model import InstructorXlEmbeddingModel
from src.observer.directory_observer import DirectoryObserver
from typing import Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
db_uri = "sqlite:////Users/samchen/Documents/GitHub/AI-File-Assistant/database/sqlite/database.db"

registered_directories = set()

class Directory(BaseModel):
    dir: str

class Query(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "dirs": registered_directories})

@app.post("/register")
async def register_directory(directory: Directory):
    try:
        if dir not in registered_directories:
            registered_directories.add(directory.dir)
            app.state.observing_directory_client.upsert_observing_directory(directory.dir, True)
            app.state.directory_observer.register_path(directory.dir)
        return {"message": "Directory registered", "registered_directories": registered_directories}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/unregister")
async def unregister_directory(directory: Directory):
    try:
        if directory.dir in registered_directories:
            registered_directories.remove(directory.dir)
            app.state.observing_directory_client.upsert_observing_directory(directory.dir, False)
            app.state.directory_observer.unregister_path(directory.dir)
        return {"message": "Directory unregistered", "registered_directories": registered_directories}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query_pdfs", response_model=List[Document])
async def query_pdfs(query: Query):
    try:
        results = app.state.pdf_chroma_client.similarity_search(query.query)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query_images", response_model=List[Document])
async def query_images(query: Query):
    try:
        results = app.state.image_chroma_client.similarity_search(query.query)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
async def startup_event():
    app.state.embedding_model = InstructorXlEmbeddingModel()
    app.state.observing_directory_client = ObservingDirectoryClient(db_uri)
    app.state.directory_observer = DirectoryObserver()
    for active_directory in app.state.observing_directory_client.get_all_active():
        registered_directories.add(active_directory.path)
        app.state.directory_observer.register_path(active_directory.path)
    app.state.image_chroma_client = ImageChromaClient(app.state.embedding_model)
    app.state.pdf_chroma_client = PdfChromaClient(app.state.embedding_model)

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shut down server")
    app.state.directory_observer.stop()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
