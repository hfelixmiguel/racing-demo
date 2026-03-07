# Product Requirements Document - 2D Racing Game Demo

## Overview
A fully playable top-down 2D racing game built with Python Arcade engine, featuring multiple tracks, physics-based car controls, lap timing, and a complete game loop.

---

## Gameplay Mechanics

### Player Controls
- **W / Up Arrow**: Accelerate forward
- **S / Down Arrow**: Brake/Reverse
- **A / Left Arrow**: Turn left (steering strength depends on speed)
- **D / Right Arrow**: Turn right (steering strength depends on speed)

### Core Mechanics
1. **Acceleration System**
   - Gradual speed increase when accelerating
   - Maximum speed limit per track
   - Speed decay when not accelerating

2. **Braking System**
   - Immediate deceleration when braking
   - Shorter stopping distance at lower speeds

3. **Steering Physics**
   - Turning radius inversely proportional to speed
   - Higher speed = wider turning arc
   - Lower speed = tighter turns possible

4. **Collision Detection**
   - Track boundary collision detection
   - Collision triggers lap reset or penalty
   - Visual feedback on collision

5. **Lap System**
   - Checkpoint-based lap counting
   - Lap timer with milliseconds precision
   - Best lap time tracking
   - Lap completion notification

---

## Architecture

### Modular ECS-Inspired Structure

```
game/
├── main.py                    # Entry point, game initialization
├── game/
│   ├── core/
│   │   ├── game_window.py     # Arcade window setup and configuration
│   │   ├── game_loop.py       # Main game loop with delta time handling
│   │   └── config.py          # Global game configuration constants
│   ├── entities/
│   │   ├── car.py             # Player car entity with properties
│   │   └── checkpoint.py      # Checkpoint marker for lap counting
│   ├── components/
│   │   ├── transform.py       # Position and rotation component
│   │   ├── velocity.py        # Velocity vector component
│   │   └── input_component.py # Player input handling
│   ├── systems/
│   │   ├── physics_system.py  # Car physics calculations
│   │   ├── collision_system.py# Track boundary collision detection
│   │   ├── lap_system.py      # Lap counting and timing logic
│   │   ├── camera_system.py   # Camera following player
│   │   └── ai_system.py       # AI opponent behavior (advanced)
│   ├── tracks/
│   │   ├── track_loader.py    # Track data loading from JSON
│   │   └── track_renderer.py  # Track visualization rendering
│   ├── ui/
│   │   ├── menu.py            # Main menu system
│   │   ├── hud.py             # Heads-up display (lap, time, speed)
│   │   └── debug_overlay.py   # Debug info overlay (F1 toggle)
│   └── assets/                # Game assets directory
├── tracks/                    # Track configuration files
│   ├── oval_track.json
│   ├── city_track.json
│   └── desert_track.json
├── tests/                     # Automated test suite
└── requirements.txt           # Python dependencies
```

### Data Flow
1. **Input → Physics**: Player input affects velocity and rotation
2. **Physics → Transform**: Velocity updates position over time
3. **Transform → Camera**: Player position drives camera follow
4. **Camera → Render**: Camera view applied to all rendering
5. **Position → Collision**: Current position checked against boundaries
6. **Checkpoint → Lap**: Checkpoint crossing triggers lap completion

---

## Physics Model

### Car Physics Parameters
- **Max Speed**: 300 pixels/second (configurable per track)
- **Acceleration**: 150 pixels/second²
- **Braking Power**: 400 pixels/second²
- **Turning Radius**: 80 pixels at full speed
- **Friction Coefficient**: 0.95 (velocity decay when not accelerating)
- **Drag Factor**: 0.1 (air resistance)

### Physics Equations
```
velocity += acceleration * delta_time
position += velocity * delta_time
rotation += steering_angle * speed_factor * delta_time
velocity *= friction_coefficient
```

### Speed-Dependent Behavior
- Steering effectiveness: `steering_power = base_steering / (1 + speed/max_speed)`
- Acceleration efficiency: `effective_accel = acceleration * (1 - speed/max_speed)`

---

## Asset Strategy

### Initial Assets (Shapes)
- **Player Car**: Red rectangle with wheels (simple sprite)
- **AI Opponent**: Blue rectangle with wheels
- **Track Surface**: Green grass background
- **Track Boundaries**: White lines on track surface
- **Checkpoints**: Yellow circular markers
- **Start/Finish Line**: Black and white checkered pattern

### Future Assets
- Procedurally generated textures
- Sprite sheets for car animations
- Sound effects (engine, collision, lap complete)
- Background music

---

## Packaging Strategy

### PyInstaller Build
- **Output Directory**: `dist/racing_demo/`
- **Executable Name**: `racing_demo.exe` (Windows), `racing_demo` (Linux/Mac)
- **One-file mode**: Single executable with embedded resources
- **Excluded directories**: `__pycache__`, `.git`, `tests/`

### Build Script (`build_executable.py`)
```python
# PyInstaller configuration
--onefile
--windowed
--name racing_demo
--icon game/assets/icon.ico
--add-data "tracks;tracks"
--hidden-import arcade
```

---

## Performance Requirements

- **Target FPS**: 60 FPS
- **Minimum FPS Warning**: Log warning if below 45 FPS
- **Memory Usage**: < 100MB during gameplay
- **Asset Loading**: Preload all assets on startup

---

## Testing Strategy

### Unit Tests
- Physics calculations (acceleration, braking, turning)
- Collision detection accuracy
- Lap counting logic
- Checkpoint validation

### Integration Tests
- Full game loop execution
- Track loading and rendering
- Menu system transitions
- HUD updates during gameplay

### Performance Tests
- FPS consistency under load
- Memory leak detection
- Asset loading times

---

## Acceptance Criteria

1. ✅ Game launches without errors
2. ✅ Main menu displays with all options
3. ✅ Player can control car with WASD/Arrow keys
4. ✅ Car physics feel responsive and realistic
5. ✅ Track boundaries prevent off-track driving
6. ✅ Lap counting works correctly with checkpoints
7. ✅ HUD displays accurate lap time, speed, and lap number
8. ✅ Camera follows player smoothly
9. ✅ Multiple tracks selectable from menu
10. ✅ PyInstaller build produces working executable

---

## Technical Decisions

1. **Arcade Engine**: Chosen for 2D game development with built-in rendering and input handling
2. **ECS Pattern**: Modular architecture for maintainability and extensibility
3. **JSON Track Config**: Flexible track definition without code changes
4. **Delta Time**: Frame-rate independent physics calculations
5. **Shape-based Assets**: No external dependencies, simple to implement

---

## Future Enhancements (Post-MVP)

- [ ] Drifting mechanics with tire smoke particles
- [ ] Improved physics model with suspension simulation
- [ ] Sound effects and background music
- [ ] Particle effects (engine exhaust, sparks on collision)
- [ ] Enhanced AI with pathfinding
- [ ] Multiplayer support (local or online)
- [ ] Car customization (colors, upgrades)
- [ ] Leaderboard system
- [ ] Achievements and rewards
