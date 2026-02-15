from fastapi import UploadFile, File, Form
from fastapi import FastAPI
from pydantic import BaseModel
from dochandler import DocumentHandler
import uvicorn


app = FastAPI()

class Document(BaseModel):
    name: str
    file_type: str
    file_size: int
    file_hash: str
    file: UploadFile


@app.get('/')
async def heartbeat():
    return {'status': 'ok'}


@app.post('/upload')
async def upload_file(
    file_type: str = Form(...), 
    file_size: int = Form(...), 
    file_hash: str = Form(...), 
    file: UploadFile = File(...)
):
    document = Document(name=file.filename, file_type=file_type, file_size=file_size, file_hash=file_hash, file=file)
    document_handler = await DocumentHandler.create(document)
    document_handler.verify_document()
    return {'status': 'ok'}

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)