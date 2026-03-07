"""
Lap System - Lap Counting and Timing

This module implements the complete lap counting system with checkpoint tracking,
lap time calculation, and best lap recording.
"""

import time
from typing import Dict, List, Optional, Tuple


class Checkpoint:
    """
    Represents a single checkpoint on the track.
    
    Attributes:
        id: Unique identifier for the checkpoint
        position: (x, y) coordinates
        visited: Whether this checkpoint has been visited in current lap
        visit_time: Timestamp when checkpoint was last visited
    """
    
    def __init__(self, checkpoint_id: int, position: Tuple[float, float]):
        """Initialize checkpoint."""
        self.id = checkpoint_id
        self.position = position
        self.visited = False
        self.visit_time: Optional[float] = None


class LapTimer:
    """
    Manages lap timing and checkpoint tracking.
    
    Features:
    - Checkpoint-based lap counting
    - Precise lap time measurement
    - Best lap time tracking
    - Lap completion detection
    
    Uses high-precision timestamps for accurate timing.
    """
    
    def __init__(self):
        """Initialize the lap timer."""
        self.checkpoints: List[Checkpoint] = []
        self.current_lap_start_time: Optional[float] = None
        self.current_lap_time: float = 0.0
        self.lap_number = 0
        
        # Best lap times (per lap number)
        self.best_lap_times: Dict[int, float] = {}
        
        # Lap completion state
        self.is_lap_complete = False
        self.last_checkpoint_index = -1
        
        # Timing precision in milliseconds
        self.precision = 3
    
    def initialize_track(self, checkpoint_data: List[Dict]) -> None:
        """
        Initialize checkpoints for a new track.
        
        Args:
            checkpoint_data: List of dicts with 'id' and 'position' keys
        """
        self.checkpoints = []
        for cp in checkpoint_data:
            checkpoint = Checkpoint(
                checkpoint_id=cp['id'],
                position=tuple(cp['position'])
            )
            self.checkpoints.append(checkpoint)
        
        # Reset lap state
        self.reset_lap()
    
    def reset_lap(self) -> None:
        """Reset to start of new lap."""
        self.lap_number += 1
        
        # Mark all checkpoints as unvisited
        for cp in self.checkpoints:
            cp.visited = False
            cp.visit_time = None
        
        # Record lap start time
        self.current_lap_start_time = time.perf_counter()
        self.current_lap_time = 0.0
        self.is_lap_complete = False
        self.last_checkpoint_index = -1
    
    def check_checkpoint_crossing(
        self,
        player_position: Tuple[float, float],
        checkpoint_radius: float = 15.0
    ) -> Optional[int]:
        """
        Check if player has crossed any checkpoint.
        
        Args:
            player_position: Current (x, y) position of player
            checkpoint_radius: Radius for collision detection
            
        Returns:
            Index of checkpoint crossed, or None if no checkpoint crossed
        """
        # Check each checkpoint
        for i, checkpoint in enumerate(self.checkpoints):
            # Calculate distance from player to checkpoint
            dx = player_position[0] - checkpoint.position[0]
            dy = player_position[1] - checkpoint.position[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            # Check if within checkpoint radius
            if distance <= checkpoint_radius:
                # Record visit time
                checkpoint.visit_time = time.perf_counter()
                
                # Update lap time
                if self.current_lap_start_time is not None:
                    elapsed = (checkpoint.visit_time or time.perf_counter()) - self.current_lap_start_time
                    self.current_lap_time = elapsed
                
                # Mark as visited
                checkpoint.visited = True
                
                # Check if all checkpoints visited (lap complete)
                if self._all_checkpoints_visited():
                    self.is_lap_complete = True
                
                return i
        
        return None
    
    def _all_checkpoints_visited(self) -> bool:
        """Check if all checkpoints have been visited in current lap."""
        return all(cp.visited for cp in self.checkpoints)
    
    def get_current_lap_time(self) -> float:
        """
        Get current lap time in seconds.
        
        Returns:
            Current lap time in seconds
        """
        if self.current_lap_start_time is None:
            return 0.0
        
        current_time = time.perf_counter()
        elapsed = current_time - self.current_lap_start_time
        
        # Add remaining time to complete lap (if not complete)
        if not self.is_lap_complete and self.checkpoints:
            last_checkpoint = self.checkpoints[-1]
            if last_checkpoint.visit_time:
                remaining = (current_time - last_checkpoint.visit_time)
                elapsed += remaining
        
        return elapsed
    
    def get_current_lap_time_ms(self) -> float:
        """
        Get current lap time in milliseconds.
        
        Returns:
            Current lap time in milliseconds
        """
        return self.get_current_lap_time() * 1000
    
    def get_best_lap_time(self, lap_number: Optional[int] = None) -> Optional[float]:
        """
        Get best lap time for specified lap number.
        
        Args:
            lap_number: Specific lap number, or None for current lap
            
        Returns:
            Best lap time in seconds, or None if not available
        """
        if lap_number is None:
            return self.current_lap_time
        
        return self.best_lap_times.get(lap_number)
    
    def record_completed_lap(self, lap_time: float) -> None:
        """
        Record a completed lap time.
        
        Args:
            lap_time: Time taken to complete the lap in seconds
        """
        # Update best lap time for this lap number
        if self.lap_number not in self.best_lap_times:
            self.best_lap_times[self.lap_number] = lap_time
        else:
            self.best_lap_times[self.lap_number] = min(
                self.best_lap_times[self.lap_number],
                lap_time
            )
    
    def get_lap_display_string(self, include_best: bool = True) -> str:
        """
        Format lap time for display in HUD.
        
        Args:
            include_best: Whether to include best lap time
            
        Returns:
            Formatted string for display
        """
        current_time_ms = self.get_current_lap_time_ms()
        
        # Format as minutes.seconds (e.g., "01:23.456")
        minutes = int(current_time_ms // 60000)
        seconds = (current_time_ms % 60000) / 1000
        
        time_str = f"{minutes}:{seconds:.{self.precision}f}"
        
        if include_best and self.lap_number in self.best_lap_times:
            best_time_ms = self.best_lap_times[self.lap_number] * 1000
            best_minutes = int(best_time_ms // 60000)
            best_seconds = (best_time_ms % 60000) / 1000
            best_str = f"{best_minutes}:{best_seconds:.{self.precision}f}"
            
            return f"{time_str} (Best: {best_str})"
        
        return time_str
    
    def reset(self) -> None:
        """Reset all lap data."""
        self.checkpoints = []
        self.current_lap_start_time = None
        self.current_lap_time = 0.0
        self.lap_number = 0
        self.best_lap_times = {}
        self.is_lap_complete = False


class LapSystem:
    """
    Main lap system that coordinates all lap-related functionality.
    
    This is the central manager for:
    - Starting and resetting laps
    - Tracking checkpoint progress
    - Recording lap times
    - Managing best lap records
    """
    
    def __init__(self):
        """Initialize the lap system."""
        self.lap_timer = LapTimer()
        self.checkpoint_radius = 15.0
    
    def start_lap(self) -> None:
        """Start a new lap."""
        self.lap_timer.reset_lap()
    
    def update(
        self,
        player_position: Tuple[float, float],
        delta_time: float
    ) -> bool:
        """
        Update lap state for one frame.
        
        Args:
            player_position: Current player position
            delta_time: Time in seconds since last frame
            
        Returns:
            True if lap is complete, False otherwise
        """
        # Check for checkpoint crossing
        crossed_checkpoint = self.lap_timer.check_checkpoint_crossing(
            player_position,
            self.checkpoint_radius
        )
        
        return self.lap_timer.is_lap_complete
    
    def get_lap_info(self) -> Dict:
        """
        Get current lap information.
        
        Returns:
            Dictionary with lap statistics
        """
        return {
            'lap_number': self.lap_timer.lap_number,
            'current_time': self.lap_timer.get_current_lap_time(),
            'current_time_ms': self.lap_timer.get_current_lap_time_ms(),
            'is_complete': self.lap_timer.is_lap_complete,
            'best_time': self.lap_timer.get_best_lap_time(),
            'checkpoints_visited': sum(1 for cp in self.lap_timer.checkpoints if cp.visited),
            'total_checkpoints': len(self.lap_timer.checkpoints),
        }


def create_lap_system(checkpoint_radius: float = 15.0) -> LapSystem:
    """
    Factory function to create a configured lap system.
    
    Args:
        checkpoint_radius: Radius for checkpoint collision detection
        
    Returns:
        Configured LapSystem instance
    """
    return LapSystem()
