import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

if not DASHSCOPE_API_KEY:
    print("Warning: DASHSCOPE_API_KEY not found in environment variables or .env file.")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "sample.docx")
DB_PATH = os.path.join(BASE_DIR, "chroma_db")

# Models
EMBEDDING_MODEL_NAME = "text-embedding-v1"
LLM_MODEL_NAME = "qwen-turbo"
MAX_RETRIES = 3
