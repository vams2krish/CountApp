"""Database module for MathBlitz - handles all data persistence"""
from .user_db import UserDatabase
from .leaderboard_db import LeaderboardDatabase
from .progress_db import ProgressDatabase

# Create singleton instances
user_db = UserDatabase()
leaderboard_db = LeaderboardDatabase()
progress_db = ProgressDatabase()

__all__ = ["UserDatabase", "LeaderboardDatabase", "ProgressDatabase", "user_db", "leaderboard_db", "progress_db"]

