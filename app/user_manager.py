# user_manager.py

import json
import os
from datetime import datetime
import re

def is_valid_email(email: str) -> bool:
    email = email.strip()
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

# Define the storage file
user_file = "user_profiles.json"

# Load existing users or create an empty list
if os.path.exists(user_file):
    with open(user_file, "r", encoding="utf-8") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            users = []
else:
    users = []


def save_users():
    """Save the users list to the JSON file."""
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def register_user(name: str, email: str, course: str) -> str:
    """Register a new user if email is not already used."""
    # Check if user already exists
    for user in users:
        if user["student_id"].lower() == email.lower():
            return "User already exists."

    # Create new user
    new_user = {
        "student_id": email,
        "name": name,
        "course": course,
        "registered_on": datetime.now().isoformat(),
        "history": []
    }
    users.append(new_user)
    save_users()
    return "User registered successfully."


def get_user(email: str):
    """Retrieve a user by email."""
    for user in users:
        if user["student_id"].lower() == email.lower():
            return user
    return None


def list_users():
    """Return a list of all registered users."""
    return users
