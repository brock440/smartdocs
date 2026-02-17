import hashlib
import boto3
from dotenv import load_dotenv
from google import genai
import os
import io

load_dotenv()

class DocumentHandler:
    def __init__(self, name=None, metadata=None, data=None):
        self.name = name
        self.metadata = metadata
        self.data = data
        self.s3 = boto3.client('s3')
    
    
    @classmethod
    async def for_upload(cls, document):
        data = await document.file.read()
        metadata = {
            'name': document.name,
            'file_type': document.file_type,
            'file_size': document.file_size,
            'file_hash': document.file_hash
        }
        return cls(metadata['name'], metadata, data)
    
    @classmethod
    async def for_s3(cls, name):
        """
        This is for downloading/deletion of files from S3
        verify_document is not required for this class
        """
        return cls(name)

    def verify_document(self):
        """This is not required for downloading/deletion of files from S3"""
        if self.data is None or self.metadata is None:
            raise ValueError("verify_document requires data and metadata; not available for S3 download/delete instances")
        
        file_hash = hashlib.sha256(self.data).hexdigest()
        if self.metadata['file_hash'] != file_hash:
            return False
        
        return True
    

    def save_document(self):
        self.s3.put_object(Bucket='suplyne-smartdocs', Key=self.name, Body=self.data)

    
    def get_document(self):
        return self.s3.get_object(Bucket='suplyne-smartdocs', Key=self.name)



    def update_document(self):
        pass


    def process_document(self):
        document = self.s3.get_object(Bucket='suplyne-smartdocs', Key=self.name)
        client = genai.Client(api_key=os.getenv('GEMINI_AI_KEY'))
        file_data = io.BytesIO(document['Body'].read())
        uploaded_file = client.files.upload(file=file_data, config={'mime_type': 'application/pdf'})
        
        while uploaded_file.state.name == "PROCESSING":
            print("Waiting for PDF to be indexed...")
            time.sleep(2)
            uploaded_file = client.files.get(name=uploaded_file.name)
        
        if uploaded_file.state.name == "FAILED":
            raise ValueError("PDF processing failed on Gemini's side.")
        
        prompt = """
        Please analyze this Bill of Lading (BL). 
        Extract the following in JSON format:
        - Shipper Name
        - Consignee Name
        - Container Numbers
        - Port of Loading
        - Total Weight
        """
    
        result = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[uploaded_file, prompt]
        )
        
        print(result.text)



    def delete_document(self):
        self.s3.delete_object(Bucket='suplyne-smartdocs', Key=self.name)

