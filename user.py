# user.py
import hashlib

class User:
    """
    User object:
      - username (str)
      - password (stored hashed)
      - balance (float)
      - permissions (list of usernames allowed to view this user's balance)
    """

    def __init__(self, username: str, plaintext: str, balance: float = 0.0, permissions=None):
        self.username = username
        self.password = self.encode_password(plaintext)
        self.balance = float(balance)
        self.permissions = list(permissions) if permissions is not None else []

    @staticmethod
    def encode_password(plain: str) -> str:
        """Hash password using SHA-256 (one-way)."""
        plain = plain.encode("utf-8")
        return hashlib.sha256(plain).hexdigest()


    def check_password(self, plain: str) -> bool:
        """Compare a plaintext password to the stored hashed password."""
        hashed_input = hashlib.sha256(plain.encode()).hexdigest()
        return hashed_input == self.password

    def to_dict(self) -> dict:
        """Serialize to dict for JSON storage."""
        return {
            "username": self.username,
            "password": self.password,
            "balance": self.balance,
            "permissions": self.permissions
        }

    @classmethod
    def from_dict(cls, d: dict):
        """Create User instance from dict (expects password already hashed)."""
        obj = cls.__new__(cls)
        obj.username = d.get("username")
        obj.password = d.get("password")
        obj.balance = float(d.get("balance", 0.0))
        obj.permissions = list(d.get("permissions", []))
        return obj


    def grant_permission(self, grantee_username: str):
        if grantee_username not in self.permissions:
            self.permissions.append(grantee_username)

    def remove_permission(self, grantee_username: str):
        if grantee_username in self.permissions:
            self.permissions.remove(grantee_username)
