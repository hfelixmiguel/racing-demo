"""
Game Configuration Constants

This module contains all configurable constants for the racing game.
Changing values here affects game behavior without modifying code logic.
"""

# =============================================================================
# WINDOW & DISPLAY CONFIGURATION
# =============================================================================

# Screen dimensions (pixels)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Window title
WINDOW_TITLE = "2D Racing Game Demo"

# Target frame rate
TARGET_FPS = 60

# Background color (RGB tuple, arcade.color names also available)
BACKGROUND_COLOR = (0.54, 0.81, 0.39)  # Lawn green


# =============================================================================
# PLAYER CAR PHYSICS CONFIGURATION
# =============================================================================

# Maximum speed (pixels per second)
MAX_SPEED = 300.0

# Acceleration rate (pixels per second squared)
ACCELERATION = 150.0

# Braking power (pixels per second squared)
BRAKING_POWER = 400.0

# Turning radius at full speed (pixels)
TURNING_RADIUS_FULL_SPEED = 80.0

# Steering sensitivity factor
STEERING_SENSITIVITY = 0.02

# Friction coefficient (velocity decay when not accelerating)
FRICTION_COEFFICIENT = 0.95

# Air drag factor
DRAG_FACTOR = 0.1


# =============================================================================
# TRACK CONFIGURATION
# =============================================================================

# Track surface colors
TRACK_GRASS_COLOR = (0.42, 0.67, 0.33)   # Darker grass
TRACK_ROAD_COLOR = (0.54, 0.81, 0.39)    # Lighter road
TRACK_BORDER_COLOR = (0.85, 0.85, 0.85)  # White border

# Track boundary padding (pixels from edge)
TRACK_PADDING = 50

# Checkpoint radius (pixels)
CHECKPOINT_RADIUS = 15

# Checkpoint color
CHECKPOINT_COLOR = (1.0, 0.8, 0.0)  # Yellow


# =============================================================================
# LAP SYSTEM CONFIGURATION
# =============================================================================

# Lap timer precision (milliseconds)
LAP_TIMER_PRECISION = 3

# Best lap time display format
BEST_LAP_DISPLAY_FORMAT = "Best: {:d}.{:02d}s"

# Lap completion message delay (seconds)
LAP_COMPLETION_DELAY = 1.5


# =============================================================================
# CAMERA CONFIGURATION
# =============================================================================

# Camera follow smoothness (0.0-1.0, higher = faster response)
CAMERA_SMOOTHING = 0.1

# Camera shake intensity on collision
COLLISION_SHAKE_INTENSITY = 5.0

# Camera shake duration (seconds)
COLLISION_SHAKE_DURATION = 0.3


# =============================================================================
# UI & HUD CONFIGURATION
# =============================================================================

# HUD font size
HUD_FONT_SIZE = 24

# Speed display units (pixels/sec or km/h)
SPEED_UNITS = "km/h"  # Options: "pixels/sec", "km/h"

# Speed conversion factor (pixels/sec to km/h)
PIXELS_TO_KMH_FACTOR = 0.36

# Debug overlay font size
DEBUG_FONT_SIZE = 18


# =============================================================================
# INPUT CONFIGURATION
# =============================================================================

# Acceleration key bindings
ACCELERATE_KEYS = ["w", "W", "up"]

# Braking key bindings
BRAKE_KEYS = ["s", "S", "down"]

# Left turn key bindings
LEFT_TURN_KEYS = ["a", "A", "left"]

# Right turn key bindings
RIGHT_TURN_KEYS = ["d", "D", "right"]

# Debug toggle key
DEBUG_TOGGLE_KEY = "f1"


# =============================================================================
# PERFORMANCE CONFIGURATION
# =============================================================================

# Minimum acceptable FPS (warning threshold)
MIN_FPS_WARNING = 45

# Maximum delta time cap (seconds) to prevent huge jumps
MAX_DELTA_TIME = 0.25

# Physics sub-steps per frame (for smoother physics)
PHYSICS_SUB_STEPS = 4


# =============================================================================
# ASSET CONFIGURATION
# =============================================================================

# Car dimensions (pixels)
CAR_WIDTH = 30
CAR_HEIGHT = 50

# Wheel dimensions (pixels)
WHEEL_RADIUS = 8

# Checkpoint spacing minimum (pixels)
CHECKPOINT_MIN_SPACING = 200


# =============================================================================
# GAMEPLAY CONFIGURATION
# =============================================================================

# Starting lap time bonus (milliseconds)
STARTING_LAP_TIME_BONUS = 5000  # 5 seconds

# Lap completion message duration (seconds)
LAP_MESSAGE_DURATION = 3.0

# Collision penalty (lap reset or time penalty)
COLLISION_PENALTY = "reset_lap"  # Options: "reset_lap", "time_penalty"


# =============================================================================
# DEBUG CONFIGURATION
# =============================================================================

# Enable debug logging
DEBUG_LOGGING = False

# Show checkpoint indices in debug mode
SHOW_CHECKPOINT_INDICES = True

# Show physics values in debug mode
SHOW_PHYSICS_VALUES = True
