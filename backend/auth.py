"""
User Authentication and Session Management Service for EduGenie.
Provides secure password hashing, user registration, login verification,
and persistent local user accounts.
"""

import json
import os
import hashlib
from typing import Dict, Optional, Tuple

USER_DB_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def _hash_password(password: str) -> str:
    """Returns SHA-256 hash of password with a static salt."""
    salt = "edugenie_study_salt_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


def _load_users() -> Dict[str, Dict[str, str]]:
    """Loads user records from JSON storage file."""
    if not os.path.exists(USER_DB_FILE):
        # Create default demo user
        default_users = {
            "student@edugenie.ai": {
                "name": "Demo Scholar",
                "password_hash": _hash_password("edugenie123"),
                "joined": "2026-09-01"
            }
        }
        with open(USER_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(default_users, f, indent=2)
        return default_users

    try:
        with open(USER_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_users(users: Dict[str, Dict[str, str]]) -> bool:
    """Saves user records to JSON storage file."""
    try:
        with open(USER_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)
        return True
    except Exception:
        return False


def register_user(email: str, name: str, password: str) -> Tuple[bool, str]:
    """Registers a new user account."""
    email = email.strip().lower()
    name = name.strip()
    
    if not email or "@" not in email:
        return False, "Please enter a valid email address."
    if not name:
        return False, "Please enter your full name."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    users = _load_users()
    if email in users:
        return False, "An account with this email already exists. Please login."

    users[email] = {
        "name": name,
        "password_hash": _hash_password(password),
        "joined": "2026-09-27"
    }
    
    if _save_users(users):
        return True, f"Account created successfully for {name}!"
    return False, "Failed to save user account. Please try again."


def authenticate_user(email: str, password: str) -> Tuple[bool, Optional[Dict[str, str]], str]:
    """Authenticates user credentials."""
    email = email.strip().lower()
    users = _load_users()
    
    if email not in users:
        return False, None, "No account found with this email. Please register first."
    
    user_record = users[email]
    if user_record.get("password_hash") == _hash_password(password):
        return True, {"email": email, "name": user_record.get("name", "Scholar")}, "Login successful!"
    
    return False, None, "Incorrect password. Please try again."
