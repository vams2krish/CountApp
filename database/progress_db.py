"""Progress database operations for MathBlitz"""
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from config.settings import DATA_DIR


class ProgressDatabase:
    """Handles all progress-related database operations"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or DATA_DIR
        self.progress_dir = self.data_dir / "progress"
        self.progress_dir.mkdir(exist_ok=True)
    
    def _get_progress_file(self, username: str) -> Path:
        """Get the progress file path for a user"""
        return self.progress_dir / f"{username}.csv"
    
    def load_progress(self, username: str) -> pd.DataFrame:
        """Load user progress data"""
        pf = self._get_progress_file(username)
        if pf.exists():
            return pd.read_csv(pf)
        return self._empty_progress_df()
    
    def _empty_progress_df(self) -> pd.DataFrame:
        """Create an empty progress DataFrame"""
        return pd.DataFrame(columns=[
            "Timestamp", "Mode", "Exercise", "Difficulty", 
            "UserAnswer", "CorrectAnswer", "Status", "TimeTaken", "Points"
        ])
    
    def save_progress(self, username: str, entry: Dict[str, Any]) -> None:
        """Save a single progress entry"""
        pf = self._get_progress_file(username)
        df = self.load_progress(username)
        new_df = pd.DataFrame([entry])
        
        if df.empty:
            new_df.to_csv(pf, index=False)
        else:
            combined = pd.concat([df, new_df], ignore_index=True)
            combined.to_csv(pf, index=False)
    
    def get_total_exercises(self, username: str) -> int:
        """Get total number of exercises completed"""
        progress = self.load_progress(username)
        return len(progress)
    
    def get_total_score(self, username: str) -> int:
        """Get total score"""
        progress = self.load_progress(username)
        return int(progress["Points"].sum()) if not progress.empty else 0
    
    def get_accuracy(self, username: str) -> float:
        """Get accuracy percentage"""
        progress = self.load_progress(username)
        if progress.empty:
            return 0.0
        correct = len(progress[progress["Status"] == "Correct"])
        return (correct / len(progress)) * 100
    
    def get_current_streak(self, username: str) -> int:
        """Get current streak (correct answers in last 10)"""
        progress = self.load_progress(username)
        if progress.empty:
            return 0
        # Get last 10 answers
        last_10 = progress.tail(10)
        correct_count = len(last_10[last_10["Status"] == "Correct"])
        return correct_count
    
    def get_average_time(self, username: str) -> float:
        """Get average time per exercise"""
        progress = self.load_progress(username)
        if progress.empty:
            return 0.0
        return progress["TimeTaken"].mean()
    
    def get_exercise_stats(self, username: str) -> Dict[str, Dict[str, Any]]:
        """Get statistics grouped by exercise"""
        progress = self.load_progress(username)
        if progress.empty:
            return {}
        
        stats = {}
        for exercise in progress["Exercise"].unique():
            ex_data = progress[progress["Exercise"] == exercise]
            stats[exercise] = {
                "total": len(ex_data),
                "correct": len(ex_data[ex_data["Status"] == "Correct"]),
                "accuracy": (len(ex_data[ex_data["Status"] == "Correct"]) / len(ex_data)) * 100,
                "points": int(ex_data["Points"].sum()),
                "avg_time": ex_data["TimeTaken"].mean()
            }
        return stats
    
    def get_difficulty_stats(self, username: str) -> Dict[str, Dict[str, Any]]:
        """Get statistics grouped by difficulty"""
        progress = self.load_progress(username)
        if progress.empty:
            return {}
        
        stats = {}
        for difficulty in progress["Difficulty"].unique():
            diff_data = progress[progress["Difficulty"] == difficulty]
            stats[difficulty] = {
                "total": len(diff_data),
                "correct": len(diff_data[diff_data["Status"] == "Correct"]),
                "accuracy": (len(diff_data[diff_data["Status"] == "Correct"]) / len(diff_data)) * 100,
                "points": int(diff_data["Points"].sum())
            }
        return stats
    
    def get_recent_activity(self, username: str, count: int = 10) -> pd.DataFrame:
        """Get recent activity"""
        progress = self.load_progress(username)
        if progress.empty:
            return self._empty_progress_df()
        return progress.tail(count)
    
    def get_rolling_accuracy(self, username: str, window: int = 5) -> pd.Series:
        """Get rolling accuracy"""
        progress = self.load_progress(username)
        if progress.empty or len(progress) < window:
            return pd.Series()
        
        progress = progress.copy()
        progress["StatusNum"] = (progress["Status"] == "Correct").astype(int)
        progress["Rolling"] = progress["StatusNum"].rolling(window).mean() * 100
        return progress["Rolling"].dropna()
    
    def reset_progress(self, username: str) -> bool:
        """Reset user progress"""
        pf = self._get_progress_file(username)
        if pf.exists():
            pf.unlink()
            return True
        return False
    
    def delete_progress(self, username: str) -> bool:
        """Delete user progress file"""
        return self.reset_progress(username)
    
    def export_to_csv(self, username: str) -> bytes:
        """Export progress to CSV bytes"""
        progress = self.load_progress(username)
        return progress.to_csv(index=False).encode('utf-8')
    
    def get_progress_trend(self, username: str) -> pd.Series:
        """Get progress trend over time"""
        progress = self.load_progress(username)
        if progress.empty or len(progress) < 2:
            return pd.Series()
        
        progress = progress.copy()
        progress["StatusNum"] = (progress["Status"] == "Correct").astype(int)
        progress["Rolling"] = progress["StatusNum"].rolling(5).mean() * 100
        return progress["Rolling"].dropna()
    
    def get_time_trend(self, username: str) -> pd.Series:
        """Get time trend over time"""
        progress = self.load_progress(username)
        return progress["TimeTaken"] if not progress.empty else pd.Series()

