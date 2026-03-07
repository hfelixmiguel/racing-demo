"""
Menu System - Main Game Menu

This module implements the main menu system with track selection,
start race, and exit options.
"""

import arcade
from typing import Optional, Callable, Dict, List


class MainMenu:
    """
    Manages the main game menu interface.
    
    Features:
    - Track selection
    - Start race option
    - Exit game option
    - Menu navigation with keyboard
    
    Uses simple text-based UI for compatibility and performance.
    """
    
    def __init__(self):
        """Initialize the main menu."""
        self.selected_option = 0  # 0=Start, 1=Select Track, 2=Exit
        self.tracks: List[str] = []
        
        # Menu text
        self.menu_title = "2D Racing Game"
        self.menu_options = [
            "Start Race",
            "Select Track",
            "Exit Game"
        ]
        
        # Display state
        self.is_visible = True
        self.show_track_selection = False
        
        # Callbacks
        self.on_start_callback: Optional[Callable] = None
        self.on_exit_callback: Optional[Callable] = None
        self.on_track_select_callback: Optional[Callable[[str], None]] = None
    
    def set_tracks(self, track_names: List[str]) -> None:
        """Set available tracks for selection."""
        self.tracks = track_names
    
    def show_start_race(self) -> None:
        """Handle Start Race option."""
        if self.on_start_callback:
            self.on_start_callback()
    
    def show_select_track(self) -> None:
        """Show track selection submenu."""
        self.show_track_selection = True
    
    def select_track(self, track_name: str) -> None:
        """Select a track and return to main menu."""
        if self.on_track_select_callback:
            self.on_track_select_callback(track_name)
        
        self.show_track_selection = False
        self.selected_option = 0
    
    def show_exit_game(self) -> None:
        """Handle Exit Game option."""
        if self.on_exit_callback:
            self.on_exit_callback()
    
    def handle_key_press(self, key: int) -> bool:
        """
        Handle menu navigation with keyboard.
        
        Args:
            key: Arcade key code
            
        Returns:
            True if a menu action was triggered, False otherwise
        """
        if not self.is_visible:
            return False
        
        # Arrow keys for navigation
        if key == arcade.key.UP or key == arcade.key.W:
            self.selected_option = max(0, self.selected_option - 1)
            return True
        
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.selected_option = min(len(self.menu_options) - 1, self.selected_option + 1)
            return True
        
        # Enter to confirm selection
        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            if not self.show_track_selection:
                # Main menu action
                if self.selected_option == 0 and self.on_start_callback:
                    self.on_start_callback()
                elif self.selected_option == 1:
                    self.show_select_track()
                elif self.selected_option == 2 and self.on_exit_callback:
                    self.on_exit_callback()
            else:
                # Track selection action
                if self.tracks and self.on_track_select_callback:
                    selected_track = self.tracks[self.selected_option]
                    self.on_track_select_callback(selected_track)
                    self.show_track_selection = False
        
        return True
    
    def draw(self, width: int, height: int) -> None:
        """
        Draw the menu to screen.
        
        Args:
            width: Screen width
            height: Screen height
        """
        # Center position
        center_x = width / 2
        center_y = height / 2
        
        # Draw title
        arcade.draw_text(
            self.menu_title,
            center_x,
            center_y + 100,
            font_name=arcade.FONT_NAME_NORMAL,
            font_size=48,
            anchor_x="center",
            color=arcade.color.WHITE
        )
        
        # Draw options
        y_offset = center_y - 20
        for i, option in enumerate(self.menu_options):
            if self.show_track_selection:
                # Show track names instead
                if i < len(self.tracks):
                    text = f"  {self.tracks[i]}"
                else:
                    text = "  "
            else:
                text = f"  {option}"
            
            # Highlight selected option
            if i == self.selected_option:
                arcade.draw_text(
                    text,
                    center_x,
                    y_offset,
                    font_name=arcade.FONT_NAME_NORMAL,
                    font_size=28,
                    anchor_x="center",
                    color=arcade.color.YELLOW
                )
            else:
                arcade.draw_text(
                    text,
                    center_x,
                    y_offset,
                    font_name=arcade.FONT_NAME_NORMAL,
                    font_size=28,
                    anchor_x="center",
                    color=arcade.color.WHITE
                )
            
            y_offset -= 40
        
        # Draw instructions
        arcade.draw_text(
            "Use UP/DOWN to navigate, ENTER to select",
            center_x,
            y_offset - 20,
            font_name=arcade.FONT_NAME_NORMAL,
            font_size=16,
            anchor_x="center",
            color=arcade.color.GRAY
        )


class TrackSelector:
    """
    Manages track selection interface.
    
    Features:
    - Display available tracks
    - Highlight selected track
    - Confirm/cancel selection
    """
    
    def __init__(self):
        """Initialize the track selector."""
        self.selected_track_index = 0
        self.tracks: List[str] = []
        self.is_visible = False
    
    def set_tracks(self, track_names: List[str]) -> None:
        """Set available tracks."""
        self.tracks = track_names
        if not self.tracks:
            self.is_visible = False
        else:
            self.selected_track_index = 0
            self.is_visible = True
    
    def handle_key_press(self, key: int) -> bool:
        """Handle navigation and selection."""
        if not self.is_visible or not self.tracks:
            return False
        
        if key == arcade.key.UP or key == arcade.key.W:
            self.selected_track_index = max(0, self.selected_track_index - 1)
            return True
        
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.selected_track_index = min(len(self.tracks) - 1, self.selected_track_index + 1)
            return True
        
        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            return True  # Confirm selection
        
        return False
    
    def draw(self, width: int, height: int) -> None:
        """Draw the track selector."""
        center_x = width / 2
        center_y = height / 2
        
        # Title
        arcade.draw_text(
            "Select Track",
            center_x,
            center_y + 80,
            font_name=arcade.FONT_NAME_NORMAL,
            font_size=36,
            anchor_x="center",
            color=arcade.color.WHITE
        )
        
        # Track options
        y_offset = center_y - 20
        for i, track in enumerate(self.tracks):
            if i == self.selected_track_index:
                arcade.draw_text(
                    f"  * {track}",
                    center_x,
                    y_offset,
                    font_name=arcade.FONT_NAME_NORMAL,
                    font_size=28,
                    anchor_x="center",
                    color=arcade.color.YELLOW
                )
            else:
                arcade.draw_text(
                    f"    {track}",
                    center_x,
                    y_offset,
                    font_name=arcade.FONT_NAME_NORMAL,
                    font_size=28,
                    anchor_x="center",
                    color=arcade.color.WHITE
                )
            
            y_offset -= 40
        
        # Instructions
        arcade.draw_text(
            "Use UP/DOWN to navigate, ENTER to confirm",
            center_x,
            y_offset - 20,
            font_name=arcade.FONT_NAME_NORMAL,
            font_size=16,
            anchor_x="center",
            color=arcade.color.GRAY
        )


def create_main_menu(
    tracks: List[str],
    on_start: Optional[Callable] = None,
    on_exit: Optional[Callable] = None,
    on_track_select: Optional[Callable[[str], None]] = None
) -> MainMenu:
    """
    Factory function to create a main menu.
    
    Args:
        tracks: List of available track names
        on_start: Callback when Start Race is selected
        on_exit: Callback when Exit Game is selected
        on_track_select: Callback when a track is selected
        
    Returns:
        Configured MainMenu instance
    """
    menu = MainMenu()
    menu.set_tracks(tracks)
    menu.on_start_callback = on_start
    menu.on_exit_callback = on_exit
    menu.on_track_select_callback = on_track_select
    
    return menu
