import os
from pathlib import Path

from dotenv import load_dotenv

# Load the .env file from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Required for asyncpg (init_db)
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

# Required for REST API access
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Optional default port for app run
APP_PORT = int(os.getenv("APP_PORT", 8080))

STORAGE_SECRET = os.getenv("STORAGE_SECRET", "fallback-dev-secret")

SECRET_KEY = os.getenv("SERVER_SIGNATURE_KEY", "fallback-dev-secret")
