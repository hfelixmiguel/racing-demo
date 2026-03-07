"""
Transform Component - Position and Rotation Management

This module manages the transform component for game entities,
handling position, rotation, and scale transformations.
"""

import arcade
from typing import Tuple


class Transform:
    """
    Manages entity transform properties (position, rotation, scale).
    
    Attributes:
        position: Entity position in world coordinates (x, y)
        angle: Entity rotation angle in degrees
        scale: Entity scale factor (uniform scaling)
        
    The transform is used to calculate the final position and orientation
    of game entities for rendering and collision detection.
    """
    
    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        angle: float = 0.0,
        scale: float = 1.0
    ):
        """Initialize transform with given properties."""
        self.position: Tuple[float, float] = (x, y)
        self.angle = angle
        self.scale = scale
    
    @property
    def x(self) -> float:
        """Get X position."""
        return self.position[0]
    
    @property
    def y(self) -> float:
        """Get Y position."""
        return self.position[1]
    
    @property
    def center_x(self) -> float:
        """Get center X position."""
        return self.x
    
    @property
    def center_y(self) -> float:
        """Get center Y position."""
        return self.y
    
    def set_position(self, x: float, y: float) -> None:
        """Set entity position."""
        self.position = (x, y)
    
    def set_x(self, x: float) -> None:
        """Set X position only."""
        self.position = (x, self.position[1])
    
    def set_y(self, y: float) -> None:
        """Set Y position only."""
        self.position = (self.position[0], y)
    
    def move(self, dx: float, dy: float) -> None:
        """Move entity by offset."""
        self.position = (self.x + dx, self.y + dy)
    
    def set_angle(self, angle: float) -> None:
        """Set entity rotation angle."""
        self.angle = angle
    
    def rotate(self, delta_angle: float) -> None:
        """Rotate entity by delta angle."""
        self.angle += delta_angle
        # Normalize to 0-360 range
        self.angle = self.angle % 360
    
    def set_scale(self, scale: float) -> None:
        """Set entity scale factor."""
        self.scale = scale
    
    def get_position_tuple(self) -> Tuple[float, float]:
        """Get position as tuple."""
        return self.position
    
    def __repr__(self) -> str:
        """String representation of transform."""
        return f"Transform(pos={self.position}, angle={self.angle}, scale={self.scale})"


class TransformManager:
    """
    Manages transforms for multiple entities.
    
    Features:
    - Batch transform updates
    - Local to world coordinate conversion
    - Camera-relative positioning
    """
    
    def __init__(self):
        """Initialize the transform manager."""
        self.transforms: dict = {}  # entity_id -> Transform
    
    def register_transform(self, entity_id: str, transform: Transform) -> None:
        """Register a transform for an entity."""
        self.transforms[entity_id] = transform
    
    def get_transform(self, entity_id: str) -> Optional[Transform]:
        """Get transform for an entity."""
        return self.transforms.get(entity_id)
    
    def update_all(
        self,
        camera_position: Tuple[float, float] = (0, 0),
        delta_time: float = 0.016
    ) -> None:
        """
        Update all registered transforms.
        
        Args:
            camera_position: Current camera position
            delta_time: Time since last update
        """
        for entity_id, transform in self.transforms.items():
            # Apply any pending updates (can be overridden by subclasses)
            transform.update(delta_time)
    
    def convert_to_world(
        self,
        local_x: float,
        local_y: float,
        camera_position: Tuple[float, float] = (0, 0)
    ) -> Tuple[float, float]:
        """
        Convert local coordinates to world coordinates.
        
        Args:
            local_x: Local X coordinate
            local_y: Local Y coordinate
            camera_position: Camera position
            
        Returns:
            World coordinates (x, y)
        """
        return (local_x + camera_position[0], local_y + camera_position[1])
    
    def convert_to_local(
        self,
        world_x: float,
        world_y: float,
        camera_position: Tuple[float, float] = (0, 0)
    ) -> Tuple[float, float]:
        """
        Convert world coordinates to local (screen) coordinates.
        
        Args:
            world_x: World X coordinate
            world_y: World Y coordinate
            camera_position: Camera position
            
        Returns:
            Local coordinates (x, y)
        """
        return (world_x - camera_position[0], world_y - camera_position[1])


def create_transform(x: float = 0.0, y: float = 0.0, angle: float = 0.0) -> Transform:
    """
    Factory function to create a transform.
    
    Args:
        x: Initial X position
        y: Initial Y position
        angle: Initial rotation angle
        
    Returns:
        Configured Transform instance
    """
    return Transform(x=x, y=y, angle=angle)
