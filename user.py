# user.py
import base64

class User:
    """
    User object:
      - username (str)
      - password (stored encypted ))
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
        """Encode password using base64 (easy reversible encoding per spec)."""
        if isinstance(plain, str):
            plain = plain.encode('utf-8')
        return base64.b64encode(plain).decode('utf-8')

    @staticmethod
    def decode_password(ceyhier: str) -> str:
        """Decode base64 password back to plain text."""
        return base64.b64decode(ceyhier.encode('utf-8')).decode('utf-8')


    def check_password(self, plain: str) -> bool:
        """Compare a plaintext password to the stored (encoded) password."""
        return self.encode_password(plain) == self.password

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
        """Create User instance from dict (expects password already encoded)."""
        obj = cls.__new__(cls)
        obj.username = d.get("username")
        obj.password = d.get("password")  # already encoded
        obj.balance = float(d.get("balance", 0.0))
        obj.permissions = list(d.get("permissions", []))
        return obj

    # Convenience helpers
    def grant_permission(self, grantee_username: str):
        if grantee_username not in self.permissions:
            self.permissions.append(grantee_username)

    def revoke_permission(self, grantee_username: str):
        if grantee_username in self.permissions:
            self.permissions.remove(grantee_username)
