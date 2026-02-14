"""
Centralized configuration for PUB Realtime System
"""
import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Data directories
CLEANER_DIR = PROJECT_ROOT / "cleaner"
INPUT_CSV_DIR = CLEANER_DIR / "input_.csv_file"
PROCESSED_CSV_DIR = CLEANER_DIR / "processed_.csv_file"

# Ensure directories exist
PROCESSED_CSV_DIR.mkdir(parents=True, exist_ok=True)

# API Configuration
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))

# CSV Configuration
DEFAULT_CSV_FILE = "PUB_Demand_2024.csv"
CSV_COLUMNS = ["Date", "Hour", "Ontario Demand"]

# Request Configuration
REQUEST_DELAY = int(os.getenv("REQUEST_DELAY", 1))  # seconds between requests