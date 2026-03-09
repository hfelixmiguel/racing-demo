"""
Game Window Module - 2D Racing Game Demo

This module handles the game window setup using the Arcade library.
It provides a properly configured window with camera support, event handling,
and frame rate control for smooth gameplay at 60 FPS.

Author: hfelixmiguel
Issue: #14 - Phase 2: Implement Base Arcade Game Window & Loop
"""

import arcade
from typing import Optional, Tuple


class GameWindow:
    """
    Manages the game window and its configuration.
    
    This class handles:
    - Window creation with proper resolution (1280x720)
    - Camera setup for player following
    - Event handling (close, resize, key presses)
    - Frame rate control targeting 60 FPS
    
    Architecture follows Arcade's built-in features for camera and delta time.
    """
    
    # Window configuration constants
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    TARGET_FPS = 60
    BACKGROUND_COLOR = arcade.color.DARK_SLATE_GRAY
    
    def __init__(self):
        """Initialize the game window."""
        self.width = self.SCREEN_WIDTH
        self.height = self.SCREEN_HEIGHT
        
        # Arcade window instance (created when open_window is called)
        self.window: Optional[arcade.Window] = None
        
        # Camera for following the player
        self.camera: Optional[arcade.Camera] = None
        
        # Flag to track if window is currently open
        self.is_open = False
    
    def open_window(self) -> None:
        """
        Create and open the game window.
        
        Sets up:
        - Window size (1280x720)
        - Background color
        - Camera system
        - Frame rate control
        
        Example:
            >>> window = GameWindow()
            >>> window.open_window()
        """
        # Create the Arcade window with proper configuration
        self.window = arcade.Window(
            width=self.width,
            height=self.height,
            title="2D Racing Game Demo - Phase 2",
            show_cursor=False,  # Hide cursor for better immersion
            resizable=True      # Allow user to resize if needed
        )
        
        # Set up the camera system
        self.camera = arcade.Camera(
            width=self.width,
            height=self.height
        )
        
        # Make the window full screen initially (can be toggled)
        self.window.use_fullscreen(True)
        
        # Configure frame rate control
        arcade.set_fps_limit(self.TARGET_FPS)
        
        print(f"Game Window opened at {self.width}x{self.height}")
        print(f"Target FPS: {self.TARGET_FPS}")
        self.is_open = True
    
    def close_window(self) -> None:
        """Close the game window and clean up resources."""
        if self.window:
            self.window.close()
            self.window = None
        
        if self.camera:
            self.camera = None
        
        self.is_open = False
        print("Game Window closed.")
    
    def clear_screen(self, color: Tuple[float, float, float]) -> None:
        """
        Clear the screen with a specified background color.
        
        Args:
            color: RGB tuple (0-1 range) for the background color
            
        Example:
            >>> self.clear_screen(arcade.color.GRAY)
        """
        if self.window and self.camera:
            arcade.start_render()
            arcade.set_background_color(color)
    
    def set_camera_position(self, x: float, y: float) -> None:
        """
        Set the camera position to follow a specific point.
        
        Args:
            x: X coordinate for camera center
            y: Y coordinate for camera center
            
        Example:
            >>> self.set_camera_position(player_x, player_y)
        """
        if self.camera and self.window:
            self.camera.position = (x, y)
    
    def handle_resize(self, new_width: int, new_height: int) -> None:
        """
        Handle window resize events.
        
        Args:
            new_width: New window width
            new_height: New window height
            
        Note: Arcade handles this automatically, but we can add custom logic here
        if needed for responsive design or aspect ratio maintenance.
        """
        print(f"Window resized to {new_width}x{new_height}")
    
    def handle_close(self) -> None:
        """Handle window close event (X button or ESC key)."""
        self.close_window()
    
    def get_fps(self) -> int:
        """Get the current frame rate."""
        if self.window:
            return self.window.get_frame_count()
        return 0
    
    @property
    def width(self) -> int:
        """Get window width."""
        return self.SCREEN_WIDTH
    
    @width.setter
    def width(self, value: int) -> None:
        """Set window width (used for configuration)."""
        self.SCREEN_WIDTH = value
    
    @property
    def height(self) -> int:
        """Get window height."""
        return self.SCREEN_HEIGHT
    
    @height.setter
    def height(self, value: int) -> None:
        """Set window height (used for configuration)."""
        self.SCREEN_HEIGHT = value


def create_game_window(width: int = 1280, height: int = 720) -> GameWindow:
    """
    Factory function to create and open a game window.
    
    Args:
        width: Window width (default: 1280)
        height: Window height (default: 720)
        
    Returns:
        Configured and opened GameWindow instance
        
    Example:
        >>> window = create_game_window()
        >>> window.open_window()
    """
    window = GameWindow()
    
    # Override dimensions if specified
    if width != 1280 or height != 720:
        window.SCREEN_WIDTH = width
        window.SCREEN_HEIGHT = height
    
    window.open_window()
    return window


# Example usage (for testing purposes)
if __name__ == "__main__":
    print("Testing Game Window Module...")
    
    # Create and open window
    window = create_game_window()
    
    try:
        print(f"Window created at {window.width}x{window.height}")
        print("Press ESC or close the X button to exit.")
        
        # Keep running until closed (in real game, this would be called from game loop)
        while window.is_open:
            import time
            time.sleep(0.1)  # Small delay to prevent CPU spinning
            
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        window.close_window()
