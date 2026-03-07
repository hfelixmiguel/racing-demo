"""
Car Entity - Player Racing Car

This module defines the player car entity with all its properties and methods.
The car is represented as a sprite in the game world with position, rotation,
and visual representation.
"""

import arcade
from typing import Optional, Tuple
from game.core.config import (
    CAR_WIDTH, CAR_HEIGHT, WHEEL_RADIUS,
    MAX_SPEED, ACCELERATION, BRAKING_POWER,
    TURNING_SENSITIVITY, FRICTION_COEFFICIENT, DRAG_FACTOR
)


class Car:
    """
    Represents the player's racing car in the game.
    
    Attributes:
        sprite: Arcade sprite for rendering the car body
        wheel_sprites: List of sprites for wheels (4 wheels)
        position: Current (x, y) position in world coordinates
        angle: Current rotation angle in degrees
        velocity: Current speed in pixels per second
        max_speed: Maximum allowed speed
        acceleration: Acceleration rate
        braking_power: Braking deceleration rate
        turning_sensitivity: How much the car turns per frame
        friction: Velocity decay coefficient
        drag: Air resistance factor
        is_on_track: Whether car is currently on valid track area
    """
    
    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        angle: float = 90.0,
        color: Tuple[int, int, int] = arcade.color.RED,
        max_speed: Optional[float] = None
    ):
        """
        Initialize the car entity.
        
        Args:
            x: Starting X position
            y: Starting Y position
            angle: Starting rotation angle (degrees, 0=right, 90=up)
            color: Car body color (RGB tuple or arcade.color name)
            max_speed: Override default maximum speed
        """
        # Position and orientation
        self.position: Tuple[float, float] = (x, y)
        self.angle = angle
        
        # Velocity and speed
        self.velocity = 0.0
        self.max_speed = max_speed or MAX_SPEED
        self.acceleration = ACCELERATION
        self.braking_power = BRAKING_POWER
        self.turning_sensitivity = TURNING_SENSITIVITY
        self.friction = FRICTION_COEFFICIENT
        self.drag = DRAG_FACTOR
        
        # Visual properties
        self.color = color if isinstance(color, tuple) else arcade.convert_color_string(color)
        
        # Create car sprite (body)
        self.sprite = arcade.Sprite(
            texture_path=None,  # Will be drawn as shape
            width=CAR_WIDTH,
            height=CAR_HEIGHT
        )
        self.sprite.center_on_position(x, y)
        self.sprite.angle = angle
        
        # Create wheel sprites (4 wheels)
        self.wheel_sprites: list[arcade.Sprite] = []
        for i in range(4):
            wheel = arcade.Sprite(
                texture_path=None,
                width=WHEEL_RADIUS * 2,
                height=WHEEL_RADIUS * 2
            )
            wheel.center_on_position(x, y)
            wheel.angle = angle
            
            # Position wheels at corners
            if i < 2:  # Front wheels
                offset_x = CAR_WIDTH / 2 - WHEEL_RADIUS
                offset_y = -CAR_HEIGHT / 2 + WHEEL_RADIUS
            else:  # Rear wheels
                offset_x = -CAR_WIDTH / 2 + WHEEL_RADIUS
                offset_y = -CAR_HEIGHT / 2 + WHEEL_RADIUS
            
            wheel.position = (x + offset_x, y + offset_y)
            self.wheel_sprites.append(wheel)
        
        # Track status
        self.is_on_track = True
    
    def update(self, delta_time: float) -> None:
        """
        Update car physics and position for one frame.
        
        Args:
            delta_time: Time in seconds since last frame
        """
        # Apply acceleration/deceleration based on current velocity
        if self.velocity > 0:
            # Decelerate when not accelerating (friction + drag)
            self.velocity *= (self.friction ** delta_time)
            self.velocity *= (1.0 - self.drag * delta_time)
            
            # Apply braking if needed (handled by input system)
        elif self.velocity < 0:
            # Reverse friction
            self.velocity *= (self.friction ** delta_time)
            self.velocity *= (1.0 - self.drag * delta_time)
        
        # Clamp velocity to max speed
        self.velocity = max(-self.max_speed / 2, min(self.max_speed, self.velocity))
        
        # Calculate turning amount (depends on speed)
        # Higher speed = wider turning arc
        speed_factor = abs(self.velocity) / self.max_speed
        turn_amount = self.turning_sensitivity * speed_factor * delta_time
        
        # Update angle based on turning
        if self.velocity != 0:
            self.angle += turn_amount
            
            # Normalize angle to 0-360 range
            self.angle = self.angle % 360
        
        # Update position based on velocity and angle
        # Arcade uses degrees where 0=right, 90=up
        radians = arcade.degrees_to_radians(self.angle)
        dx = self.velocity * delta_time * arcade.cos(radians)
        dy = self.velocity * delta_time * arcade.sin(radians)
        
        self.position = (self.position[0] + dx, self.position[1] + dy)
    
    def set_position(self, x: float, y: float) -> None:
        """Set car position directly."""
        self.position = (x, y)
    
    def set_angle(self, angle: float) -> None:
        """Set car rotation angle."""
        self.angle = angle % 360
    
    def set_velocity(self, velocity: float) -> None:
        """Set car velocity directly."""
        self.velocity = max(-self.max_speed / 2, min(self.max_speed, velocity))
    
    def accelerate(self) -> None:
        """Apply acceleration to the car."""
        if self.velocity < self.max_speed:
            self.velocity += self.acceleration
    
    def brake(self) -> None:
        """Apply braking to the car."""
        if self.velocity > 0:
            self.velocity -= self.braking_power
        elif self.velocity < 0:
            self.velocity += self.braking_power
    
    def turn_left(self, delta_time: float) -> None:
        """Turn the car left."""
        speed_factor = abs(self.velocity) / self.max_speed
        turn_amount = self.turning_sensitivity * speed_factor * delta_time
        self.angle -= turn_amount
        self.angle = self.angle % 360
    
    def turn_right(self, delta_time: float) -> None:
        """Turn the car right."""
        speed_factor = abs(self.velocity) / self.max_speed
        turn_amount = self.turning_sensitivity * speed_factor * delta_time
        self.angle += turn_amount
        self.angle = self.angle % 360
    
    def get_position(self) -> Tuple[float, float]:
        """Get current car position."""
        return self.position
    
    def get_angle(self) -> float:
        """Get current car angle."""
        return self.angle
    
    def get_velocity(self) -> float:
        """Get current car velocity."""
        return self.velocity
    
    def get_speed_kmh(self) -> float:
        """
        Get current speed in km/h.
        
        Returns:
            Speed in km/h (assuming 1 pixel/sec = 0.36 km/h)
        """
        return abs(self.velocity) * 0.36
    
    def get_speed_pixels_per_sec(self) -> float:
        """Get current speed in pixels per second."""
        return abs(self.velocity)
    
    def draw(self, sprite_manager: Optional[arcade.SpriteManager] = None) -> None:
        """
        Draw the car and its wheels.
        
        Args:
            sprite_manager: Optional arcade SpriteManager for rendering
        """
        # Draw car body (as a colored rectangle)
        if self.sprite is not None:
            self.sprite.draw()
        
        # Draw wheels
        for wheel in self.wheel_sprites:
            wheel.draw()
    
    def reset(self) -> None:
        """Reset car to initial state."""
        self.velocity = 0.0
        self.is_on_track = True
    
    @property
    def center_x(self) -> float:
        """Get car center X position."""
        return self.position[0]
    
    @property
    def center_y(self) -> float:
        """Get car center Y position."""
        return self.position[1]


def create_player_car(
    x: float = 0.0,
    y: float = 0.0,
    angle: float = 90.0,
    color: Tuple[int, int, int] = arcade.color.RED
) -> Car:
    """
    Factory function to create a player car.
    
    Args:
        x: Starting X position
        y: Starting Y position
        angle: Starting rotation angle
        color: Car body color
        
    Returns:
        Configured Car instance
    """
    return Car(x=x, y=y, angle=angle, color=color)
