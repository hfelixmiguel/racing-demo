"""
Track Renderer - Render Tracks and Boundaries

This module handles rendering of tracks, boundaries, checkpoints,
and other track-related visual elements.
"""

import arcade
from typing import List, Optional, Tuple
from game.tracks.track_loader import TrackData


class TrackRenderer:
    """
    Renders tracks and their components to the screen.
    
    Features:
    - Track surface rendering
    - Boundary line drawing
    - Checkpoint markers
    - Start/finish line visualization
    
    Uses Arcade's shape drawing capabilities for efficient rendering.
    """
    
    def __init__(self):
        """Initialize the track renderer."""
        self.checkpoint_radius = 15
        self.checkpoint_color = (1.0, 0.8, 0.0)  # Yellow
        
        # Track colors
        self.track_grass_color = (0.42, 0.67, 0.33)
        self.track_road_color = (0.54, 0.81, 0.39)
        self.track_border_color = (0.85, 0.85, 0.85)  # White
        
        # Line width for boundaries
        self.boundary_line_width = 3
    
    def draw_track(
        self,
        track_data: TrackData,
        camera_position: Optional[Tuple[float, float]] = None
    ) -> None:
        """
        Draw the complete track with all components.
        
        Args:
            track_data: Loaded track configuration
            camera_position: Optional camera position for rendering optimization
        """
        # Draw grass area (background)
        self._draw_grass_area(track_data)
        
        # Draw track surface
        self._draw_track_surface(track_data)
        
        # Draw boundaries
        self._draw_boundaries(track_data)
        
        # Draw checkpoints
        self._draw_checkpoints(track_data)
    
    def _draw_grass_area(self, track_data: TrackData) -> None:
        """Draw the grass area surrounding the track."""
        arcade.draw_rectangle_filled(
            0, 0,
            track_data.boundaries['right'] - track_data.boundaries['left'],
            track_data.boundaries['top'] - track_data.boundaries['bottom'],
            color=arcade.color.rgb_to_hex(*track_data.grass_color)
        )
    
    def _draw_track_surface(self, track_data: TrackData) -> None:
        """Draw the main track surface."""
        # Calculate track dimensions with padding
        padding = 20
        
        left = track_data.boundaries['left'] + padding
        right = track_data.boundaries['right'] - padding
        bottom = track_data.boundaries['bottom'] + padding
        top = track_data.boundaries['top'] - padding
        
        # Draw track surface as a large rectangle
        arcade.draw_rectangle_filled(
            0, 0,
            right - left,
            top - bottom,
            color=arcade.color.rgb_to_hex(*track_data.surface_color)
        )
    
    def _draw_boundaries(self, track_data: TrackData) -> None:
        """Draw track boundaries and borders."""
        # Draw outer border
        arcade.draw_rectangle_outline(
            0, 0,
            track_data.boundaries['right'] - track_data.boundaries['left'],
            track_data.boundaries['top'] - track_data.boundaries['bottom'],
            color=arcade.color.rgb_to_hex(*track_data.surface_color),
            line_width=self.boundary_line_width
        )
        
        # Draw inner boundary (road edge)
        padding = 20
        left = track_data.boundaries['left'] + padding
        right = track_data.boundaries['right'] - padding
        bottom = track_data.boundaries['bottom'] + padding
        top = track_data.boundaries['top'] - padding
        
        arcade.draw_rectangle_outline(
            0, 0,
            right - left,
            top - bottom,
            color=arcade.color.rgb_to_hex(*self.track_border_color),
            line_width=self.boundary_line_width
        )
    
    def _draw_checkpoints(self, track_data: TrackData) -> None:
        """Draw checkpoint markers."""
        for checkpoint in track_data.checkpoints:
            pos = checkpoint['position']
            
            # Draw checkpoint circle
            arcade.draw_circle_filled(
                pos[0], pos[1],
                self.checkpoint_radius,
                color=arcade.color.rgb_to_hex(*self.checkpoint_color)
            )
            
            # Draw checkpoint border
            arcade.draw_circle_outline(
                pos[0], pos[1],
                self.checkpoint_radius + 3,
                color=arcade.color.rgb_to_hex(*self.checkpoint_color),
                line_width=2
            )
    
    def draw_start_finish_line(
        self,
        track_data: TrackData,
        position: Tuple[float, float] = (0, 0)
    ) -> None:
        """
        Draw start/finish line at specified position.
        
        Args:
            track_data: Track configuration
            position: Position of the start/finish line
        """
        # Draw checkered pattern
        square_size = 20
        offset_x, offset_y = position
        
        for row in range(4):
            for col in range(4):
                x = offset_x + (col * square_size) - square_size
                y = offset_y + (row * square_size) - square_size
                
                # Alternate black and white squares
                if (row + col) % 2 == 0:
                    arcade.draw_rectangle_filled(x, y, square_size, square_size, arcade.color.BLACK)
                else:
                    arcade.draw_rectangle_filled(x, y, square_size, square_size, arcade.color.WHITE)


class TrackVisualizer:
    """
    Provides additional visualizations for tracks.
    
    Features:
    - Lap progress indicator
    - Checkpoint connection lines
    - Track preview rendering
    """
    
    def __init__(self):
        """Initialize the track visualizer."""
        self.checkpoint_radius = 15
    
    def draw_checkpoint_connections(
        self,
        checkpoints: List[dict],
        line_width: int = 2
    ) -> None:
        """
        Draw lines connecting checkpoints to show lap path.
        
        Args:
            checkpoints: List of checkpoint position dicts
            line_width: Width of connection lines
        """
        if len(checkpoints) < 2:
            return
        
        # Draw lines between consecutive checkpoints
        for i in range(len(checkpoints) - 1):
            start = checkpoints[i]['position']
            end = checkpoints[i + 1]['position']
            
            arcade.draw_line(
                start[0], start[1],
                end[0], end[1],
                color=(0.8, 0.6, 0.2),
                line_width=line_width
            )
        
        # Draw line from last checkpoint back to first (complete lap)
        if len(checkpoints) > 1:
            start = checkpoints[-1]['position']
            end = checkpoints[0]['position']
            
            arcade.draw_line(
                start[0], start[1],
                end[0], end[1],
                color=(0.8, 0.6, 0.2),
                line_width=line_width,
                dash_length=10,
                gap_length=5
            )
    
    def draw_lap_progress(
        self,
        current_checkpoint: int,
        total_checkpoints: int,
        checkpoint_positions: List[Tuple[float, float]]
    ) -> None:
        """
        Draw visual indicator of lap progress.
        
        Args:
            current_checkpoint: Index of current checkpoint (0-based)
            total_checkpoints: Total number of checkpoints
            checkpoint_positions: List of checkpoint positions
        """
        if len(checkpoint_positions) < 2:
            return
        
        # Draw line from start to current checkpoint
        for i in range(min(current_checkpoint + 1, total_checkpoints - 1)):
            pos = checkpoint_positions[i]
            
            arcade.draw_circle_filled(
                pos[0], pos[1],
                self.checkpoint_radius,
                color=(0.2, 0.8, 0.2) if i < current_checkpoint else (0.8, 0.6, 0.2)
            )


def render_track_preview(track_data: TrackData, scale: float = 1.0) -> None:
    """
    Render a small preview of the track for menu display.
    
    Args:
        track_data: Track configuration
        scale: Scaling factor for preview size
    """
    # Draw simplified track outline
    padding = 20 * scale
    
    left = track_data.boundaries['left'] + padding
    right = track_data.boundaries['right'] - padding
    bottom = track_data.boundaries['bottom'] + padding
    top = track_data.boundaries['top'] - padding
    
    # Draw track surface
    arcade.draw_rectangle_filled(
        0, 0,
        right - left,
        top - bottom,
        color=arcade.color.rgb_to_hex(*track_data.surface_color)
    )
    
    # Draw boundary
    arcade.draw_rectangle_outline(
        0, 0,
        right - left,
        top - bottom,
        color=arcade.color.rgb_to_hex(*track_data.surface_color),
        line_width=int(2 * scale)
    )
