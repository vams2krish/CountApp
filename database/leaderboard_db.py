"""Leaderboard database operations for MathBlitz"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from config.settings import LEADERBOARD_FILE


class LeaderboardDatabase:
    """Handles all leaderboard-related database operations"""
    
    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or LEADERBOARD_FILE
    
    def _load_leaderboard(self) -> List[Dict[str, Any]]:
        """Load leaderboard from JSON file"""
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return []
    
    def _save_leaderboard(self, leaderboard: List[Dict[str, Any]]) -> None:
        """Save leaderboard to JSON file"""
        with open(self.file_path, 'w') as f:
            json.dump(leaderboard, f, indent=2)
    
    def get_leaderboard(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get the full leaderboard"""
        leaderboard = self._load_leaderboard()
        return sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:limit]
    
    def get_top(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get top N players"""
        return self.get_leaderboard(count)
    
    def get_user_rank(self, username: str) -> Optional[int]:
        """Get a user's rank (1-based)"""
        leaderboard = self.get_leaderboard()
        for i, entry in enumerate(leaderboard):
            if entry['username'] == username:
                return i + 1
        return None
    
    def get_user_entry(self, username: str) -> Optional[Dict[str, Any]]:
        """Get a specific user's leaderboard entry"""
        leaderboard = self._load_leaderboard()
        for entry in leaderboard:
            if entry['username'] == username:
                return entry
        return None
    
    def update_score(self, username: str, score: int) -> List[Dict[str, Any]]:
        """Update a user's score, adding if they don't exist"""
        leaderboard = self._load_leaderboard()
        
        # Find existing entry
        for entry in leaderboard:
            if entry['username'] == username:
                # Only update if new score is higher
                if score > entry['score']:
                    entry['score'] = score
                entry['last_update'] = datetime.now().isoformat()
                break
        else:
            # New entry
            leaderboard.append({
                'username': username,
                'score': score,
                'last_update': datetime.now().isoformat()
            })
        
        # Sort and limit
        leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:100]
        self._save_leaderboard(leaderboard)
        return leaderboard
    
    def remove_user(self, username: str) -> bool:
        """Remove a user from the leaderboard"""
        leaderboard = self._load_leaderboard()
        original_length = len(leaderboard)
        leaderboard = [entry for entry in leaderboard if entry['username'] != username]
        
        if len(leaderboard) < original_length:
            self._save_leaderboard(leaderboard)
            return True
        return False
    
    def clear_leaderboard(self) -> None:
        """Clear all leaderboard entries"""
        self._save_leaderboard([])
    
    def get_total_players(self) -> int:
        """Get total number of players on leaderboard"""
        return len(self._load_leaderboard())

