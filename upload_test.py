from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
# Your Supabase settings
api_key = os.environ["MISTRAL_API_KEY"]
SUPABASE_URL = os.environ["SUPABASE_URL"]  # replace this
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_API_KEY"]   # keep this secret

# Initialize the client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# File details
bucket_name = "story-assets"  # your bucket name
file_path = "hello.txt"
file_content = b"Hello from Supabase Python!"

# Write test file locally
with open(file_path, "wb") as f:
    f.write(file_content)

# Upload to Supabase
with open(file_path, "rb") as f:
    supabase.storage.from_(bucket_name).upload("test-folder/hello.txt", f)

print("✅ Uploaded hello.txt to Supabase Storage!")
