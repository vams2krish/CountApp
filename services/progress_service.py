"""Progress service for MathBlitz"""
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime

from database import progress_db
from config.settings import DIFFICULTY_SETTINGS


class ProgressService:
    """Handles progress tracking logic"""
    
    def __init__(self):
        self.progress_db = progress_db
        self.difficulty_settings = DIFFICULTY_SETTINGS
    
    def save_exercise_result(
        self,
        username: str,
        exercise: str,
        difficulty: str,
        user_answer: Any,
        correct_answer: Any,
        is_correct: bool,
        time_taken: float,
        points_earned: int
    ) -> None:
        """Save an exercise result"""
        entry = {
            "Timestamp": datetime.now().isoformat(),
            "Mode": exercise,
            "Exercise": exercise,
            "Difficulty": difficulty,
            "UserAnswer": str(user_answer),
            "CorrectAnswer": str(correct_answer),
            "Status": "Correct" if is_correct else ("Incorrect" if user_answer != 0 else "Timeout"),
            "TimeTaken": round(time_taken, 2),
            "Points": points_earned
        }
        self.progress_db.save_progress(username, entry)
    
    def process_answer(
        self,
        username: str,
        task: Dict[str, Any],
        difficulty: str,
        user_answer: Any,
        time_taken: float
    ) -> Dict[str, Any]:
        """
        Process an answer and save progress
        
        Returns:
            Dictionary with result details
        """
        correct_answer = task["correct_answer"]
        is_correct = user_answer == correct_answer
        
        if is_correct:
            points = self._calculate_points(difficulty, time_taken)
        else:
            points = 0
        
        # Save progress
        self.save_exercise_result(
            username=username,
            exercise=task["exercise"],
            difficulty=difficulty,
            user_answer=user_answer,
            correct_answer=correct_answer,
            is_correct=is_correct,
            time_taken=time_taken,
            points_earned=points
        )
        
        return {
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "points_earned": points,
            "user_answer": user_answer
        }
    
    def _calculate_points(self, difficulty: str, time_taken: float) -> int:
        """Calculate points for a correct answer"""
        base = 10 * self.difficulty_settings.get(difficulty, {}).get("points_multiplier", 1)
        time_limit = self.difficulty_settings.get(difficulty, {}).get("time_limit", 45)
        bonus = max(0, int((time_limit - time_taken) / 5))
        return base + bonus
    
    def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        progress = self.progress_db.load_progress(username)
        
        if progress.empty:
            return {
                "total_exercises": 0,
                "total_score": 0,
                "accuracy": 0.0,
                "average_time": 0.0,
                "current_streak": 0
            }
        
        total = len(progress)
        correct = len(progress[progress["Status"] == "Correct"])
        accuracy = (correct / total * 100) if total > 0 else 0
        
        return {
            "total_exercises": total,
            "total_score": int(progress["Points"].sum()),
            "accuracy": round(accuracy, 1),
            "average_time": round(progress["TimeTaken"].mean(), 1),
            "current_streak": self.progress_db.get_current_streak(username)
        }
    
    def get_exercise_stats(self, username: str) -> Dict[str, Dict[str, Any]]:
        """Get statistics by exercise"""
        return self.progress_db.get_exercise_stats(username)
    
    def get_difficulty_stats(self, username: str) -> Dict[str, Dict[str, Any]]:
        """Get statistics by difficulty"""
        return self.progress_db.get_difficulty_stats(username)
    
    def get_recent_activity(self, username: str, count: int = 10) -> pd.DataFrame:
        """Get recent activity"""
        return self.progress_db.get_recent_activity(username, count)
    
    def get_progress_trend(self, username: str) -> pd.Series:
        """Get progress trend"""
        return self.progress_db.get_progress_trend(username)
    
    def get_time_trend(self, username: str) -> pd.Series:
        """Get time trend"""
        return self.progress_db.get_time_trend(username)
    
    def reset_progress(self, username: str) -> bool:
        """Reset user progress"""
        return self.progress_db.reset_progress(username)
    
    def export_progress(self, username: str) -> bytes:
        """Export progress to CSV"""
        return self.progress_db.export_to_csv(username)


# Create singleton instance
progress_service = ProgressService()

