from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client
import io

class SupabaseStorage(Storage):
    def __init__(self, bucket_name=None):
        # Initialize Supabase client
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.bucket_name = bucket_name or settings.SUPABASE_BUCKET_NAME
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.bucket = self.supabase.storage.from_(self.bucket_name)

    def _save(self, name, content):
        try:
            content_bytes = content.read()
            self.bucket.upload(name, content_bytes, {'content-type':content.content_type, "x-upsert": 'true'})
        except Exception as e:
            print(f'Error uploading file to Supabase: {e}')
            
    def save(self, name, content, max_length=None):
        # Ensure the custom save method calls _save
        return self._save(name, content)
    
    def delete(self, name):
        # Delete a file from Supabase
        try:
            self.bucket.remove([name])
        except Exception as e:
            print(f'Error deleting file from Supabase: {e}')

    def url(self, name):
        # Return URL to access the file
        try:
            return self.bucket.get_public_url(name)
        except Exception as e:
            print(f'Error getting URL to access the file in Supabase: {e}')

    def exists(self, name):
        # Check if file exists in Supabase storage
        try:
            self.bucket.download(name)
            return True
        except Exception as e:
            if 'not_found' in str(e):  # 404 error means file doesn't exist
                return False
            print(f'Error checking if file exists in Supabase: {e}')
    
    def _open(self, name, mode='rb'):
        # You can implement this method if you need to read files back
        try:
            file = self.bucket.download(name)
            # Convert the binary data to a BytesIO object
            image_data = io.BytesIO(file)
            return image_data
        except Exception as e:
            print(f'Error downloading file to Supabase: {e}')
    
    def open(self, name, mode='rb'):
        return self._open(name)
    
    def listdir(self, path):
        # List files in a given path in the Supabase storage.
        result = self.bucket.list(path)
        files = [file['name'] for file in result]
        dirs = []  # Supabase doesn't have directories as such
        return dirs, files
