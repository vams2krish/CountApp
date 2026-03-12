"""Sound service for MathBlitz"""
from pathlib import Path
from typing import Optional

from config.settings import SOUNDS_DIR


class SoundService:
    """Handles sound playback logic"""
    
    def __init__(self, sounds_dir: Optional[Path] = None):
        self.sounds_dir = sounds_dir or SOUNDS_DIR
        self.pygame_initialized = False
    
    def play_sound(self, sound_name: str, enabled: bool = True) -> None:
        """
        Play a sound effect
        
        Args:
            sound_name: Name of the sound (correct, wrong, new_task)
            enabled: Whether sound is enabled
        """
        if not enabled:
            return
        
        try:
            import pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            sound_files = {
                "correct": self.sounds_dir / "correct.wav",
                "wrong": self.sounds_dir / "wrong.wav",
                "new_task": self.sounds_dir / "new_task.wav"
            }
            
            sound_file = sound_files.get(sound_name)
            if sound_file and sound_file.exists():
                pygame.mixer.music.load(str(sound_file))
                pygame.mixer.music.play()
        except Exception:
            # Silently fail if pygame is not available
            pass
    
    def play_correct(self, enabled: bool = True) -> None:
        """Play correct answer sound"""
        self.play_sound("correct", enabled)
    
    def play_wrong(self, enabled: bool = True) -> None:
        """Play wrong answer sound"""
        self.play_sound("wrong", enabled)
    
    def play_new_task(self, enabled: bool = True) -> None:
        """Play new task sound"""
        self.play_sound("new_task", enabled)


# Create singleton instance
sound_service = SoundService()

