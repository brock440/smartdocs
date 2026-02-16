import hashlib
import boto3
from dotenv import load_dotenv

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
        pass


    def delete_document(self):
        self.s3.delete_object(Bucket='suplyne-smartdocs', Key=self.name)

