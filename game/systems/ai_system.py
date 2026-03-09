"""
AI Opponent System for Racing Demo

This module implements an AI opponent that follows checkpoints with realistic behavior,
including speed variation and smooth steering adjustments.
"""

import math
from typing import Optional, Dict, Any


class AICar:
    """AI-controlled car that follows the track checkpoints."""
    
    def __init__(self, x: float = 0.0, y: float = 0.0, angle: float = 0.0):
        self.position = type('obj', (object,), {'x': x, 'y': y})
        self.angle = math.radians(angle)
        self.speed = 150.0  # pixels per second
        self.max_speed = 200.0
        self.min_speed = 80.0
        self.acceleration = 300.0
        self.deceleration = 400.0
        self.turn_speed = 5.0  # radians per second
        
        # AI behavior state
        self.target_checkpoint_index: Optional[int] = None
        self.current_lap = 1
        self.lap_times: list[float] = []
        
    def update(self, checkpoints: list[dict], dt: float) -> tuple[float, float]:
        """
        Update AI position based on checkpoint sequence.
        
        Args:
            checkpoints: List of checkpoint dictionaries with 'x' and 'y' keys
            dt: Delta time in seconds
            
        Returns:
            Tuple of (new_x, new_y) position
        """
        if not checkpoints or self.target_checkpoint_index is None:
            return self.position.x, self.position.y
        
        # Calculate target checkpoint index based on current lap and progress
        total_checkpoints = len(checkpoints)
        
        # Determine which checkpoint to head toward
        if self.target_checkpoint_index >= total_checkpoints:
            # Reset to first checkpoint (new lap or start)
            self.target_checkpoint_index = 0
        
        target_checkpoint = checkpoints[self.target_checkpoint_index]
        target_x = target_checkpoint['x']
        target_y = target_checkpoint['y']
        
        # Calculate angle to target
        dx = target_x - self.position.x
        dy = target_y - self.position.y
        distance_to_target = math.sqrt(dx * dx + dy * dy)
        
        if distance_to_target > 0:
            desired_angle = math.atan2(dy, dx)
            
            # Smooth steering toward target angle
            angle_diff = desired_angle - self.angle
            
            # Normalize angle difference to [-pi, pi]
            while angle_diff <= -math.pi:
                angle_diff += 2 * math.pi
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            
            # Apply turn with speed-dependent turning (faster = less turn)
            effective_turn_speed = self.turn_speed / max(1, self.speed / 100)
            self.angle += angle_diff * min(1.0, dt * effective_turn_speed)
        
        # Speed control - accelerate toward target checkpoint
        if distance_to_target > 200:
            # Far from target - maintain or increase speed
            if self.speed < self.max_speed:
                self.speed = min(self.max_speed, self.speed + self.acceleration * dt)
        else:
            # Close to target - slow down for precision
            if self.speed > self.min_speed:
                self.speed = max(self.min_speed, self.speed - self.deceleration * dt)
        
        # Add slight speed variation for realistic behavior
        speed_variation = (math.sin(len(checkpoints) * 0.1 + self.current_lap * 2) * 5)
        actual_speed = self.speed + speed_variation
        
        # Update position
        new_x = self.position.x + math.cos(self.angle) * actual_speed * dt
        new_y = self.position.y + math.sin(self.angle) * actual_speed * dt
        
        # Check if we've reached the target checkpoint (crossed the line)
        if distance_to_target < 50:
            self.target_checkpoint_index += 1
            
            # Record lap time if we completed a full lap
            if self.target_checkpoint_index >= total_checkpoints:
                self.current_lap += 1
                self.target_checkpoint_index = 0
        
        return new_x, new_y
    
    def get_speed_kmh(self) -> float:
        """Convert speed from pixels/sec to km/h (approximate)."""
        # Assuming 1 pixel = 0.5 meters for gameplay purposes
        return round(self.speed * 0.5 * 3.6, 1)


def create_ai_car(config: Optional[dict] = None) -> AICar:
    """
    Factory function to create an AI car with optional configuration.
    
    Args:
        config: Dictionary with custom settings (speed, turn_rate, etc.)
        
    Returns:
        Configured AICar instance
    """
    ai_car = AICar()
    
    if config:
        if 'max_speed' in config:
            ai_car.max_speed = config['max_speed']
        if 'min_speed' in config:
            ai_car.min_speed = config['min_speed']
        if 'turn_speed' in config:
            ai_car.turn_speed = math.radians(config['turn_speed'])
        if 'starting_angle' in config:
            ai_car.angle = math.radians(config['starting_angle'])
    
    return ai_car
