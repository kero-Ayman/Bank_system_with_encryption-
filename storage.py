# storage.py
import json
import os
from typing import Dict
from user import User

USERS_FILE = "users.json"
ADMIN_USERNAME = "kerolos"
ADMIN_PASSWORD = "0000"   # base64 will be used when creating user
ADMIN_BALANCE = 0.0

def load_users() -> Dict[str, User]:
    """Load users from USERS_FILE. Return dict username->User."""
    if not os.path.exists(USERS_FILE):
        # create default admin
        admin = User(ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_BALANCE, permissions=[])
        data = {ADMIN_USERNAME: admin.to_dict()}
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return {ADMIN_USERNAME: admin}

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError:
            # If corrupted, re-create admin
            admin = User(ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_BALANCE, permissions=[])
            data = {ADMIN_USERNAME: admin.to_dict()}
            with open(USERS_FILE, "w", encoding="utf-8") as f2:
                json.dump(data, f2, indent=4)
            return {ADMIN_USERNAME: admin}

    users = {}
    for uname, udata in raw.items():
        users[uname] = User.from_dict(udata)
    # Ensure admin exists
    if ADMIN_USERNAME not in users:
        admin = User(ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_BALANCE, permissions=[])
        users[ADMIN_USERNAME] = admin
        save_users(users)
    return users

def save_users(users: Dict[str, User]):
    """Save the users dict (username->User) to USERS_FILE."""
    serial = {uname: user.to_dict() for uname, user in users.items()}
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(serial, f, indent=4)

def user_exists(users: Dict[str, User], username: str) -> bool:
    return username in users

def add_user(users: Dict[str, User], username: str, password_plain: str, balance: float = 0.0) -> bool:
    """Add a new user. Return True if added, False if username exists."""
    if user_exists(users, username):
        return False
    users[username] = User(username, password_plain, balance, permissions=[])
    save_users(users)
    return True

def get_user(users: Dict[str, User], username: str) -> User:
    return users.get(username)

def update_user(users: Dict[str, User], username: str):
    """Persist a single user's current state to file (save all)."""
    save_users(users)
