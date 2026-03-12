"""Leaderboard service for MathBlitz"""
from typing import List, Dict, Any, Optional

from database import leaderboard_db


class LeaderboardService:
    """Handles leaderboard logic"""
    
    def __init__(self):
        self.leaderboard_db = leaderboard_db
    
    def get_leaderboard(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get the leaderboard"""
        return self.leaderboard_db.get_leaderboard(limit)
    
    def get_top_players(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get top N players"""
        return self.leaderboard_db.get_top(count)
    
    def get_user_rank(self, username: str) -> Optional[int]:
        """Get a user's rank"""
        return self.leaderboard_db.get_user_rank(username)
    
    def get_user_entry(self, username: str) -> Optional[Dict[str, Any]]:
        """Get a user's leaderboard entry"""
        return self.leaderboard_db.get_user_entry(username)
    
    def update_score(self, username: str, score: int) -> List[Dict[str, Any]]:
        """Update a user's score"""
        return self.leaderboard_db.update_score(username, score)
    
    def remove_user(self, username: str) -> bool:
        """Remove a user from leaderboard"""
        return self.leaderboard_db.remove_user(username)
    
    def get_total_players(self) -> int:
        """Get total number of players"""
        return self.leaderboard_db.get_total_players()


# Create singleton instance
leaderboard_service = LeaderboardService()

