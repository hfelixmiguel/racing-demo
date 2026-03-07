"""
Velocity Component - Movement State Management

This module manages the velocity component for game entities,
handling speed, direction, and movement calculations.
"""

import arcade
from typing import Tuple


class Velocity:
    """
    Manages entity velocity properties (speed and direction).
    
    Attributes:
        speed: Current speed magnitude (always non-negative)
        angle: Direction of movement in degrees
        x_velocity: Horizontal velocity component
        y_velocity: Vertical velocity component
        
    The velocity is used to calculate movement over time using delta time.
    """
    
    def __init__(
        self,
        speed: float = 0.0,
        angle: float = 0.0
    ):
        """Initialize velocity with given speed and direction."""
        self.speed = max(0.0, speed)  # Speed is always non-negative
        self.angle = angle
        
        # Calculate velocity components
        self._update_components()
    
    def _update_components(self) -> None:
        """Update x and y velocity components from speed and angle."""
        radians = arcade.degrees_to_radians(self.angle)
        self.x_velocity = self.speed * arcade.cos(radians)
        self.y_velocity = self.speed * arcade.sin(radians)
    
    @property
    def x_velocity(self) -> float:
        """Get horizontal velocity component."""
        return self._x_velocity
    
    @x_velocity.setter
    def x_velocity(self, value: float) -> None:
        """Set horizontal velocity and recalculate angle."""
        self._x_velocity = value
        self._recalculate_from_components()
    
    @property
    def y_velocity(self) -> float:
        """Get vertical velocity component."""
        return self._y_velocity
    
    @y_velocity.setter
    def y_velocity(self, value: float) -> None:
        """Set vertical velocity and recalculate angle."""
        self._y_velocity = value
        self._recalculate_from_components()
    
    def _recalculate_from_components(self) -> None:
        """Recalculate speed and angle from velocity components."""
        # Calculate magnitude (speed)
        self.speed = (self._x_velocity ** 2 + self._y_velocity ** 2) ** 0.5
        
        if self.speed > 0:
            # Calculate angle from components
            radians = arcade.atan2(self._y_velocity, self._x_velocity)
            self.angle = arcade.radians_to_degrees(radians)
    
    def set_speed(self, speed: float) -> None:
        """Set speed magnitude."""
        self.speed = max(0.0, speed)
        self._update_components()
    
    def set_angle(self, angle: float) -> None:
        """Set movement direction angle."""
        self.angle = angle % 360
        self._update_components()
    
    def add_velocity(
        self,
        dx: float,
        dy: float,
        delta_time: float = 1.0
    ) -> None:
        """
        Add velocity impulse.
        
        Args:
            dx: X component of impulse
            dy: Y component of impulse
            delta_time: Time interval for the impulse
        """
        # Convert impulse to velocity (divide by time)
        vx = dx / delta_time
        vy = dy / delta_time
        
        # Add to current velocity components
        self.x_velocity += vx
        self.y_velocity += vy
        
        # Recalculate speed and angle
        self._recalculate_from_components()
    
    def accelerate(
        self,
        acceleration: float,
        direction_angle: float,
        delta_time: float = 1.0
    ) -> None:
        """
        Apply acceleration in a specific direction.
        
        Args:
            acceleration: Acceleration magnitude
            direction_angle: Direction of acceleration in degrees
            delta_time: Time interval
        """
        # Calculate velocity change from acceleration
        dv_x = acceleration * arcade.cos(arcade.degrees_to_radians(direction_angle)) * delta_time
        dv_y = acceleration * arcade.sin(arcade.degrees_to_radians(direction_angle)) * delta_time
        
        self.x_velocity += dv_x
        self.y_velocity += dv_y
        self._recalculate_from_components()
    
    def apply_friction(self, friction: float) -> None:
        """
        Apply friction to reduce velocity.
        
        Args:
            friction: Friction coefficient (0.0-1.0)
        """
        if friction >= 1.0:
            return
        
        # Reduce velocity magnitude while maintaining direction
        self.speed *= friction
        self._update_components()
    
    def stop(self) -> None:
        """Stop the entity completely."""
        self.speed = 0.0
        self.x_velocity = 0.0
        self.y_velocity = 0.0
    
    def is_moving(self, threshold: float = 0.1) -> bool:
        """
        Check if entity is moving above threshold.
        
        Args:
            threshold: Minimum speed to be considered moving
            
        Returns:
            True if moving, False otherwise
        """
        return self.speed > threshold
    
    def get_speed_kmh(self, factor: float = 0.36) -> float:
        """
        Get speed in km/h (assuming pixels/sec to km/h conversion).
        
        Args:
            factor: Conversion factor (default: 0.36 for px/s to km/h)
            
        Returns:
            Speed in km/h
        """
        return self.speed * factor
    
    def get_speed_pixels_per_sec(self) -> float:
        """Get speed in pixels per second."""
        return self.speed
    
    def reset(self) -> None:
        """Reset velocity to zero."""
        self.stop()


class VelocityManager:
    """
    Manages velocity for multiple entities.
    
    Features:
    - Batch velocity updates
    - Velocity interpolation
    - Velocity clamping
    """
    
    def __init__(self):
        """Initialize the velocity manager."""
        self.velocities: dict = {}  # entity_id -> Velocity
    
    def register_velocity(self, entity_id: str, velocity: Velocity) -> None:
        """Register a velocity for an entity."""
        self.velocities[entity_id] = velocity
    
    def get_velocity(self, entity_id: str) -> Optional[Velocity]:
        """Get velocity for an entity."""
        return self.velocities.get(entity_id)
    
    def apply_friction_to_all(self, friction: float) -> None:
        """Apply friction to all registered velocities."""
        for velocity in self.velocities.values():
            velocity.apply_friction(friction)
    
    def clamp_speeds(
        self,
        max_speed: float,
        min_speed: float = 0.0
    ) -> None:
        """Clamp all speeds to range."""
        for velocity in self.velocities.values():
            if velocity.speed > max_speed:
                velocity.speed = max_speed
            elif velocity.speed < min_speed:
                velocity.speed = min_speed


def create_velocity(speed: float = 0.0, angle: float = 0.0) -> Velocity:
    """
    Factory function to create a velocity.
    
    Args:
        speed: Initial speed
        angle: Initial direction angle
        
    Returns:
        Configured Velocity instance
    """
    return Velocity(speed=speed, angle=angle)
