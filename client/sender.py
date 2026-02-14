import pandas as pd
import time
import requests
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import PROCESSED_CSV_DIR, API_URL, REQUEST_DELAY, DEFAULT_CSV_FILE

# Construct CSV path
csv_path = PROCESSED_CSV_DIR / DEFAULT_CSV_FILE

# Check if file exists
if not csv_path.exists():
    print(f"❌ ERROR: CSV file not found at {csv_path}")
    print(f"   Please run 'CSV File Cleaner.ipynb' first to process CSV files.")
    sys.exit(1)

print(f"✅ Found CSV file: {csv_path}")
filename = csv_path.name
df = pd.read_csv(csv_path)
print(f"📊 Loaded {len(df)} rows from {filename}\n")

for idx, row in df.iterrows():
    data = row.to_dict()
    print(f"📤 Sending row {idx+1}/{len(df)} from {filename}")

    try:
        response = requests.post(f"{API_URL}/ingest", json=data, timeout=10)
        print(f"   ✅ Server Response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error sending data: {e}")

    time.sleep(REQUEST_DELAY)

print("\n✅ Data transmission complete!")