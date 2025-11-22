import os
from config import DASHSCOPE_API_KEY, DATA_PATH, DB_PATH, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME

def test_config():
    print("Testing Configuration Loading...")
    print(f"DASHSCOPE_API_KEY present: {'Yes' if DASHSCOPE_API_KEY else 'No'}")
    print(f"DATA_PATH: {DATA_PATH}")
    print(f"DB_PATH: {DB_PATH}")
    print(f"EMBEDDING_MODEL_NAME: {EMBEDDING_MODEL_NAME}")
    print(f"LLM_MODEL_NAME: {LLM_MODEL_NAME}")
    
    if not DASHSCOPE_API_KEY:
        print("\n[WARNING] DASHSCOPE_API_KEY is missing. Please create a .env file with your API key.")
    else:
        print("\n[SUCCESS] Configuration loaded successfully.")

if __name__ == "__main__":
    test_config()
