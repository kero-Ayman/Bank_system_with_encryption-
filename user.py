# user.py
import hashlib
import os

class User:
    """
      - username (str)
      - password (stored hashed)
      - balance (float)
      - permissions (list of usernames allowed to view this user's balance)
      - added salt (str) for common passwords 
    """

    def __init__(self, username: str, plaintext: str, balance: float = 0.0, permissions=None):
        self.username = username
        """add the salting process must add here bc we use it in paswword encoding"""
        self.salt = os.urandom(16).hex()  # generate a random salt using os.urandom
        self.password = self.encode_password(plaintext)
        self.balance = float(balance)
        self.permissions = list(permissions) if permissions is not None else []


    def encode_password(self, plain: str) -> str:

        return hashlib.sha256((self.salt + plain).encode()).hexdigest()


    def check_password(self, plain: str) -> bool:
        """Compare a plaintext password to the stored hashed password."""
        test_input = self.encode_password(plain)
        return test_input == self.password

    def convert_to_dict(self) -> dict:
        """convert the user object to dict for JSON storage."""
        return {
            "username": self.username,
            "password": self.password,
            "balance": self.balance,
            "permissions": self.permissions,
            "salt": self.salt 
        }

    @classmethod
    def from_dict(cls, dic: dict):
        """Create User instance from dict (expects password already hashed)."""
        obj = cls.__new__(cls)
        obj.username = dic.get("username")
        obj.password = dic.get("password")
        obj.balance = float(dic.get("balance", 0.0))
        obj.permissions = list(dic.get("permissions", []))
        obj.salt = dic.get("salt")
        return obj


    def grant_permission(self, grantee_username: str):
        if grantee_username not in self.permissions:
            self.permissions.append(grantee_username)

    def remove_permission(self, grantee_username: str):
        if grantee_username in self.permissions:
            self.permissions.remove(grantee_username)
