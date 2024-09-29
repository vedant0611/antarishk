import firebase_admin
from firebase_admin import credentials, storage
import random
from datetime import timedelta
from google.cloud.storage.blob import Blob

cred = credentials.Certificate("config/antarshik.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'antashik-2709f.appspot.com'  
})

def get_random_image_url():
    bucket = storage.bucket()
    
    blobs = bucket.list_blobs()

    image_blobs = [blob for blob in blobs if blob.name.endswith(('.jpg', '.jpeg', '.png'))]

    if not image_blobs:
        return None  # No images found
    
    random_blob = random.choice(image_blobs)
    
    expiration_time = timedelta(hours=1)  # Token valid for 1 hour from now
    image_url = random_blob.generate_signed_url(expiration=expiration_time)

    return image_url

def main():
    random_image_url = get_random_image_url()
    
    if random_image_url:
        print(f"Random Image URL: {random_image_url}")
    else:
        print("No images found in the bucket.")
