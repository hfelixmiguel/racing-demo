"""
Game Loop Module - 2D Racing Game Demo

This module implements the main game loop with proper delta time handling.
It ensures frame-rate independent calculations and smooth gameplay at 60 FPS.

Author: hfelixmiguel
Issue: #14 - Phase 2: Implement Base Arcade Game Window & Loop
"""

import arcade
from typing import Optional, Callable, Any


class GameLoop:
    """
    Manages the main game loop with delta time handling.
    
    This class handles:
    - Main loop structure (update -> draw)
    - Delta time calculations for frame-rate independence
    - FPS counter and throttling mechanism
    - Proper cleanup on window close
    
    Architecture follows Arcade's built-in features for camera and delta time.
    """
    
    # Configuration constants
    TARGET_FPS = 60
    MAX_DT = 1.0  # Maximum delta time to prevent huge jumps if game pauses
    
    def __init__(self, fps_target: int = 60):
        """
        Initialize the game loop.
        
        Args:
            fps_target: Target frames per second (default: 60)
            
        Example:
            >>> loop = GameLoop(fps_target=60)
            >>> loop.start()
        """
        self.fps_target = fps_target
        self.window: Optional[arcade.Window] = None
        
        # Timing variables
        self.last_frame_time: float = 0.0
        self.current_fps = 0.0
        self.frame_count = 0
        self.fps_update_interval = 1.0 / fps_target
        
        # Callbacks for update and draw phases
        self.update_callback: Optional[Callable[[float], None]] = None
        self.draw_callback: Optional[Callable[[], bool]] = None
        
        # Running state
        self.running = False
    
    def start(self) -> None:
        """Start the game loop."""
        if not self.window:
            raise RuntimeError("GameLoop: Window must be set before starting")
        
        self.running = True
        self.last_frame_time = arcade.get_current_time()
        
        # Start Arcade's main loop with our callbacks
        arcade.run(self.on_update)
    
    def stop(self) -> None:
        """Stop the game loop."""
        self.running = False
    
    def on_update(self, delta_time: float) -> None:
        """
        Main update callback called by Arcade.
        
        This is the entry point for each frame. It handles:
        - Delta time calculation and throttling
        - Update phase (game logic)
        - Draw phase (rendering)
        
        Args:
            delta_time: Time in seconds since last frame
            
        Example:
            >>> arcade.run(self.on_update)
        """
        # Throttle delta time to prevent huge jumps if game pauses
        if delta_time > self.MAX_DT:
            delta_time = self.MIN_DT
        
        # Update timing statistics
        self.frame_count += 1
        current_fps = self.frame_count / delta_time if delta_time > 0 else 0
        self.current_fps = current_fps
        
        # Call update callback (game logic)
        if self.update_callback:
            try:
                self.update_callback(delta_time)
            except Exception as e:
                print(f"Error in update phase: {e}")
        
        # Call draw callback (rendering)
        if self.draw_callback:
            try:
                should_continue = self.draw_callback()
                if not should_continue:
                    arcade.stop_render()
                    return False  # Stop the loop
            except Exception as e:
                print(f"Error in draw phase: {e}")
        
        return True
    
    def set_update_callback(self, callback: Callable[[float], None]) -> None:
        """
        Set the update callback for game logic.
        
        Args:
            callback: Function that takes delta_time as argument
            
        Example:
            >>> def my_update(dt):
            ...     print(f"Update at {dt:.3f}s")
            >>> loop.set_update_callback(my_update)
        """
        self.update_callback = callback
    
    def set_draw_callback(self, callback: Callable[[], bool]) -> None:
        """
        Set the draw callback for rendering.
        
        Args:
            callback: Function that returns True to continue, False to stop
            
        Example:
            >>> def my_draw():
            ...     arcade.draw_rectangle_filled(0, 0, 100, 100, arcade.color.RED)
            ...     return self.running
            >>> loop.set_draw_callback(my_draw)
        """
        self.draw_callback = callback
    
    def get_fps(self) -> int:
        """Get the current frame rate."""
        return int(self.current_fps)
    
    def set_window(self, window: arcade.Window) -> None:
        """Set the Arcade window to use for rendering."""
        self.window = window


def create_game_loop(fps_target: int = 60) -> GameLoop:
    """
    Factory function to create a game loop.
    
    Args:
        fps_target: Target frames per second (default: 60)
        
    Returns:
        Configured GameLoop instance
        
    Example:
        >>> loop = create_game_loop()
        >>> loop.start()
    """
    return GameLoop(fps_target=fps_target)


# Example usage (for testing purposes)
if __name__ == "__main__":
    import arcade
    
    print("Testing Game Loop Module...")
    
    # Create window first
    window = arcade.Window(
        width=800,
        height=600,
        title="Game Loop Test"
    )
    
    # Create game loop
    loop = create_game_loop(fps_target=30)  # Lower FPS for testing
    
    # Set up callbacks
    def update(delta_time: float):
        """Update phase - game logic."""
        print(f"[UPDATE] Delta time: {delta_time:.3f}s, FPS: {loop.get_fps()}")
        
        # Simulate some game logic here
        # e.g., player movement, physics updates, etc.
    
    def draw() -> bool:
        """Draw phase - rendering."""
        arcade.start_render()
        arcade.draw_rectangle_filled(0, 0, 400, 300, arcade.color.DARK_SLATE_GRAY)
        arcade.draw_text("Game Loop Test", 150, 280, 
                        arcade.color.WHITE, 24, anchor_x="center")
        arcade.draw_text(f"FPS: {loop.get_fps()}", 400, 300,
                        arcade.color.YELLOW, 16, anchor_x="left")
        
        # Check if window is still open
        return not window.is_closing
    
    loop.set_window(window)
    loop.set_update_callback(update)
    loop.set_draw_callback(draw)
    
    try:
        print("Starting game loop... Press ESC to exit.")
        loop.start()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        window.close()
