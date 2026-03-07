"""
Camera System - Follow Player Car

This module implements a smooth camera system that follows the player car,
providing a dynamic view of the gameplay while maintaining performance.
"""

import arcade
from typing import Optional, Tuple
from game.core.config import (
    CAMERA_SMOOTHING, COLLISION_SHAKE_INTENSITY,
    COLLISION_SHAKE_DURATION, SCREEN_WIDTH, SCREEN_HEIGHT
)


class CameraSystem:
    """
    Manages camera behavior for following the player car.
    
    Features:
    - Smooth follow with interpolation
    - Collision shake effect
    - Viewport bounds management
    - Performance optimization
    
    The camera uses linear interpolation (Lerp) for smooth movement,
    ensuring the view transitions naturally rather than snapping to the player.
    """
    
    def __init__(self):
        """Initialize the camera system."""
        # Camera state
        self.position: Tuple[float, float] = (0, 0)
        self.target_position: Tuple[float, float] = (0, 0)
        
        # Viewport bounds
        self.viewport_left = 0
        self.viewport_right = SCREEN_WIDTH
        self.viewport_top = 0
        self.viewport_bottom = SCREEN_HEIGHT
        
        # Shake effect state
        self.shake_intensity = 0.0
        self.shake_duration = COLLISION_SHAKE_DURATION
        self.shake_timer = 0.0
        
        # Smoothing factor (higher = faster response)
        self.smoothing = CAMERA_SMOOTHING
    
    def follow_player(
        self,
        player_x: float,
        player_y: float,
        delta_time: float
    ) -> None:
        """
        Update camera to follow the player with smooth interpolation.
        
        Args:
            player_x: Player's X position
            player_y: Player's Y position
            delta_time: Time in seconds since last frame
        """
        # Set target position (center on player)
        self.target_position = (player_x, player_y)
        
        # Apply linear interpolation for smooth movement
        # Formula: current = current + (target - current) * smoothing * dt
        dx = (self.target_position[0] - self.position[0]) * self.smoothing * delta_time
        dy = (self.target_position[1] - self.position[1]) * self.smoothing * delta_time
        
        self.position = (
            self.position[0] + dx,
            self.position[1] + dy
        )
    
    def apply_collision_shake(self) -> None:
        """Apply screen shake effect from collision."""
        if self.shake_intensity > 0:
            # Decrease intensity over time
            self.shake_intensity -= (COLLISION_SHAKE_INTENSITY * 10) * 0.016  # ~60 FPS
            
            # Reset timer
            self.shake_timer = COLLISION_SHAKE_DURATION
        else:
            self.shake_intensity = 0
    
    def update_shake(self, delta_time: float) -> None:
        """Update shake timer."""
        if self.shake_timer > 0:
            self.shake_timer -= delta_time
            
            # Reset when duration expires
            if self.shake_timer <= 0:
                self.shake_intensity = 0
    
    def get_shake_offset(self) -> Tuple[float, float]:
        """
        Get current shake offset for applying to camera position.
        
        Returns:
            (shake_x, shake_y) tuple to add to camera position
        """
        if self.shake_intensity <= 0:
            return (0, 0)
        
        # Generate random offset based on intensity
        import random
        shake_x = (random.random() - 0.5) * self.shake_intensity
        shake_y = (random.random() - 0.5) * self.shake_intensity
        
        return (shake_x, shake_y)
    
    def set_viewport_bounds(
        self,
        left: float,
        right: float,
        top: float,
        bottom: float
    ) -> None:
        """
        Set the viewport bounds to restrict camera view.
        
        Args:
            left: Left boundary
            right: Right boundary
            top: Top boundary
            bottom: Bottom boundary
        """
        self.viewport_left = left
        self.viewport_right = right
        self.viewport_top = top
        self.viewport_bottom = bottom
    
    def get_camera_position(self) -> Tuple[float, float]:
        """Get current camera position."""
        return self.position
    
    def set_position(self, x: float, y: float) -> None:
        """Set camera position directly."""
        self.position = (x, y)
    
    def reset(self) -> None:
        """Reset camera to default state."""
        self.position = (0, 0)
        self.target_position = (0, 0)
        self.shake_intensity = 0
        self.shake_timer = 0


class CameraShaker:
    """
    Manages collision shake effects separately from main camera.
    
    This allows for more complex shake patterns and multiple shake sources.
    """
    
    def __init__(self, intensity: float = COLLISION_SHAKE_INTENSITY):
        """Initialize the camera shaker."""
        self.intensity = intensity
        self.active = False
    
    def activate(self) -> None:
        """Activate shake effect."""
        self.active = True
    
    def update(self, delta_time: float) -> Tuple[float, float]:
        """
        Update shake and return current offset.
        
        Args:
            delta_time: Time in seconds
            
        Returns:
            (shake_x, shake_y) offset tuple
        """
        if not self.active:
            return (0, 0)
        
        # Decay intensity
        self.intensity *= 0.95
        
        # Generate random offset
        import random
        shake_x = (random.random() - 0.5) * self.intensity
        shake_y = (random.random() - 0.5) * self.intensity
        
        # Stop when intensity is negligible
        if self.intensity < 0.1:
            self.active = False
        
        return (shake_x, shake_y)


def create_smooth_camera(
    smoothing: float = CAMERA_SMOOTHING,
    viewport_bounds: Optional[Tuple[float, float, float, float]] = None
) -> CameraSystem:
    """
    Factory function to create a configured camera system.
    
    Args:
        smoothing: Camera smoothness factor (0.0-1.0)
        viewport_bounds: Optional (left, right, top, bottom) bounds
        
    Returns:
        Configured CameraSystem instance
    """
    camera = CameraSystem()
    camera.smoothing = smoothing
    
    if viewport_bounds:
        camera.set_viewport_bounds(*viewport_bounds)
    
    return camera
