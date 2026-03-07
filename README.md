# 2D Racing Game Demo

A fully playable top-down 2D racing game built with Python Arcade engine, featuring physics-based car controls, multiple tracks, lap timing, and a complete game loop.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Arcade](https://img.shields.io/badge/Arcade-2.7+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

### Core Gameplay
- **Physics-based car controls** with acceleration, braking, and speed-dependent steering
- **Multiple tracks** - Select from different track layouts (Oval, City, Desert)
- **Lap timing system** with checkpoint tracking and best lap recording
- **Smooth camera follow** that centers on the player car
- **Realistic physics model** including friction, drag, and turning radius

### Controls
| Key | Action |
|-----|--------|
| W / ↑ | Accelerate forward |
| S / ↓ | Brake/Reverse |
| A / ← | Turn left (steering strength depends on speed) |
| D / → | Turn right (steering strength depends on speed) |
| F1 | Toggle debug overlay |

### User Interface
- **Main Menu** - Start race, select track, or exit game
- **HUD** - Displays lap number, current lap time, best lap time, and player speed
- **Debug Overlay** - Shows FPS, checkpoint index, and detailed stats (toggle with F1)

## Requirements

- Python 3.10 or higher
- arcade >= 2.7.0
- pytest >= 7.4.0 (for testing)
- pyinstaller >= 6.0.0 (for building executable)

## Installation

### Clone the repository
```bash
git clone https://github.com/hfelixmiguel/racing-demo.git
cd racing-demo
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the game
```bash
python main.py
```

## Building Executable

To create a standalone executable for distribution:

```bash
python build_executable.py
```

The executable will be created in `dist/racing_demo/` directory.

## Project Structure

```
racing-demo/
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── PRD.md                    # Product Requirements Document
├── PLAN.md                   # Development Plan
├── build_executable.py       # PyInstaller build script
├── game/                     # Game source code
│   ├── core/
│   │   ├── game_window.py    # Arcade window setup
│   │   ├── game_loop.py      # Main game loop
│   │   └── config.py         # Game configuration
│   ├── entities/
│   │   ├── car.py            # Player car entity
│   │   └── checkpoint.py     # Checkpoint marker
│   ├── components/
│   │   ├── transform.py      # Position and rotation
│   │   ├── velocity.py       # Velocity vector
│   │   └── input_component.py # Player input handling
│   ├── systems/
│   │   ├── physics_system.py # Car physics calculations
│   │   ├── collision_system.py # Collision detection
│   │   ├── lap_system.py     # Lap counting logic
│   │   ├── camera_system.py  # Camera follow system
│   │   └── ai_system.py      # AI opponent (advanced)
│   ├── tracks/
│   │   ├── track_loader.py   # Track data loading
│   │   └── track_renderer.py # Track visualization
│   ├── ui/
│   │   ├── menu.py           # Main menu system
│   │   ├── hud.py            # Heads-up display
│   │   └── debug_overlay.py  # Debug info overlay
│   └── assets/               # Game assets
├── tracks/                   # Track configuration files
│   ├── oval_track.json
│   ├── city_track.json
│   └── desert_track.json
├── tests/                    # Automated test suite
└── .github/
    └── workflows/
        └── ci.yml           # CI/CD pipeline
```

## Development Status

### Current Phase: Project Initialization ✅

- [x] Repository created
- [x] PRD.md written
- [x] PLAN.md created
- [x] requirements.txt configured
- [ ] Base game window implementation
- [ ] Physics system
- [ ] Track loading and rendering
- [ ] Lap counting system
- [ ] UI components (Menu, HUD, Debug)

### Planned Features

**Phase 1 - Core Gameplay** (In Progress)
- Basic car controls and physics
- Single track implementation
- Lap timing system
- Main menu and HUD

**Phase 2 - Advanced Features**
- Multiple tracks with different layouts
- AI opponent
- Procedural track generation
- Sound effects and music

**Phase 3 - Polish & Optimization**
- Particle effects (drifting, exhaust)
- Car customization
- Leaderboard system
- Performance optimization for 60 FPS

## Testing

Run the test suite:
```bash
pytest tests/
```

## CI/CD

The project includes a GitHub Actions workflow that automatically:
1. Installs dependencies
2. Runs pytest test suite
3. Validates Python imports
4. Attempts PyInstaller build

## License

MIT License - feel free to use this project for learning or as a starting point for your own games.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [Arcade](https://api.arcade.academy/) - The 2D game engine powering this project
- Python community for excellent documentation and support

---

**Built with ❤️ using Python Arcade Engine**