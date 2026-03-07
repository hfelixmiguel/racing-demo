"""
HUD - Heads-Up Display

This module implements the in-game heads-up display showing lap information,
speed, and timing data.
"""

import arcade
from typing import Optional


class HUD:
    """
    Manages the heads-up display for the game.
    
    Displays:
    - Current lap number
    - Current lap time
    - Best lap time
    - Player speed
    
    Updates in real-time during gameplay.
    """
    
    def __init__(self):
        """Initialize the HUD."""
        # Display settings
        self.font_size = 24
        self.position_x = 20
        self.position_y = 50
        
        # Lap information
        self.current_lap = 1
        self.lap_time: float = 0.0
        self.best_lap_time: Optional[float] = None
        
        # Speed display
        self.speed_kmh: float = 0.0
        
        # Position offset for new lap message
        self.new_lap_offset_y = 0
    
    def update_lap_info(
        self,
        lap_number: int,
        lap_time: float,
        best_lap_time: Optional[float] = None
    ) -> None:
        """
        Update lap information.
        
        Args:
            lap_number: Current lap number
            lap_time: Current lap time in seconds
            best_lap_time: Best lap time for this lap (optional)
        """
        self.current_lap = lap_number
        self.lap_time = lap_time
        
        if best_lap_time is not None:
            self.best_lap_time = best_lap_time
    
    def update_speed(self, speed_kmh: float) -> None:
        """
        Update displayed speed.
        
        Args:
            speed_kmh: Speed in km/h
        """
        self.speed_kmh = speed_kmh
    
    def draw(self, width: int, height: int) -> None:
        """
        Draw the HUD to screen.
        
        Args:
            width: Screen width
            height: Screen height
        """
        # Lap number
        arcade.draw_text(
            f"Lap {self.current_lap}",
            self.position_x,
            height - self.position_y,
            font_name=arcade.FONT_NAME_NORMAL,
            font_size=self.font_size,
            anchor_x="left",
            color=arcade.color.WHITE
        )
        
        # Current lap time
        minutes = int(self.lap_time // 60)
        seconds = (self.lap_time % 60)
        milliseconds = (self.lap_time * 1000) % 1000
        
        time_str = f"{minutes}:{seconds:02d}.{milliseconds:03d}"
        arcade.draw_text(
            f"Time: {time_str}",
            self.position_x,
            height - self.position_y - self.font_size - 10,
            font_name=arcade.FONT_NAME_NORMAL,
            font_size=self.font_size,
            anchor_x="left",
            color=arcade.color.WHITE
        )
        
        # Best lap time
        if self.best_lap_time is not None:
            best_minutes = int(self.best_lap_time // 60)
            best_seconds = (self.best_lap_time % 60)
            best_ms = (self.best_lap_time * 1000) % 1000
            
            best_str = f"{best_minutes}:{best_seconds:02d}.{best_ms:03d}"
            arcade.draw_text(
                f"Best: {best_str}",
                self.position_x,
                height - self.position_y - (self.font_size + 10) * 2,
                font_name=arcade.FONT_NAME_NORMAL,
                font_size=self.font_size,
                anchor_x="left",
                color=arcade.color.YELLOW
            )
        
        # Speed
        arcade.draw_text(
            f"Speed: {self.speed_kmh:.0f} km/h",
            width - self.position_x - 150,
            height - self.position_y,
            font_name=arcade.FONT_NAME_NORMAL,
            font_size=self.font_size,
            anchor_x="right",
            color=arcade.color.WHITE
        )
    
    def draw_new_lap_message(self, width: int, height: int) -> None:
        """
        Draw new lap completion message.
        
        Args:
            width: Screen width
            height: Screen height
        """
        if self.new_lap_offset_y > 0:
            arcade.draw_text(
                "LAP COMPLETE!",
                width / 2,
                height - self.position_y - self.new_lap_offset_y,
                font_name=arcade.FONT_NAME_NORMAL,
                font_size=48,
                anchor_x="center",
                color=arcade.color.YELLOW
            )
            
            # Fade out effect
            self.new_lap_offset_y += 2
            
            if self.new_lap_offset_y > 60:
                self.new_lap_offset_y = 0


class Speedometer:
    """
    Displays speed with visual gauge.
    
    Features:
    - Numeric speed display
    - Visual speed bar
    - Color-coded by speed range
    """
    
    def __init__(self):
        """Initialize the speedometer."""
        self.speed_kmh = 0.0
        self.max_speed = 200.0  # Maximum speed for gauge
        
        # Gauge settings
        self.gauge_width = 150
        self.gauge_height = 20
        self.position_x = 20
        self.position_y = 30
    
    def update_speed(self, speed_kmh: float) -> None:
        """Update displayed speed."""
        self.speed_kmh = max(0, min(speed_kmh, self.max_speed))
    
    def draw(self, width: int, height: int) -> None:
        """Draw the speedometer."""
        # Calculate gauge fill percentage
        fill_percentage = self.speed_kmh / self.max_speed
        
        # Draw gauge background
        arcade.draw_rectangle_filled(
            self.position_x + self.gauge_width // 2,
            self.position_y,
            self.gauge_width,
            self.gauge_height,
            color=arcade.color.GRAY
        )
        
        # Draw speed fill (color changes with speed)
        if fill_percentage < 0.5:
            fill_color = arcade.color.GREEN
        elif fill_percentage < 0.8:
            fill_color = arcade.color.YELLOW
        else:
            fill_color = arcade.color.RED
        
        fill_width = self.gauge_width * fill_percentage
        arcade.draw_rectangle_filled(
            self.position_x + self.gauge_width // 2,
            self.position_y,
            fill_width,
            self.gauge_height,
            color=fill_color
        )
        
        # Draw numeric speed
        arcade.draw_text(
            f"{self.speed_kmh:.0f} km/h",
            self.position_x + self.gauge_width // 2 + 10,
            self.position_y,
            font_name=arcade.FONT_NAME_NORMAL,
            font_size=self.font_size,
            anchor_x="left",
            color=arcade.color.WHITE
        )


class LapInfoDisplay:
    """
    Displays detailed lap information.
    
    Features:
    - Current lap number
    - Lap time with milliseconds
    - Best lap comparison
    - Checkpoint progress
    """
    
    def __init__(self):
        """Initialize the lap info display."""
        self.lap_number = 1
        self.lap_time: float = 0.0
        self.best_lap_time: Optional[float] = None
        self.checkpoints_visited = 0
        self.total_checkpoints = 4
    
    def update(self, lap_number: int, lap_time: float) -> None:
        """Update lap information."""
        self.lap_number = lap_number
        self.lap_time = lap_time
    
    def draw(self, width: int, height: int) -> None:
        """Draw lap information."""
        # Lap number
        arcade.draw_text(
            f"LAP {self.lap_number}",
            10,
            height - 40,
            font_name=arcade.FONT_NAME_NORMAL,
            font_size=28,
            anchor_x="left",
            color=arcade.color.WHITE
        )
        
        # Lap time
        minutes = int(self.lap_time // 60)
        seconds = (self.lap_time % 60)
        ms = (self.lap_time * 1000) % 1000
        
        time_str = f"{minutes}:{seconds:02d}.{ms:03d}"
        arcade.draw_text(
            f"TIME: {time_str}",
            10,
            height - 75,
            font_name=arcade.FONT_NAME_NORMAL,
            font_size=24,
            anchor_x="left",
            color=arcade.color.WHITE
        )
        
        # Best lap
        if self.best_lap_time is not None:
            best_minutes = int(self.best_lap_time // 60)
            best_seconds = (self.best_lap_time % 60)
            best_ms = (self.best_lap_time * 1000) % 1000
            
            best_str = f"{best_minutes}:{best_seconds:02d}.{best_ms:03d}"
            arcade.draw_text(
                f"BEST: {best_str}",
                10,
                height - 110,
                font_name=arcade.FONT_NAME_NORMAL,
                font_size=24,
                anchor_x="left",
                color=arcade.color.YELLOW
            )
        
        # Checkpoint progress
        if self.total_checkpoints > 0:
            progress = (self.checkpoints_visited / self.total_checkpoints) * 100
            arcade.draw_text(
                f"CHECKPOINTS: {self.checkpoints_visited}/{self.total_checkpoints} ({progress:.0f}%)",
                width - 250,
                height - 40,
                font_name=arcade.FONT_NAME_NORMAL,
                font_size=16,
                anchor_x="right",
                color=arcade.color.GRAY
            )
