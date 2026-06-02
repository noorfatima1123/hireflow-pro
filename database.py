import json
import os
from pathlib import Path

DB_FILE = Path(__file__).parent / "data.json"

def load_db():
    """Database ko read karta hai"""
    if not os.path.exists(DB_FILE):
        # Agar file nahi hai to empty database create karo
        empty_db = {"users": [], "jobs": [], "candidates": []}
        save_db(empty_db)
        return empty_db
    
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    """Database ko save karta hai"""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_user(user_data):
    """Naya user add karta hai"""
    db = load_db()
    db["users"].append(user_data)
    save_db(db)
    return user_data

def get_user_by_email(email):
    """Email se user dhundta hai"""
    db = load_db()
    for user in db["users"]:
        if user["email"] == email:
            return user
    return None