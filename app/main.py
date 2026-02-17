from fastapi import UploadFile, File, Form
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from botocore.exceptions import ClientError
from urllib.parse import quote
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
    document_handler = await DocumentHandler.for_upload(document)    
    if document_handler.verify_document():
        document_handler.save_document()
        return {'status': 'ok'}
    else:
        return {'status': 'File hash does not match'}


@app.get('/download/{name}')
async def download_file(name: str):
    try:
        document_handler = await DocumentHandler.for_s3(name)
        response = document_handler.get_document()
        file_stream = response['Body']
        content_type = response.get('ContentType', 'application/octet-stream')

        return StreamingResponse(
            file_stream, 
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(name)}"}
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise HTTPException(status_code=404, detail='File not found')
    
        raise HTTPException(status_code=500, detail='Internal server error')

@app.post('/process')
async def process_document(name: str):
    document_handler = await DocumentHandler.for_s3(name)
    document_handler.process_document()
    return {'status': 'ok'}

@app.delete('/delete/{name}')
async def delete_file(name: str):
    document_handler = await DocumentHandler.for_s3(name)
    document_handler.delete_document()
    return {'status': 'ok'}

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)