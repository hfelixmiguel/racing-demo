"""
Arcade Game Window Configuration

This module sets up the base Arcade game window with proper configuration,
event handling, and frame rate control.
"""

import arcade
from typing import Optional


class GameWindow:
    """
    Manages the main game window and rendering context.
    
    Attributes:
        window: The Arcade window instance
        screen_width: Width of the game in pixels
        screen_height: Height of the game in pixels
        camera: Camera object for following the player
        running: Flag to control game loop execution
    """
    
    # Window configuration constants
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    TITLE = "2D Racing Game Demo"
    FPS = 60
    
    def __init__(self):
        """Initialize the game window with Arcade settings."""
        self.window: Optional[arcade.Window] = None
        self.camera: Optional[arcade.Camera] = None
        self.running = False
        
        # Initialize Arcade window
        self._setup_window()
    
    def _setup_window(self) -> None:
        """
        Configure and create the main game window.
        
        Sets up:
        - Window size and title
        - Frame rate control
        - Event handlers (close, resize)
        - Sprite texture atlas for rendering
        """
        # Create Arcade window with specified dimensions
        self.window = arcade.Window(
            width=self.SCREEN_WIDTH,
            height=self.SCREEN_HEIGHT,
            title=self.TITLE,
            resizable=False,  # Fixed size for consistent gameplay
            show_cursor=True,  # Show cursor for menu navigation
        )
        
        # Set background color (grass green for racing track)
        arcade.set_background_color(arcade.color.LAWN_GREEN)
        
        # Configure frame rate to target 60 FPS
        self.window.set_fps_limit(self.FPS)
        
        # Create camera that will follow the player
        self.camera = arcade.Camera(
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT
        )
        
        # Set up sprite texture atlas for efficient rendering
        # This allows multiple sprites to share the same texture
        arcade.use_texture_atlas(True)
    
    def open_window(self) -> None:
        """Open and display the game window."""
        if self.window is None:
            raise RuntimeError("GameWindow not initialized. Call _setup_window() first.")
        
        # Make window visible
        self.window.open()
        self.running = True
    
    def close_window(self) -> None:
        """Close the game window and clean up resources."""
        if self.window is not None:
            self.window.close()
            self.window = None
        
        if self.camera is not None:
            self.camera = None
        
        self.running = False
    
    def set_camera_position(self, center_x: float, center_y: float) -> None:
        """
        Set the camera to follow a specific position.
        
        Args:
            center_x: X coordinate to center camera on
            center_y: Y coordinate to center camera on
        """
        if self.camera is not None and self.window is not None:
            self.camera.position = (center_x, center_y)
    
    def set_camera_bounds(self, left: float, right: float, top: float, bottom: float) -> None:
        """
        Set camera view bounds to restrict visible area.
        
        Args:
            left: Left boundary of visible area
            right: Right boundary of visible area
            top: Top boundary of visible area
            bottom: Bottom boundary of visible area
        """
        if self.camera is not None and self.window is not None:
            self.camera.use_viewport_bounds(
                left=left,
                right=right,
                top=top,
                bottom=bottom
            )
    
    def clear_screen(self, color: tuple = arcade.color.LAWN_GREEN) -> None:
        """
        Clear the screen with specified color before rendering.
        
        Args:
            color: RGB tuple for background color (default: lawn green)
        """
        if self.window is not None:
            self.window.clear(color)
    
    def draw(self) -> bool:
        """
        Render the current frame.
        
        This method:
        1. Clears the screen
        2. Sets camera view
        3. Calls the draw function provided by caller
        
        Returns:
            True if rendering successful, False otherwise
        """
        if self.window is None or self.camera is None:
            return False
        
        try:
            # Clear screen with background color
            self.clear_screen()
            
            # Set camera to current position and make visible
            self.camera.use_viewport_bounds(
                left=0,
                right=self.SCREEN_WIDTH,
                top=0,
                bottom=self.SCREEN_HEIGHT
            )
            self.window.use_camera(self.camera)
            
            # Call the draw function (must be implemented by caller)
            return True
            
        except Exception as e:
            print(f"Error during rendering: {e}")
            return False
    
    def update(self, delta_time: float) -> None:
        """
        Update game state for a single frame.
        
        Args:
            delta_time: Time in seconds since last frame (for frame-rate independent updates)
        """
        if self.window is not None:
            # Check if window should be closed
            if self.window.should_close:
                self.close_window()
    
    def get_fps(self) -> int:
        """
        Get current frames per second.
        
        Returns:
            Current FPS as integer
        """
        if self.window is not None:
            return self.window.get_fps()
        return 0
    
    @property
    def width(self) -> int:
        """Get screen width."""
        return self.SCREEN_WIDTH
    
    @property
    def height(self) -> int:
        """Get screen height."""
        return self.SCREEN_HEIGHT


def create_game_window() -> GameWindow:
    """
    Factory function to create and configure game window.
    
    Returns:
        Configured GameWindow instance ready for use
    """
    game_window = GameWindow()
    game_window.open_window()
    return game_window
