"""
Main Game Loop Controller

This module implements the core game loop that orchestrates all game systems,
handles frame timing, and coordinates updates between different components.
"""

import arcade
from typing import Callable, Optional
import time


class GameLoop:
    """
    Manages the main game loop with delta time handling.
    
    The game loop follows this pattern each frame:
    1. Calculate delta time since last frame
    2. Update all game systems with delta time
    3. Render the current frame
    4. Check for termination conditions
    
    Attributes:
        running: Flag to control loop execution
        fps_target: Target frames per second (default 60)
        dt_accumulator: Accumulator for fixed-time step updates
        last_frame_time: Timestamp of last frame
        update_callback: Function called each update cycle
        draw_callback: Function called each draw cycle
    """
    
    # Frame rate constants
    FPS_TARGET = 60
    DT_PER_FRAME = 1.0 / FPS_TARGET  # Delta time per frame in seconds
    
    def __init__(
        self,
        fps_target: int = FPS_TARGET,
        update_callback: Optional[Callable[[float], None]] = None,
        draw_callback: Optional[Callable[[], bool]] = None
    ):
        """
        Initialize the game loop.
        
        Args:
            fps_target: Target frames per second
            update_callback: Function to call each update (receives delta_time)
            draw_callback: Function to call each draw (returns True if continue)
        """
        self.running = False
        self.fps_target = fps_target
        self.dt_per_frame = 1.0 / fps_target
        
        # Callbacks for game logic and rendering
        self.update_callback = update_callback or self._default_update
        self.draw_callback = draw_callback or self._default_draw
        
        # Timing variables
        self.last_frame_time: float = time.time()
        self.dt_accumulator = 0.0
        
        # FPS tracking
        self.fps_count = 0
        self.fps_start_time = time.time()
    
    def start(self) -> None:
        """Start the game loop."""
        self.running = True
        self.last_frame_time = time.time()
        self._run_loop()
    
    def stop(self) -> None:
        """Stop the game loop."""
        self.running = False
    
    def _run_loop(self) -> None:
        """Main game loop implementation using while loop with timing control."""
        while self.running:
            # Get current time and calculate delta time
            current_time = time.time()
            dt = current_time - self.last_frame_time
            
            # Cap delta time to prevent huge jumps if game pauses
            dt = min(dt, 0.25)  # Maximum 250ms per frame
            
            self.last_frame_time = current_time
            self.dt_accumulator += dt
            
            # Update game systems with accumulated time
            self.update_callback(self.dt_accumulator)
            
            # Reset accumulator if we've exceeded one frame's worth of time
            if self.dt_accumulator >= self.dt_per_frame:
                self.dt_accumulator -= self.dt_per_frame
            
            # Render the current frame
            if not self.draw_callback():
                break  # Draw callback requested to stop
            
            # Sleep to maintain target FPS (if running too fast)
            elapsed = time.time() - current_time
            sleep_time = self.dt_per_frame - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        # Cleanup when loop ends
        self._cleanup()
    
    def _default_update(self, delta_time: float) -> None:
        """Default update function (can be overridden)."""
        pass
    
    def _default_draw(self) -> bool:
        """Default draw function (can be overridden)."""
        return True  # Continue running
    
    def _cleanup(self) -> None:
        """Clean up resources when loop ends."""
        self.running = False
        print(f"Game loop ended. Final FPS: {self.get_fps()}")
    
    def get_fps(self) -> int:
        """
        Calculate and return current frames per second.
        
        Returns:
            Current FPS as integer
        """
        current_time = time.time()
        elapsed = current_time - self.fps_start_time
        
        if elapsed <= 0:
            return 0
        
        self.fps_count += 1
        
        # Reset counter every second
        if elapsed >= 1.0:
            fps = int(self.fps_count / elapsed)
            self.fps_count = 0
            self.fps_start_time = current_time
            return fps
        
        return int(self.fps_count / elapsed)
    
    def set_fps_limit(self, fps: int) -> None:
        """
        Set the target FPS for the game loop.
        
        Args:
            fps: Target frames per second
        """
        self.fps_target = fps
        self.dt_per_frame = 1.0 / fps


class GameLoopManager:
    """
    Manages multiple game loops and coordinates their execution.
    
    This class allows running multiple independent game loops (e.g., 
    main game loop, UI animation loop) in a coordinated manner.
    """
    
    def __init__(self):
        """Initialize the game loop manager."""
        self.loops: dict[str, GameLoop] = {}
        self.main_loop: Optional[GameLoop] = None
    
    def create_loop(
        self,
        name: str,
        fps_target: int = 60,
        update_callback: Optional[Callable[[float], None]] = None,
        draw_callback: Optional[Callable[[], bool]] = None
    ) -> GameLoop:
        """
        Create and register a new game loop.
        
        Args:
            name: Unique identifier for the loop
            fps_target: Target FPS for this loop
            update_callback: Update function for this loop
            draw_callback: Draw function for this loop
            
        Returns:
            The created GameLoop instance
        """
        loop = GameLoop(
            fps_target=fps_target,
            update_callback=update_callback,
            draw_callback=draw_callback
        )
        self.loops[name] = loop
        
        if name == "main":
            self.main_loop = loop
        
        return loop
    
    def start_all(self) -> None:
        """Start all registered game loops."""
        for name, loop in self.loops.items():
            loop.start()
    
    def stop_all(self) -> None:
        """Stop all registered game loops."""
        for loop in self.loops.values():
            loop.stop()
    
    def get_loop(self, name: str) -> Optional[GameLoop]:
        """
        Get a specific game loop by name.
        
        Args:
            name: Name of the loop to retrieve
            
        Returns:
            GameLoop instance or None if not found
        """
        return self.loops.get(name)


def create_main_game_loop(
    update_callback: Optional[Callable[[float], None]] = None,
    draw_callback: Optional[Callable[[], bool]] = None
) -> GameLoop:
    """
    Factory function to create the main game loop.
    
    Args:
        update_callback: Function called each update cycle
        draw_callback: Function called each draw cycle
        
    Returns:
        Configured GameLoop instance ready to start
    """
    loop = GameLoop(
        fps_target=GameLoop.FPS_TARGET,
        update_callback=update_callback,
        draw_callback=draw_callback
    )
    loop.start()
    return loop
