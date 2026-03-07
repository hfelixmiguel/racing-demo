"""
Debug Overlay - Game Debug Information

This module implements a debug overlay showing FPS, player stats,
and other debugging information. Toggled with F1 key.
"""

import arcade
from typing import Optional


class DebugOverlay:
    """
    Manages the debug information overlay.
    
    Displays:
    - Current FPS
    - Player speed and position
    - Checkpoint index
    - Lap number
    - Physics values (when enabled)
    
    Toggled on/off with F1 key press.
    """
    
    def __init__(self):
        """Initialize the debug overlay."""
        # Display state
        self.is_visible = False
        
        # Font settings
        self.font_size = 18
        self.position_x = 10
        self.position_y = 10
        
        # Debug data
        self.fps: int = 0
        self.player_speed: float = 0.0
        self.checkpoint_index: int = -1
        self.lap_number: int = 1
        self.show_physics_values = True
        
        # Toggle state
        self.last_toggle = False
    
    def toggle(self) -> bool:
        """
        Toggle debug overlay visibility.
        
        Returns:
            True if toggled on, False if already on or toggled off
        """
        was_visible = self.is_visible
        self.is_visible = not self.is_visible
        
        return self.is_visible and not was_visible
    
    def update_fps(self, fps: int) -> None:
        """Update FPS display."""
        self.fps = fps
    
    def update_player_data(
        self,
        speed: float,
        checkpoint_index: int,
        lap_number: int
    ) -> None:
        """
        Update player data for display.
        
        Args:
            speed: Player speed in km/h
            checkpoint_index: Current checkpoint index (-1 if none)
            lap_number: Current lap number
        """
        self.player_speed = speed
        self.checkpoint_index = checkpoint_index
        self.lap_number = lap_number
    
    def update_physics_values(
        self,
        velocity: float,
        angle: float,
        acceleration: float,
        friction: float
    ) -> None:
        """Update physics values for display."""
        if not self.show_physics_values:
            return
        
        self.velocity = velocity
        self.angle = angle
        self.acceleration = acceleration
        self.friction = friction
    
    def draw(self, width: int, height: int) -> None:
        """
        Draw the debug overlay.
        
        Args:
            width: Screen width
            height: Screen height
        """
        if not self.is_visible:
            return
        
        # FPS counter (top left)
        arcade.draw_text(
            f"FPS: {self.fps}",
            self.position_x,
            height - self.position_y,
            font_name=arcade.FONT_NAME_MONOSPACE,
            font_size=self.font_size,
            anchor_x="left",
            color=arcade.color.WHITE
        )
        
        # Player speed (top right)
        arcade.draw_text(
            f"Speed: {self.player_speed:.1f} km/h",
            width - self.position_x - 150,
            height - self.position_y,
            font_name=arcade.FONT_NAME_MONOSPACE,
            font_size=self.font_size,
            anchor_x="right",
            color=arcade.color.WHITE
        )
        
        # Checkpoint and lap info (middle left)
        if self.checkpoint_index >= 0:
            arcade.draw_text(
                f"Checkpoint: {self.checkpoint_index + 1}",
                self.position_x,
                height - self.position_y - self.font_size * 2,
                font_name=arcade.FONT_NAME_MONOSPACE,
                font_size=self.font_size,
                anchor_x="left",
                color=arcade.color.YELLOW
            )
        
        arcade.draw_text(
            f"Lap: {self.lap_number}",
            self.position_x,
            height - self.position_y - self.font_size * 4,
            font_name=arcade.FONT_NAME_MONOSPACE,
            font_size=self.font_size,
            anchor_x="left",
            color=arcade.color.WHITE
        )
        
        # Physics values (bottom left, if enabled)
        if self.show_physics_values:
            arcade.draw_text(
                f"Velocity: {self.velocity:.2f} px/s",
                self.position_x,
                height - self.position_y - self.font_size * 6,
                font_name=arcade.FONT_NAME_MONOSPACE,
                font_size=self.font_size,
                anchor_x="left",
                color=arcade.color.GRAY
            )
            
            arcade.draw_text(
                f"Angle: {self.angle:.1f}°",
                self.position_x,
                height - self.position_y - self.font_size * 7,
                font_name=arcade.FONT_NAME_MONOSPACE,
                font_size=self.font_size,
                anchor_x="left",
                color=arcade.color.GRAY
            )
            
            arcade.draw_text(
                f"Accel: {self.acceleration:.2f} | Friction: {self.friction:.2f}",
                self.position_x,
                height - self.position_y - self.font_size * 8,
                font_name=arcade.FONT_NAME_MONOSPACE,
                font_size=self.font_size,
                anchor_x="left",
                color=arcade.color.GRAY
            )
        
        # Toggle instruction (bottom right)
        arcade.draw_text(
            "[F1] Toggle Debug",
            width - self.position_x - 150,
            height - self.position_y - self.font_size * 2,
            font_name=arcade.FONT_NAME_MONOSPACE,
            font_size=self.font_size,
            anchor_x="right",
            color=arcade.color.GRAY
        )


class FPSCounter:
    """
    Dedicated FPS counter with configurable display.
    
    Features:
    - Real-time FPS calculation
    - Minimum/maximum FPS tracking
    - Customizable display position and style
    """
    
    def __init__(self):
        """Initialize the FPS counter."""
        self.fps_history: list = []
        self.max_history = 60  # Track last 60 frames (1 second at 60 FPS)
        
        self.current_fps = 0
        self.min_fps = float('inf')
        self.max_fps = 0
        
        self.position_x = 10
        self.position_y = 10
        self.font_size = 24
    
    def update(self, fps: int) -> None:
        """Update FPS and track statistics."""
        self.fps_history.append(fps)
        
        # Keep history bounded
        if len(self.fps_history) > self.max_history:
            self.fps_history.pop(0)
        
        # Update current FPS
        self.current_fps = fps
        
        # Track min/max
        self.min_fps = min(self.min_fps, fps) if self.min_fps != float('inf') else fps
        self.max_fps = max(self.max_fps, fps)
    
    def draw(self, width: int, height: int) -> None:
        """Draw FPS counter."""
        if not self.fps_history:
            return
        
        # Calculate average FPS from history
        avg_fps = sum(self.fps_history) / len(self.fps_history)
        
        # Color based on performance
        if avg_fps >= 55:
            color = arcade.color.GREEN
        elif avg_fps >= 45:
            color = arcade.color.YELLOW
        else:
            color = arcade.color.RED
        
        # Draw main FPS display
        arcade.draw_text(
            f"FPS: {int(avg_fps)}",
            self.position_x,
            height - self.position_y,
            font_name=arcade.FONT_NAME_MONOSPACE,
            font_size=self.font_size,
            anchor_x="left",
            color=color
        )
        
        # Draw min/max FPS (smaller text)
        arcade.draw_text(
            f"Min: {int(self.min_fps)} | Max: {int(self.max_fps)}",
            self.position_x,
            height - self.position_y - self.font_size - 5,
            font_name=arcade.FONT_NAME_MONOSPACE,
            font_size=self.font_size // 2,
            anchor_x="left",
            color=color
        )


def create_debug_overlay() -> DebugOverlay:
    """
    Factory function to create a debug overlay.
    
    Returns:
        Configured DebugOverlay instance
    """
    return DebugOverlay()
