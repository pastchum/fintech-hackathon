import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    # Access environment variables
    OPENAI_APIKEY = os.getenv("OPENAI_APIKEY")  # Default value if not set

config = Config()
