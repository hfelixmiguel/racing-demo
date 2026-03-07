"""
Track Loader - Load and Manage Tracks from JSON

This module handles loading track configurations from JSON files,
validating the data structure, and providing access to track information.
"""

import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class TrackData:
    """
    Represents a loaded track with all its configuration data.
    
    Attributes:
        name: Display name of the track
        start_position: Starting (x, y) coordinates
        checkpoints: List of checkpoint positions and order
        boundaries: Track boundary coordinates
        lap_length: Expected lap length in pixels
        surface_color: Color for track surface
        grass_color: Color for surrounding area
    """
    
    def __init__(
        self,
        name: str,
        start_position: Tuple[float, float],
        checkpoints: List[Dict],
        boundaries: Dict[str, float],
        lap_length: float,
        surface_color: Tuple[int, int, int],
        grass_color: Tuple[int, int, int]
    ):
        """Initialize track data."""
        self.name = name
        self.start_position = start_position
        self.checkpoints = checkpoints
        self.boundaries = boundaries
        self.lap_length = lap_length
        self.surface_color = surface_color
        self.grass_color = grass_color
    
    @property
    def left(self) -> float:
        """Get left boundary."""
        return self.boundaries.get('left', 0)
    
    @property
    def right(self) -> float:
        """Get right boundary."""
        return self.boundaries.get('right', 0)
    
    @property
    def bottom(self) -> float:
        """Get bottom boundary."""
        return self.boundaries.get('bottom', 0)
    
    @property
    def top(self) -> float:
        """Get top boundary."""
        return self.boundaries.get('top', 0)


class TrackLoader:
    """
    Loads and manages track configurations from JSON files.
    
    Features:
    - JSON parsing and validation
    - Multiple track support
    - Default track definitions
    - Error handling for invalid tracks
    
    Tracks are defined in the 'tracks/' directory with JSON configuration.
    """
    
    # Default track definitions (used if no JSON file found)
    DEFAULT_TRACKS = {
        'oval_track': TrackData(
            name="Oval Track",
            start_position=(0, 0),
            checkpoints=[
                {'id': 1, 'position': (200, 0)},
                {'id': 2, 'position': (400, 300)},
                {'id': 3, 'position': (200, 600)},
            ],
            boundaries={
                'left': -100,
                'right': 1000,
                'bottom': -100,
                'top': 700
            },
            lap_length=1200,
            surface_color=(0.54, 0.81, 0.39),
            grass_color=(0.42, 0.67, 0.33)
        ),
        'city_track': TrackData(
            name="City Track",
            start_position=(0, 0),
            checkpoints=[
                {'id': 1, 'position': (150, 150)},
                {'id': 2, 'position': (350, 450)},
                {'id': 3, 'position': (650, 350)},
                {'id': 4, 'position': (850, 150)},
            ],
            boundaries={
                'left': -50,
                'right': 900,
                'bottom': -50,
                'top': 750
            },
            lap_length=2000,
            surface_color=(0.6, 0.75, 0.5),
            grass_color=(0.35, 0.55, 0.25)
        ),
        'desert_track': TrackData(
            name="Desert Track",
            start_position=(0, 0),
            checkpoints=[
                {'id': 1, 'position': (100, 200)},
                {'id': 2, 'position': (300, 500)},
                {'id': 3, 'position': (600, 400)},
                {'id': 4, 'position': (800, 100)},
            ],
            boundaries={
                'left': -100,
                'right': 950,
                'bottom': -100,
                'top': 700
            },
            lap_length=2400,
            surface_color=(0.8, 0.7, 0.5),
            grass_color=(0.6, 0.5, 0.3)
        ),
    }
    
    def __init__(self, tracks_directory: str = 'tracks'):
        """
        Initialize the track loader.
        
        Args:
            tracks_directory: Path to directory containing track JSON files
        """
        self.tracks_directory = Path(tracks_directory)
        self.loaded_tracks: Dict[str, TrackData] = {}
        self._load_default_tracks()
    
    def _load_default_tracks(self) -> None:
        """Load default track definitions."""
        for track_name, track_data in self.DEFAULT_TRACKS.items():
            self.loaded_tracks[track_name] = track_data
    
    def load_track_from_file(
        self,
        track_name: str,
        file_path: Optional[str] = None
    ) -> Optional[TrackData]:
        """
        Load a track from a JSON file.
        
        Args:
            track_name: Name of the track to load
            file_path: Optional custom path (uses default if not provided)
            
        Returns:
            TrackData instance or None if loading failed
        """
        if file_path is None:
            file_path = self.tracks_directory / f"{track_name}.json"
        
        try:
            with open(file_path, 'r') as f:
                track_data = json.load(f)
            
            # Validate and create TrackData instance
            validated_track = self._validate_and_create_track(track_name, track_data)
            self.loaded_tracks[track_name] = validated_track
            
            return validated_track
            
        except FileNotFoundError:
            print(f"Track file not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in track file {file_path}: {e}")
            return None
        except Exception as e:
            print(f"Error loading track {track_name}: {e}")
            return None
    
    def _validate_and_create_track(
        self,
        track_name: str,
        data: Dict
    ) -> TrackData:
        """
        Validate track JSON structure and create TrackData instance.
        
        Args:
            track_name: Name of the track
            data: Parsed JSON data
            
        Returns:
            Validated TrackData instance
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Required fields
        required_fields = ['name', 'start_position', 'checkpoints', 'boundaries']
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Track '{track_name}' missing required field: {field}")
        
        # Validate start_position
        start_pos = data['start_position']
        if not isinstance(start_pos, (list, tuple)) or len(start_pos) != 2:
            raise ValueError("start_position must be a [x, y] tuple/list")
        
        # Validate checkpoints
        checkpoints = data['checkpoints']
        if not isinstance(checkpoints, list):
            raise ValueError("checkpoints must be a list")
        
        for i, cp in enumerate(checkpoints):
            if 'position' not in cp:
                raise ValueError(f"Checkpoint {i} missing 'position' field")
            pos = cp['position']
            if not isinstance(pos, (list, tuple)) or len(pos) != 2:
                raise ValueError(f"Checkpoint {i} position must be a [x, y] tuple/list")
        
        # Validate boundaries
        boundaries = data['boundaries']
        for side in ['left', 'right', 'bottom', 'top']:
            if side not in boundaries:
                raise ValueError(f"Track '{track_name}' missing boundary: {side}")
        
        # Create TrackData instance with defaults
        return TrackData(
            name=data.get('name', track_name),
            start_position=tuple(data['start_position']),
            checkpoints=checkpoints,
            boundaries=boundaries,
            lap_length=data.get('lap_length', 1000),
            surface_color=tuple(data.get('surface_color', (0.54, 0.81, 0.39))),
            grass_color=tuple(data.get('grass_color', (0.42, 0.67, 0.33)))
        )
    
    def get_available_tracks(self) -> List[str]:
        """
        Get list of available track names.
        
        Returns:
            List of track names that are loaded
        """
        return list(self.loaded_tracks.keys())
    
    def get_track(self, track_name: str) -> Optional[TrackData]:
        """
        Get a loaded track by name.
        
        Args:
            track_name: Name of the track
            
        Returns:
            TrackData instance or None if not found
        """
        return self.loaded_tracks.get(track_name)
    
    def get_all_tracks(self) -> Dict[str, TrackData]:
        """
        Get all loaded tracks.
        
        Returns:
            Dictionary mapping track names to TrackData instances
        """
        return self.loaded_tracks.copy()
    
    def list_tracks(self) -> List[Dict[str, any]]:
        """
        Get formatted list of available tracks for display.
        
        Returns:
            List of dictionaries with track info for UI display
        """
        tracks = []
        for name, data in self.loaded_tracks.items():
            tracks.append({
                'name': data.name,
                'start_position': data.start_position,
                'checkpoint_count': len(data.checkpoints),
                'boundaries': data.boundaries,
                'lap_length': data.lap_length,
            })
        return tracks


def load_track(
    track_name: str,
    file_path: Optional[str] = None,
    tracks_directory: str = 'tracks'
) -> Optional[TrackData]:
    """
    Convenience function to load a single track.
    
    Args:
        track_name: Name of the track
        file_path: Optional custom path
        tracks_directory: Directory containing track files
        
    Returns:
        TrackData instance or None if loading failed
    """
    loader = TrackLoader(tracks_directory)
    return loader.load_track_from_file(track_name, file_path)
