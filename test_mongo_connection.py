from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI and tlsCAFile from the environment
uri = os.getenv('URI_FOR_Mongo')
tlsCAFile = os.getenv('tlsCAFile')

try:
    # Create MongoClient with the correct URI and TLS certificate
    client = MongoClient(uri, tlsCAFile=tlsCAFile)

    # Try to list the databases to ensure the connection works
    print("Available databases:", client.list_database_names())
    print("Connection to MongoDB successful!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
