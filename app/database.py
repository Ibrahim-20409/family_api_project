import csv
import os
from typing import List, Dict

# Get path to the /data folder from project root
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# File paths
FAMILY_FILE = os.path.join(DATA_DIR, "family.csv")
PERSON_FILE = os.path.join(DATA_DIR, "person.csv")

# ✅ Read CSV into list of dicts
def read_csv(filename: str) -> List[Dict[str, str]]:
    if not os.path.exists(filename):
        return []
    with open(filename, mode="r", newline='', encoding="utf-8") as f:
        return list(csv.DictReader(f))

# ✅ Write list of dicts to CSV
def write_csv(filename: str, data: List[Dict[str, str]], fieldnames: List[str]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
