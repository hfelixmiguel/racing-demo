"""
Input Component - Player Input Handling

This module handles all player input from keyboard, providing a clean interface
for the game systems to respond to player actions.
"""

import arcade
from typing import Dict, List, Optional, Set


class InputComponent:
    """
    Manages all player input from keyboard.
    
    Features:
    - Keyboard state tracking
    - Multiple key bindings support
    - Input debouncing
    - Clean interface for game systems
    
    Provides a centralized input system that can be queried by any game component.
    """
    
    def __init__(self):
        """Initialize the input component."""
        # Key binding configurations
        self.key_bindings: Dict[str, List[str]] = {
            'accelerate': ['w', 'W', 'up'],
            'brake': ['s', 'S', 'down'],
            'turn_left': ['a', 'A', 'left'],
            'turn_right': ['d', 'D', 'right'],
            'debug_toggle': ['f1'],
        }
        
        # Current key states (pressed/released)
        self.pressed_keys: Set[str] = set()
        self.released_keys: Set[str] = set()
        
        # Input history for smooth controls
        self.input_history: List[Dict[str, bool]] = []
        self.max_history = 10
    
    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Handle key press event.
        
        Args:
            key: Arcade key code
            key_modifiers: Key modifiers (shift, ctrl, alt)
        """
        # Get key name from code
        key_name = arcade.key.key_names.get(key, str(key))
        
        self.pressed_keys.add(key_name)
        self.released_keys.discard(key_name)
        
        self._record_input(True)
    
    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """
        Handle key release event.
        
        Args:
            key: Arcade key code
            key_modifiers: Key modifiers
        """
        key_name = arcade.key.key_names.get(key, str(key))
        
        self.released_keys.add(key_name)
        self.pressed_keys.discard(key_name)
        
        self._record_input(False)
    
    def _record_input(self, is_pressed: bool) -> None:
        """Record input for history."""
        input_state = {key: is_pressed for key in self.key_bindings.keys()}
        self.input_history.append(input_state)
        
        # Keep only recent inputs
        if len(self.input_history) > self.max_history:
            self.input_history.pop(0)
    
    def get_action_state(self, action: str) -> bool:
        """
        Get whether an action is currently active.
        
        Args:
            action: Name of the action (accelerate, brake, turn_left, etc.)
            
        Returns:
            True if action is active, False otherwise
        """
        if action not in self.key_bindings:
            return False
        
        # Check if any bound key is pressed
        for key in self.key_bindings[action]:
            if key in self.pressed_keys:
                return True
        
        return False
    
    def get_action_state_history(self, action: str, frames: int = 3) -> bool:
        """
        Get action state from input history (for smooth controls).
        
        Args:
            action: Name of the action
            frames: Number of frames to check in history
            
        Returns:
            True if action was active recently, False otherwise
        """
        if not self.input_history:
            return False
        
        # Check recent history
        for i in range(min(frames, len(self.input_history))):
            if self.input_history[-(i+1)].get(action, False):
                return True
        
        return False
    
    def get_all_actions(self) -> Dict[str, bool]:
        """
        Get state of all actions.
        
        Returns:
            Dictionary mapping action names to their current state
        """
        return {action: self.get_action_state(action) for action in self.key_bindings.keys()}
    
    def reset(self) -> None:
        """Reset input state."""
        self.pressed_keys = set()
        self.released_keys = set()
        self.input_history = []


class InputHandler:
    """
    Higher-level input handler with additional features.
    
    Features:
    - Action smoothing
    - Input validation
    - Custom key bindings
    """
    
    def __init__(self):
        """Initialize the input handler."""
        self.input_component = InputComponent()
        
        # Action smoothing parameters
        self.action_threshold = 0.5  # Minimum frames for action to trigger
        self.smoothing_enabled = True
    
    def setup_window(self, window: arcade.Window) -> None:
        """
        Connect input handler to window events.
        
        Args:
            window: Arcade window instance
        """
        window.push_event_handler(window.key_press, self.input_component.on_key_press)
        window.push_event_handler(window.key_release, self.input_component.on_key_release)
    
    def get_input_state(self) -> Dict[str, bool]:
        """Get current input state."""
        return self.input_component.get_all_actions()
    
    def is_accelerating(self) -> bool:
        """Check if player is accelerating."""
        return self.input_component.get_action_state('accelerate')
    
    def is_braking(self) -> bool:
        """Check if player is braking."""
        return self.input_component.get_action_state('brake')
    
    def is_turning_left(self) -> bool:
        """Check if player is turning left."""
        return self.input_component.get_action_state('turn_left')
    
    def is_turning_right(self) -> bool:
        """Check if player is turning right."""
        return self.input_component.get_action_state('turn_right')
    
    def is_debug_mode_requested(self) -> bool:
        """Check if debug mode toggle was pressed."""
        return self.input_component.get_action_state('debug_toggle')


def create_input_handler() -> InputHandler:
    """
    Factory function to create input handler.
    
    Returns:
        Configured InputHandler instance
    """
    return InputHandler()
