"""
CSV File Cleaner - Use this instead of notebook for production
Or update the notebook cells with the code below
"""
import os
import glob
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import INPUT_CSV_DIR, PROCESSED_CSV_DIR, CSV_COLUMNS

print("=" * 50)
print("   PUB Realtime System - CSV File Cleaner")
print("=" * 50)

# Create directories if they don't exist
INPUT_CSV_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_CSV_DIR.mkdir(parents=True, exist_ok=True)

# Find all CSV files in input folder
all_files = glob.glob(str(INPUT_CSV_DIR / '*.csv'))
print(f"\n📁 Looking for CSV files in: {INPUT_CSV_DIR}")
print(f"✅ Found {len(all_files)} files to process\n")

if len(all_files) == 0:
    print("❌ No CSV files found!")
    print(f"   Please place your CSV files in: {INPUT_CSV_DIR}")
    sys.exit(1)

for file_path in all_files:
    print(f"Processing: {Path(file_path).name}")
    skip = 0

    # Find the row containing column headers
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if all(col in line for col in CSV_COLUMNS):
                skip = i
                break

    # Read CSV skipping rows above header
    df = pd.read_csv(file_path, skiprows=skip)

    # Keep only required columns
    df = df[[col for col in CSV_COLUMNS if col in df.columns]]

    # Create output filename with 'P' suffix before .csv
    base_name, ext = os.path.splitext(os.path.basename(file_path))
    output_file_name = f"{base_name}P{ext}"
    output_file_path = PROCESSED_CSV_DIR / output_file_name

    # Save processed file
    df.to_csv(output_file_path, index=False)
    print(f"   ✅ Saved: {output_file_name}\n")

print("=" * 50)
print("✅ Data processing complete!")
print(f"📁 Processed files saved in: {PROCESSED_CSV_DIR}")
print("=" * 50)