"""User database operations for MathBlitz"""
import json
import hashlib
import secrets
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from config.settings import USERS_FILE, DEFAULT_SETTINGS


class UserDatabase:
    """Handles all user-related database operations"""
    
    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or USERS_FILE
    
    def _load_users(self) -> Dict[str, Any]:
        """Load users from JSON file"""
        if self.file_path.exists():
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {}
    
    def _save_users(self, users: Dict[str, Any]) -> None:
        """Save users to JSON file"""
        with open(self.file_path, "w") as f:
            json.dump(users, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256 with a random salt"""
        salt = secrets.token_hex(16)
        password_with_salt = salt + password
        hashed = hashlib.sha256(password_with_salt.encode()).hexdigest()
        return f"{salt}${hashed}"
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify a password against a stored hash"""
        try:
            salt, hashed = stored_hash.split('$')
            password_with_salt = salt + password
            new_hash = hashlib.sha256(password_with_salt.encode()).hexdigest()
            return new_hash == hashed
        except:
            return False
    
    def user_exists(self, username: str) -> bool:
        """Check if a user exists"""
        users = self._load_users()
        return username in users
    
    def create_user(self, username: str, password: str) -> tuple[bool, str]:
        """Create a new user"""
        users = self._load_users()
        
        if username in users:
            return False, "Username already exists"
        
        if len(username) < 3:
            return False, "Username too short"
        
        if len(password) < 4:
            return False, "Password too short"
        
        hashed_password = self._hash_password(password)
        users[username] = {
            "password": hashed_password,
            "created_at": datetime.now().isoformat(),
            "settings": DEFAULT_SETTINGS.copy()
        }
        self._save_users(users)
        return True, "Registration successful"
    
    def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials"""
        users = self._load_users()
        
        if username not in users:
            return False
        
        # Handle legacy plain-text passwords (for backward compatibility)
        stored_password = users[username]["password"]
        if "$" not in stored_password:
            # Legacy plain-text password
            if password == stored_password:
                # Upgrade to hashed password
                users[username]["password"] = self._hash_password(password)
                self._save_users(users)
                return True
            return False
        
        return self._verify_password(password, stored_password)
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user data"""
        users = self._load_users()
        return users.get(username)
    
    def get_user_settings(self, username: str) -> Dict[str, Any]:
        """Get user settings"""
        user = self.get_user(username)
        if user and "settings" in user:
            return user["settings"]
        return DEFAULT_SETTINGS.copy()
    
    def save_user_settings(self, username: str, settings: Dict[str, Any]) -> bool:
        """Save user settings"""
        users = self._load_users()
        
        if username not in users:
            return False
        
        users[username]["settings"] = settings
        self._save_users(users)
        return True
    
    def delete_user(self, username: str) -> bool:
        """Delete a user"""
        users = self._load_users()
        
        if username not in users:
            return False
        
        del users[username]
        self._save_users(users)
        return True
    
    def get_all_users(self) -> Dict[str, Any]:
        """Get all users"""
        return self._load_users()
    
    def update_user_password(self, username: str, new_password: str) -> bool:
        """Update user password"""
        users = self._load_users()
        
        if username not in users:
            return False
        
        users[username]["password"] = self._hash_password(new_password)
        self._save_users(users)
        return True

