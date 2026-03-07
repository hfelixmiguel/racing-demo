"""
Physics System - Car Physics Calculations

This module implements the complete physics model for the racing car,
including acceleration, braking, steering, friction, and drag.
The physics calculations are frame-rate independent using delta time.
"""

import arcade
from typing import Tuple
from game.core.config import (
    MAX_SPEED, ACCELERATION, BRAKING_POWER,
    TURNING_RADIUS_FULL_SPEED, STEERING_SENSITIVITY,
    FRICTION_COEFFICIENT, DRAG_FACTOR, CAR_WIDTH, CAR_HEIGHT
)


class PhysicsSystem:
    """
    Manages all physics calculations for the car.
    
    Implements a realistic car physics model with:
    - Speed-dependent acceleration and braking
    - Turning radius that varies with speed
    - Friction and air drag
    - Velocity clamping and normalization
    
    The physics uses delta time for frame-rate independence, ensuring
    consistent behavior regardless of frame rate.
    """
    
    def __init__(self):
        """Initialize the physics system with default parameters."""
        # Store current physics state
        self.velocity = 0.0
        self.angle = 90.0  # Degrees (0=right, 90=up)
        
        # Physics parameters (can be overridden)
        self.max_speed = MAX_SPEED
        self.acceleration = ACCELERATION
        self.braking_power = BRAKING_POWER
        self.turning_radius_full_speed = TURNING_RADIUS_FULL_SPEED
        self.steering_sensitivity = STEERING_SENSITIVITY
        self.friction = FRICTION_COEFFICIENT
        self.drag = DRAG_FACTOR
        
        # Track boundaries (set when track is loaded)
        self.track_bounds: Tuple[float, float, float, float] = (0, 0, 0, 0)
    
    def update(
        self,
        velocity: float,
        angle: float,
        is_accelerating: bool,
        is_braking: bool,
        is_turning_left: bool,
        is_turning_right: bool,
        delta_time: float
    ) -> Tuple[float, float]:
        """
        Update physics state for one frame.
        
        Args:
            velocity: Current velocity in pixels/second
            angle: Current angle in degrees
            is_accelerating: Whether accelerator is pressed
            is_braking: Whether brake is pressed
            is_turning_left: Whether left turn is active
            is_turning_right: Whether right turn is active
            delta_time: Time in seconds since last frame
            
        Returns:
            Tuple of (new_velocity, new_angle)
        """
        # Apply acceleration or braking
        if is_accelerating:
            # Acceleration decreases as we approach max speed
            # This creates a smooth acceleration curve
            speed_ratio = velocity / self.max_speed
            effective_acceleration = self.acceleration * (1.0 - speed_ratio)
            velocity += effective_acceleration * delta_time
            
        elif is_braking:
            # Braking is more powerful at higher speeds
            velocity -= self.braking_power * delta_time
        
        # Apply friction and drag when not actively controlling
        if not is_accelerating and not is_braking:
            # Friction reduces velocity exponentially
            velocity *= (self.friction ** delta_time)
            
            # Air drag adds additional resistance
            velocity *= (1.0 - self.drag * delta_time)
        
        # Clamp velocity to maximum/minimum limits
        velocity = max(-self.max_speed / 2, min(self.max_speed, velocity))
        
        # Calculate turning amount based on speed
        # At full speed: wider turning arc
        # At low speed: tighter turns possible
        speed_factor = abs(velocity) / self.max_speed
        
        # Steering effectiveness decreases at high speeds
        # This prevents the car from spinning out at top speed
        steering_effectiveness = 1.0 - (speed_factor * 0.5)
        
        turn_amount = 0.0
        if is_turning_left or is_turning_right:
            # Base turning amount depends on speed and sensitivity
            base_turn = self.steering_sensitivity * speed_factor
            
            # Apply steering input
            if is_turning_left:
                turn_amount -= base_turn * steering_effectiveness
            elif is_turning_right:
                turn_amount += base_turn * steering_effectiveness
        
        # Update angle with turning
        new_angle = angle + turn_amount
        
        # Normalize angle to 0-360 range
        new_angle = new_angle % 360
        
        return (velocity, new_angle)
    
    def calculate_turning_radius(self, velocity: float) -> float:
        """
        Calculate the turning radius at current speed.
        
        Args:
            velocity: Current velocity in pixels/second
            
        Returns:
            Turning radius in pixels
        """
        speed_ratio = abs(velocity) / self.max_speed
        
        # At full speed: use configured turning radius
        # At low speed: much tighter turns (smaller radius)
        if speed_ratio == 0:
            return self.turning_radius_full_speed * 0.3  # Tightest turn
        
        # Interpolate between tight and wide turning
        radius = self.turning_radius_full_speed / (1.0 + speed_factor * 0.5)
        
        return max(radius, self.turning_radius_full_speed * 0.3)
    
    def calculate_drift_amount(self, velocity: float, angle_change: float) -> float:
        """
        Calculate how much the car would drift based on cornering force.
        
        Args:
            velocity: Current velocity
            angle_change: How much the car turned
            
        Returns:
            Drift amount (0.0 = no drift, 1.0 = maximum drift)
        """
        # Drift increases with speed and sharp turns
        speed_factor = abs(velocity) / self.max_speed
        
        # Normalize angle change to 0-1 range (-180 to 180 degrees)
        normalized_turn = abs(angle_change) / 180.0
        
        # Combine factors for drift calculation
        drift = (speed_factor * 0.7 + normalized_turn * 0.3)
        
        return min(drift, 1.0)
    
    def check_collision_with_boundaries(
        self,
        position: Tuple[float, float],
        car_width: float = CAR_WIDTH,
        car_height: float = CAR_HEIGHT
    ) -> bool:
        """
        Check if car position is within track boundaries.
        
        Args:
            position: Current (x, y) position of car
            car_width: Width of the car for collision box
            car_height: Height of the car for collision box
            
        Returns:
            True if car is outside boundaries (collision), False otherwise
        """
        # Get half dimensions for collision box
        half_width = car_width / 2
        half_height = car_height / 2
        
        # Check all four corners of the car's bounding box
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
        
        return False  # All corners inside bounds
    
    def _point_in_bounds(self, x: float, y: float) -> bool:
        """Check if a point is within track boundaries."""
        left, right, bottom, top = self.track_bounds
        
        return (left <= x <= right) and (bottom <= y <= top)
    
    def set_track_bounds(
        self,
        left: float,
        right: float,
        bottom: float,
        top: float
    ) -> None:
        """
        Set the track boundaries for collision detection.
        
        Args:
            left: Left boundary X coordinate
            right: Right boundary X coordinate
            bottom: Bottom boundary Y coordinate
            top: Top boundary Y coordinate
        """
        self.track_bounds = (left, right, bottom, top)
    
    def reset(self) -> None:
        """Reset physics state to defaults."""
        self.velocity = 0.0
        self.angle = 90.0


class PhysicsCalculator:
    """
    Helper class for calculating physics values without full simulation.
    
    Useful for:
    - Displaying speed in HUD
    - Calculating expected turning radius
    - Predicting car behavior
    """
    
    @staticmethod
    def calculate_expected_position(
        current_x: float,
        current_y: float,
        velocity: float,
        angle: float,
        delta_time: float
    ) -> Tuple[float, float]:
        """
        Calculate where the car will be after delta_time.
        
        Args:
            current_x: Current X position
            current_y: Current Y position
            velocity: Current velocity
            angle: Current angle in degrees
            delta_time: Time interval
            
        Returns:
            (new_x, new_y) position
        """
        radians = arcade.degrees_to_radians(angle)
        dx = velocity * delta_time * arcade.cos(radians)
        dy = velocity * delta_time * arcade.sin(radians)
        
        return (current_x + dx, current_y + dy)
    
    @staticmethod
    def calculate_stopping_distance(velocity: float, braking_power: float = BRAKING_POWER) -> float:
        """
        Calculate distance needed to stop from current velocity.
        
        Args:
            velocity: Current velocity in pixels/second
            braking_power: Braking deceleration rate
            
        Returns:
            Stopping distance in pixels
        """
        if velocity == 0:
            return 0.0
        
        # Using physics formula: d = v² / (2a)
        stopping_distance = (velocity ** 2) / (2 * braking_power)
        
        return stopping_distance
    
    @staticmethod
    def calculate_acceleration_time(
        velocity: float,
        target_velocity: float,
        acceleration: float = ACCELERATION
    ) -> float:
        """
        Calculate time needed to reach target velocity.
        
        Args:
            velocity: Current velocity
            target_velocity: Target velocity
            acceleration: Acceleration rate
            
        Returns:
            Time in seconds
        """
        if acceleration == 0:
            return float('inf')
        
        time_needed = (target_velocity - velocity) / acceleration
        
        return max(0, time_needed)


# Physics constants for reference
PHYSICS_CONSTANTS = {
    'max_speed': MAX_SPEED,
    'acceleration': ACCELERATION,
    'braking_power': BRAKING_POWER,
    'turning_radius_full_speed': TURNING_RADIUS_FULL_SPEED,
    'steering_sensitivity': STEERING_SENSITIVITY,
    'friction': FRICTION_COEFFICIENT,
    'drag': DRAG_FACTOR,
}
