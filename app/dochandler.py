import hashlib


class DocumentHandler:
    def __init__(self, document, data):
        self.document = document
        self.name = document.name
        self.file_type = document.file_type
        self.file_size = document.file_size
        self.file_hash = document.file_hash
        self.data = data
    
    @classmethod
    async def create(cls, document):
        data = await document.file.read()
        return cls(document, data)

    def verify_document(self):
        if self.file_hash != hashlib.sha256(self.data).hexdigest():
            raise ValueError("File hash does not match")


    def save_document(self):
        pass

    
    def get_document(self):
        pass


    def update_document(self):
        pass


    def process_document(self):
        pass


    def delete_document(self):
        pass

