# storage.py
import json
import os
from typing import Dict
from user import User

USERS_FILE = "users.json"
ADMIN_USERNAME="not_set"
ADMIN_BALANCE = 0.0

def load_users() -> Dict[str, User]:
    """Load users from USERS_FILE. Return dict username->User."""
    if not os.path.exists(USERS_FILE):
        # create default admin
        ADMIN_USERNAME= input("Enter the admin username: ").strip()
        ADMIN_PASSWORD= input("Enter the admin password: ").strip()
        admin = User(ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_BALANCE, permissions=[])
        data = {ADMIN_USERNAME: admin.to_dict()}
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return {ADMIN_USERNAME: admin}

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        '''read the file content'''
        raw = json.load(f)


    users = {}
    for uname, udata in raw.items():
        users[uname] = User.from_dict(udata)
  


    return users

def save_users(users: Dict[str, User]):
    """Save the users dict (username->User) to USERS_FILE."""
    serial = {}  # create an empty dictionary first
    for uname, user in users.items():
        # convert each User object to a dictionary
        serial[uname] = user.to_dict()  

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

        # load existing JSON
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    # update only this user
    raw[username] = users[username].to_dict()
    # save back
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(raw, f, indent=4)
