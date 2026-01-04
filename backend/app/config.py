import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////app/data/ars.db")

# Ensure data directory exists
data_dir = Path("/app/data")
data_dir.mkdir(parents=True, exist_ok=True)
