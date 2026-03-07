"""
Collision System - Track Boundary Collision Detection

This module handles collision detection between entities and track boundaries,
as well as entity-to-entity collisions.
"""

import arcade
from typing import Tuple, List, Optional


class CollisionSystem:
    """
    Manages all collision detection for the game.
    
    Features:
    - Track boundary collision
    - Entity-to-entity collision
    - Checkpoint collision
    - Collision response handling
    
    Uses axis-aligned bounding box (AABB) and circle collision detection.
    """
    
    def __init__(self):
        """Initialize the collision system."""
        # Track boundaries
        self.track_bounds: Tuple[float, float, float, float] = (0, 0, 0, 0)
        
        # Collision callbacks
        self.on_collision_handler = None
        
        # Collision state
        self.collision_active = False
    
    def set_track_bounds(
        self,
        left: float,
        right: float,
        bottom: float,
        top: float
    ) -> None:
        """Set track boundaries for collision detection."""
        self.track_bounds = (left, right, bottom, top)
    
    def check_track_collision(
        self,
        position: Tuple[float, float],
        entity_width: float,
        entity_height: float
    ) -> bool:
        """
        Check if entity is colliding with track boundaries.
        
        Args:
            position: Entity center position (x, y)
            entity_width: Width of the entity
            entity_height: Height of the entity
            
        Returns:
            True if collision detected, False otherwise
        """
        # Calculate corners of entity's bounding box
        half_width = entity_width / 2
        half_height = entity_height / 2
        
        corners = [
            (position[0] - half_width, position[1] - half_height),
            (position[0] + half_width, position[1] - half_height),
            (position[0] - half_width, position[1] + half_height),
            (position[0] + half_width, position[1] + half_height),
        ]
        
        # Check each corner against track bounds
        for corner_x, corner_y in corners:
            if not self._point_in_bounds(corner_x, corner_y):
                return True  # Corner outside bounds = collision
        
        return False
    
    def _point_in_bounds(self, x: float, y: float) -> bool:
        """Check if a point is within track boundaries."""
        left, right, bottom, top = self.track_bounds
        return (left <= x <= right) and (bottom <= y <= top)
    
    def check_circle_collision(
        self,
        pos1: Tuple[float, float],
        radius1: float,
        pos2: Tuple[float, float],
        radius2: float
    ) -> bool:
        """
        Check collision between two circles.
        
        Args:
            pos1: First circle center position
            radius1: First circle radius
            pos2: Second circle center position
            radius2: Second circle radius
            
        Returns:
            True if circles overlap, False otherwise
        """
        # Calculate distance between centers
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        # Check if distance is less than sum of radii
        return distance < (radius1 + radius2)
    
    def check_circle_collision_with_bounds(
        self,
        position: Tuple[float, float],
        radius: float
    ) -> bool:
        """
        Check if circle collides with track boundaries.
        
        Args:
            position: Circle center position
            radius: Circle radius
            
        Returns:
            True if collision detected, False otherwise
        """
        left, right, bottom, top = self.track_bounds
        
        # Check each edge
        # Left edge
        if position[0] - radius < left:
            return True
        
        # Right edge
        if position[0] + radius > right:
            return True
        
        # Bottom edge
        if position[1] - radius < bottom:
            return True
        
        # Top edge
        if position[1] + radius > top:
            return True
        
        return False
    
    def resolve_track_collision(
        self,
        position: Tuple[float, float],
        velocity: Tuple[float, float],
        entity_width: float,
        entity_height: float
    ) -> Tuple[float, float]:
        """
        Resolve collision by pushing entity back inside track.
        
        Args:
            position: Current entity position
            velocity: Entity velocity vector
            entity_width: Width of the entity
            entity_height: Height of the entity
            
        Returns:
            New position after resolution
        """
        half_width = entity_width / 2
        half_height = entity_height / 2
        
        new_position = list(position)
        
        # Check left boundary
        if position[0] - half_width < self.track_bounds[0]:
            new_position[0] = self.track_bounds[0] + half_width
        
        # Check right boundary
        if position[0] + half_width > self.track_bounds[1]:
            new_position[0] = self.track_bounds[1] - half_width
        
        # Check bottom boundary
        if position[1] - half_height < self.track_bounds[2]:
            new_position[1] = self.track_bounds[2] + half_height
        
        # Check top boundary
        if position[1] + half_height > self.track_bounds[3]:
            new_position[1] = self.track_bounds[3] - half_height
        
        return tuple(new_position)
    
    def check_checkpoint_collision(
        self,
        player_position: Tuple[float, float],
        checkpoint_radius: float,
        checkpoints: List[Tuple[float, float]]
    ) -> Optional[int]:
        """
        Check if player collided with any checkpoint.
        
        Args:
            player_position: Player position
            checkpoint_radius: Radius for collision detection
            checkpoints: List of checkpoint positions
            
        Returns:
            Index of checkpoint collided with, or None
        """
        for i, cp_pos in enumerate(checkpoints):
            if self.check_circle_collision(player_position, checkpoint_radius, cp_pos, checkpoint_radius):
                return i
        
        return None
    
    def trigger_collision(self) -> None:
        """Trigger collision callback if registered."""
        if self.on_collision_handler:
            self.on_collision_handler()


class EntityCollision:
    """
    Handles entity-to-entity collisions.
    
    Features:
    - Multiple entity collision detection
    - Collision response
    - Collision event handling
    """
    
    def __init__(self):
        """Initialize the entity collision system."""
        self.entities: List[dict] = []  # List of entity data dicts
    
    def register_entity(
        self,
        entity_id: str,
        position: Tuple[float, float],
        radius: float,
        is_static: bool = False
    ) -> None:
        """
        Register an entity for collision detection.
        
        Args:
            entity_id: Unique identifier for the entity
            position: Entity center position
            radius: Collision radius
            is_static: Whether entity is static (doesn't move)
        """
        self.entities.append({
            'id': entity_id,
            'position': position,
            'radius': radius,
            'is_static': is_static,
            'active': True
        })
    
    def check_all_collisions(
        self,
        on_collision: Optional[callable] = None
    ) -> List[Tuple[str, str]]:
        """
        Check for collisions between all registered entities.
        
        Args:
            on_collision: Callback function called when collision detected
            
        Returns:
            List of collision pairs (entity_id1, entity_id2)
        """
        collisions = []
        
        # Compare each pair of entities
        for i in range(len(self.entities)):
            for j in range(i + 1, len(self.entities)):
                e1 = self.entities[i]
                e2 = self.entities[j]
                
                if not e1.get('active', True) or not e2.get('active', True):
                    continue
                
                # Check collision
                if self.check_circle_collision(
                    e1['position'], e1['radius'],
                    e2['position'], e2['radius']
                ):
                    collisions.append((e1['id'], e2['id']))
                    
                    # Call callback
                    if on_collision:
                        on_collision(e1['id'], e2['id'])
        
        return collisions
    
    def check_circle_collision(
        self,
        pos1: Tuple[float, float],
        radius1: float,
        pos2: Tuple[float, float],
        radius2: float
    ) -> bool:
        """Check if two circles collide."""
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        return distance < (radius1 + radius2)


def create_collision_system(
    track_bounds: Optional[Tuple[float, float, float, float]] = None
) -> CollisionSystem:
    """
    Factory function to create a collision system.
    
    Args:
        track_bounds: Optional initial track boundaries
        
    Returns:
        Configured CollisionSystem instance
    """
    system = CollisionSystem()
    
    if track_bounds:
        system.set_track_bounds(*track_bounds)
    
    return system
