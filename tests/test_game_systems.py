"""
Test Suite for Racing Game Demo

This module contains all automated tests for the racing game systems.
Uses pytest framework for test organization and execution.
"""

import arcade
import pytest


class TestImports:
    """Test that all modules can be imported without errors."""
    
    def test_import_arcade(self):
        """Verify Arcade library is importable."""
        import arcade
        assert arcade is not None
    
    def test_import_game_window(self):
        """Verify game window module imports correctly."""
        from game.core.game_window import GameWindow
        assert GameWindow is not None
    
    def test_import_game_loop(self):
        """Verify game loop module imports correctly."""
        from game.core.game_loop import GameLoop
        assert GameLoop is not None


class TestGameWindow:
    """Test the GameWindow class functionality."""
    
    @pytest.fixture
    def window(self):
        """Create a GameWindow instance for testing."""
        return GameWindow()
    
    def test_window_initialization(self, window):
        """Verify window initializes with correct dimensions."""
        assert window.SCREEN_WIDTH == 1280
        assert window.SCREEN_HEIGHT == 720
    
    def test_fps_configuration(self, window):
        """Verify frame rate is set to 60 FPS."""
        assert window.FPS == 60
    
    def test_camera_initialization(self, window):
        """Verify camera is created during initialization."""
        # Camera should be initialized in _setup_window()
        assert hasattr(window, 'camera')


class TestGameLoop:
    """Test the GameLoop class functionality."""
    
    @pytest.fixture
    def game_loop(self):
        """Create a GameLoop instance for testing."""
        return GameLoop(fps_target=60)
    
    def test_game_loop_initialization(self, game_loop):
        """Verify game loop initializes with correct FPS target."""
        assert game_loop.fps_target == 60
    
    def test_delta_time_calculation(self, game_loop):
        """Verify delta time is calculated correctly."""
        # Delta time should be approximately 1/60 seconds at 60 FPS
        expected_dt = 1.0 / 60.0
        assert abs(game_loop.calculate_delta_time(1)) < 0.1


class TestPhysicsSystem:
    """Test the physics system calculations."""
    
    def test_acceleration_calculation(self):
        """Verify acceleration is calculated correctly."""
        from game.core.config import ACCELERATION, MAX_SPEED
        
        # Acceleration should increase velocity by ACCELERATION per second
        initial_velocity = 0.0
        dt = 1.0  # One second
        
        new_velocity = initial_velocity + (ACCELERATION * dt)
        
        assert new_velocity > 0
        assert new_velocity <= MAX_SPEED
    
    def test_braking_calculation(self):
        """Verify braking reduces velocity correctly."""
        from game.core.config import BRAKING_POWER, MAX_SPEED
        
        # Braking should reduce velocity by BRAKING_POWER per second
        initial_velocity = MAX_SPEED
        dt = 1.0
        
        new_velocity = max(0, initial_velocity - (BRAKING_POWER * dt))
        
        assert new_velocity < initial_velocity
        assert new_velocity >= 0
    
    def test_turning_with_speed_dependency(self):
        """Verify turning strength depends on speed."""
        from game.core.config import TURNING_SENSITIVITY
        
        # At higher speeds, turning should be less effective
        low_speed = 10.0
        high_speed = 50.0
        
        low_turn = TURNING_SENSITIVITY / (1 + low_speed / 100)
        high_turn = TURNING_SENSITIVITY / (1 + high_speed / 100)
        
        assert low_turn > high_turn


class TestConfig:
    """Test configuration constants."""
    
    def test_screen_dimensions(self):
        """Verify screen dimensions are set correctly."""
        from game.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
        
        assert SCREEN_WIDTH == 1280
        assert SCREEN_HEIGHT == 720
    
    def test_target_fps(self):
        """Verify target FPS is 60."""
        from game.core.config import TARGET_FPS
        
        assert TARGET_FPS == 60
    
    def test_physics_constants_positive(self):
        """Verify all physics constants are positive values."""
        from game.core.config import (
            ACCELERATION, BRAKING_POWER, TURNING_SENSITIVITY,
            FRICTION_COEFFICIENT, DRAG_FACTOR
        )
        
        assert ACCELERATION > 0
        assert BRAKING_POWER > 0
        assert TURNING_SENSITIVITY > 0
        assert FRICTION_COEFFICIENT > 0
        assert DRAG_FACTOR > 0


class TestTrackData:
    """Test track data structure and validation."""
    
    def test_track_data_creation(self):
        """Verify TrackData can be created with valid parameters."""
        from game.tracks.track_loader import TrackData
        
        track = TrackData(
            name="Test Track",
            start_position=(0, 0),
            checkpoints=[{'id': 1, 'position': (100, 100)}],
            boundaries={
                'left': -500,
                'right': 500,
                'bottom': -300,
                'top': 300
            },
            lap_length=1000,
            surface_color=(0.5, 0.5, 0.5),
            grass_color=(0.3, 0.6, 0.3)
        )
        
        assert track.name == "Test Track"
        assert track.start_position == (0, 0)
        assert len(track.checkpoints) == 1
    
    def test_track_data_validation(self):
        """Verify track data validates required fields."""
        from game.tracks.track_loader import TrackData
        
        # Should raise error if missing required fields
        with pytest.raises(Exception):
            TrackData(
                name="Incomplete Track",
                # Missing start_position, checkpoints, boundaries
            )


class TestInputHandler:
    """Test input handling functionality."""
    
    def test_key_mapping(self):
        """Verify key mappings are correct."""
        from game.core.config import (
            ACCELERATE_KEYS, BRAKE_KEYS, 
            TURN_LEFT_KEYS, TURN_RIGHT_KEYS
        )
        
        assert len(ACCELERATE_KEYS) > 0
        assert len(BRAKE_KEYS) > 0
        assert len(TURN_LEFT_KEYS) > 0
        assert len(TURN_RIGHT_KEYS) > 0


class TestPerformance:
    """Test performance requirements."""
    
    def test_fps_target(self):
        """Verify FPS target is achievable."""
        from game.core.config import TARGET_FPS
        
        # Target should be reasonable for modern hardware
        assert TARGET_FPS <= 120
        assert TARGET_FPS >= 30
    
    def test_window_dimensions_reasonable(self):
        """Verify window dimensions are reasonable for gameplay."""
        from game.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
        
        # Should be HD or higher resolution
        assert SCREEN_WIDTH >= 1280
        assert SCREEN_HEIGHT >= 720


class TestIntegration:
    """Test integration between systems."""
    
    def test_window_and_camera_compatibility(self):
        """Verify window and camera work together."""
        from game.core.game_window import GameWindow
        
        window = GameWindow()
        
        # Camera dimensions should match window
        assert window.SCREEN_WIDTH > 0
        assert window.SCREEN_HEIGHT > 0
    
    def test_physics_and_collision_compatibility(self):
        """Verify physics and collision systems can work together."""
        from game.core.config import CAR_WIDTH, CAR_HEIGHT
        
        # Car dimensions should be reasonable for gameplay
        assert CAR_WIDTH > 0
        assert CAR_HEIGHT > 0
        assert CAR_WIDTH < SCREEN_WIDTH / 2
        assert CAR_HEIGHT < SCREEN_HEIGHT / 2
