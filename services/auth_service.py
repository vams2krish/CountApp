"""Authentication service for MathBlitz"""
from typing import Optional, Dict, Any, Tuple

from database import user_db


class AuthService:
    """Handles authentication logic"""
    
    def __init__(self):
        self.user_db = user_db
    
    def register(self, username: str, password: str, confirm_password: str) -> Tuple[bool, str]:
        """
        Register a new user
        
        Args:
            username: The username
            password: The password
            confirm_password: Password confirmation
            
        Returns:
            Tuple of (success, message)
        """
        # Validate passwords match
        if password != confirm_password:
            return False, "Passwords don't match"
        
        # Validate password length
        if len(password) < 4:
            return False, "Password too short (minimum 4 characters)"
        
        # Validate username length
        if len(username) < 3:
            return False, "Username too short (minimum 3 characters)"
        
        # Create user
        return self.user_db.create_user(username, password)
    
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Login a user
        
        Args:
            username: The username
            password: The password
            
        Returns:
            Tuple of (success, message)
        """
        if not username or not password:
            return False, "Please enter username and password"
        
        if self.user_db.verify_user(username, password):
            return True, "Login successful"
        
        return False, "Invalid credentials"
    
    def logout(self) -> None:
        """Logout the current user (handled by session state)"""
        pass
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user data"""
        return self.user_db.get_user(username)
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        return self.user_db.user_exists(username)
    
    def delete_account(self, username: str) -> Tuple[bool, str]:
        """
        Delete a user account
        
        Args:
            username: The username to delete
            
        Returns:
            Tuple of (success, message)
        """
        if self.user_db.delete_user(username):
            return True, "Account deleted successfully"
        
        return False, "User not found"
    
    def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change user password
        
        Args:
            username: The username
            old_password: Current password
            new_password: New password
            
        Returns:
            Tuple of (success, message)
        """
        # Verify old password
        if not self.user_db.verify_user(username, old_password):
            return False, "Current password is incorrect"
        
        # Validate new password
        if len(new_password) < 4:
            return False, "New password too short (minimum 4 characters)"
        
        # Update password
        if self.user_db.update_user_password(username, new_password):
            return True, "Password changed successfully"
        
        return False, "Failed to change password"


# Create singleton instance
auth_service = AuthService()

