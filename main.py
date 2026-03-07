"""
Main Entry Point - 2D Racing Game Demo

This module initializes and runs the complete racing game,
integrating all systems: window, loop, physics, tracks, UI, etc.
"""

import arcade
from typing import Optional, Tuple

# Import game modules
from game.core.game_window import GameWindow
from game.core.game_loop import GameLoop
from game.core.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS,
    CAR_WIDTH, CAR_HEIGHT, MAX_SPEED, ACCELERATION, BRAKING_POWER,
    TURNING_SENSITIVITY, FRICTION_COEFFICIENT, DRAG_FACTOR,
    BACKGROUND_COLOR, DEBUG_TOGGLE_KEY
)
from game.entities.car import Car
from game.systems.physics_system import PhysicsSystem
from game.systems.camera_system import CameraSystem
from game.systems.lap_system import LapSystem
from game.systems.collision_system import CollisionSystem
from game.components.input_component import InputHandler
from game.tracks.track_loader import TrackLoader, TrackData
from game.tracks.track_renderer import TrackRenderer
from game.ui.menu import MainMenu, create_main_menu
from game.ui.hud import HUD
from game.ui.debug_overlay import DebugOverlay


class RacingGame:
    """
    Main game class that orchestrates all game systems.
    
    This is the central controller that:
    - Manages game state (menu, playing, paused)
    - Coordinates all game systems
    - Handles input and updates
    - Renders each frame
    
    Architecture follows ECS-inspired pattern with separate systems.
    """
    
    def __init__(self):
        """Initialize the racing game."""
        # Game state
        self.state = "menu"  # menu, playing, paused
        self.running = False
        
        # Window and loop
        self.window: Optional[GameWindow] = None
        self.game_loop: Optional[GameLoop] = None
        
        # Physics and systems
        self.physics_system: Optional[PhysicsSystem] = None
        self.camera_system: Optional[CameraSystem] = None
        self.lap_system: Optional[LapSystem] = None
        self.collision_system: Optional[CollisionSystem] = None
        
        # Entities
        self.player_car: Optional[Car] = None
        self.track_data: Optional[TrackData] = None
        
        # Input and UI
        self.input_handler: Optional[InputHandler] = None
        self.menu: Optional[MainMenu] = None
        self.hud: Optional[HUD] = None
        self.debug_overlay: Optional[DebugOverlay] = None
        
        # Track renderer
        self.track_renderer: Optional[TrackRenderer] = None
        
        # Timing
        self.last_update_time = 0.0
        self.delta_time = 0.0
    
    def initialize(self) -> None:
        """Initialize all game systems."""
        print("Initializing Racing Game...")
        
        # Create window
        self.window = GameWindow()
        self.window.open_window()
        
        # Create game loop
        self.game_loop = GameLoop(fps_target=TARGET_FPS)
        
        # Initialize physics system
        self.physics_system = PhysicsSystem()
        
        # Initialize camera system
        self.camera_system = CameraSystem()
        
        # Initialize lap system
        self.lap_system = LapSystem()
        
        # Initialize collision system
        self.collision_system = CollisionSystem()
        
        # Create input handler
        self.input_handler = InputHandler()
        self.input_handler.setup_window(self.window)
        
        # Create track renderer
        self.track_renderer = TrackRenderer()
        
        # Create UI components
        self.menu = create_main_menu(
            tracks=['Oval Track', 'City Track', 'Desert Track'],
            on_start=self.start_game,
            on_exit=self.quit_game
        )
        self.hud = HUD()
        self.debug_overlay = DebugOverlay()
        
        # Create player car at start position
        self.player_car = Car(
            x=0, y=0,
            angle=90,  # Facing up
            color=arcade.color.RED
        )
        
        print("Game initialized successfully.")
    
    def start_game(self) -> None:
        """Start the game (from menu)."""
        self.state = "playing"
        self.running = True
        
        # Initialize track and lap system
        self._load_oval_track()
        
        # Reset player car
        self.player_car.reset()
        self.physics_system.reset()
        
        # Start first lap
        self.lap_system.start_lap()
        
        print("Game started!")
    
    def _load_oval_track(self) -> None:
        """Load the oval track configuration."""
        # Set track boundaries
        left = -200
        right = 800
        bottom = -150
        top = 450
        
        self.physics_system.set_track_bounds(left, right, bottom, top)
        self.collision_system.set_track_bounds(left, right, bottom, top)
        
        # Set track data
        self.track_data = TrackData(
            name="Oval Track",
            start_position=(0, 0),
            checkpoints=[
                {'id': 1, 'position': (200, 0)},
                {'id': 2, 'position': (400, 300)},
                {'id': 3, 'position': (600, 0)},
            ],
            boundaries={
                'left': left,
                'right': right,
                'bottom': bottom,
                'top': top
            },
            lap_length=1200,
            surface_color=(0.54, 0.81, 0.39),
            grass_color=(0.42, 0.67, 0.33)
        )
        
        # Initialize lap system with checkpoints
        self.lap_system.initialize_track(self.track_data.checkpoints)
        
        # Set camera viewport bounds
        self.camera_system.set_viewport_bounds(
            left=left - 100,
            right=right + 100,
            top=top + 100,
            bottom=bottom - 100
        )
    
    def quit_game(self) -> None:
        """Quit the game."""
        self.running = False
        self.state = "menu"
        
        if self.window:
            self.window.close_window()
        
        print("Game quit.")
    
    def update(self, delta_time: float) -> None:
        """
        Update game state for one frame.
        
        Args:
            delta_time: Time in seconds since last frame
        """
        if self.state != "playing":
            return
        
        # Get input state
        is_accelerating = self.input_handler.is_accelerating()
        is_braking = self.input_handler.is_braking()
        is_turning_left = self.input_handler.is_turning_left()
        is_turning_right = self.input_handler.is_turning_right()
        
        # Update physics
        velocity, angle = self.physics_system.update(
            velocity=self.player_car.get_velocity(),
            angle=self.player_car.get_angle(),
            is_accelerating=is_accelerating,
            is_braking=is_braking,
            is_turning_left=is_turning_left,
            is_turning_right=is_turning_right,
            delta_time=delta_time
        )
        
        # Update car with new physics values
        self.player_car.set_velocity(velocity)
        self.player_car.set_angle(angle)
        
        # Check collision with track boundaries
        if self.collision_system.check_track_collision(
            self.player_car.get_position(),
            CAR_WIDTH,
            CAR_HEIGHT
        ):
            # Handle collision - push back and reset lap
            print("Collision detected!")
            self.physics_system.apply_collision_shake()
            
            # Reset current lap
            self.lap_system.reset_lap()
        
        # Update camera to follow player
        self.camera_system.follow_player(
            self.player_car.get_position()[0],
            self.player_car.get_position()[1],
            delta_time
        )
        
        # Check checkpoint crossings
        crossed_checkpoint = self.lap_system.check_checkpoint_crossing(
            self.player_car.get_position()
        )
        if crossed_checkpoint is not None:
            self.debug_overlay.update_player_data(
                speed=self.player_car.get_speed_kmh(),
                checkpoint_index=crossed_checkpoint,
                lap_number=self.lap_system.lap_timer.lap_number
            )
        
        # Check if lap is complete
        if self.lap_system.is_lap_complete:
            print("Lap complete!")
            self.hud.draw_new_lap_message(
                self.window.width,
                self.window.height
            )
            
            # Record lap time
            lap_time = self.lap_system.get_current_lap_time()
            self.lap_system.record_completed_lap(lap_time)
            self.hud.update_lap_info(
                lap_number=self.lap_system.lap_timer.lap_number,
                lap_time=lap_time,
                best_lap_time=self.lap_system.get_best_lap_time()
            )
        
        # Update HUD
        self.hud.update_speed(self.player_car.get_speed_kmh())
        
        # Update debug overlay
        if self.debug_overlay.is_visible:
            self.debug_overlay.update_fps(self.game_loop.get_fps())
            self.debug_overlay.update_player_data(
                speed=self.player_car.get_speed_kmh(),
                checkpoint_index=crossed_checkpoint if crossed_checkpoint is not None else -1,
                lap_number=self.lap_system.lap_timer.lap_number
            )
        
        # Update camera shake
        self.camera_system.update_shake(delta_time)
    
    def draw(self) -> bool:
        """
        Render the current frame.
        
        Returns:
            True if should continue, False to stop
        """
        if self.state == "menu":
            # Draw menu
            self.menu.draw(self.window.width, self.window.height)
        else:
            # Clear screen
            self.window.clear_screen(BACKGROUND_COLOR)
            
            # Draw track
            if self.track_data:
                self.track_renderer.draw_track(self.track_data)
                
                # Draw start/finish line
                self.track_renderer.draw_start_finish_line(self.track_data, (0, 0))
            
            # Draw player car
            if self.player_car:
                self.player_car.draw()
            
            # Draw HUD
            if self.hud:
                self.hud.draw(self.window.width, self.window.height)
            
            # Draw debug overlay
            if self.debug_overlay and self.debug_overlay.is_visible:
                self.debug_overlay.draw(self.window.width, self.window.height)
        
        return self.running
    
    def handle_key_press(self, key: int) -> None:
        """Handle keyboard input."""
        # Menu navigation
        if self.state == "menu":
            if self.menu.handle_key_press(key):
                pass  # Menu handled the input
        
        # Debug toggle
        elif self.state == "playing":
            if key == arcade.key.F1:
                self.debug_overlay.toggle()
    
    def run(self) -> None:
        """Run the game loop."""
        try:
            # Initialize game
            self.initialize()
            
            # Start game loop
            self.game_loop.start()
            
        except Exception as e:
            print(f"Error running game: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Cleanup
            if self.window:
                self.window.close_window()


def main():
    """Main entry point."""
    game = RacingGame()
    game.run()


if __name__ == "__main__":
    main()
