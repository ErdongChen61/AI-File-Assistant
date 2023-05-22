import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from src.observer.directory_observer import DirectoryObserver
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

registered_directories = set()

class Directory(BaseModel):
    dir: str

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "dirs": registered_directories})

@app.post("/register")
async def register_directory(directory: Directory):
    if dir not in registered_directories:
        registered_directories.add(directory.dir)
        app.state.directory_observer.register_path(directory.dir)
    return {"message": "Directory registered", "registered_directories": registered_directories}

@app.post("/unregister")
async def unregister_directory(directory: Directory):
    if directory.dir in registered_directories:
        registered_directories.remove(directory.dir)
        app.state.directory_observer.unregister_path(directory.dir)
    return {"message": "Directory unregistered", "registered_directories": registered_directories}

@app.on_event("startup")
async def startup_event():
    # Initialize and start the DirectoryObserver.
    app.state.directory_observer = DirectoryObserver()

@app.on_event("shutdown")
def shutdown_event():
    # Stop and cleanup the DirectoryObserver here
    app.state.directory_observer.stop()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
