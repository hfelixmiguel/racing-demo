# Development Plan - 2D Racing Game Demo

- github project: https://github.com/hfelixmiguel/racing-demo

## Current Status: Phase 1 - Project Initialization ✅

### Completed Tasks
- [x] Create GitHub repository
- [x] Write PRD.md (Product Requirements Document)
- [x] Initialize project structure planning
- [ ] Implement base Arcade game window
- [x] Create requirements.txt with dependencies
- [ ] Open first GitHub issue: Project Initialization

---

## Development Roadmap

### Phase 1: Project Foundation (Current)
**Goal**: Set up repository, documentation, and basic project structure

- [x] Initialize Python project
- [x] Configure Arcade engine setup
- [ ] Implement game window with proper configuration
- [x] Create requirements.txt with dependencies
- [ ] Open GitHub issue for Project Initialization
- [ ] Set up CI/CD pipeline (GitHub Actions)

**Estimated Completion**: After base game window implementation

---

### Phase 2: Core Game Loop & Window
**Goal**: Establish the foundation for all game systems

- [ ] Implement game_window.py with Arcade setup
  - Configure window size (1280x720)
  - Set up camera system
  - Handle window events (close, resize)
  - Implement frame rate control

- [ ] Implement game_loop.py
  - Main loop with delta time
  - Update and draw phases
  - FPS counter and throttling

**Estimated Completion**: After Phase 1

---

### Phase 3: Player Car & Physics
**Goal**: Create controllable player car with realistic physics

- [ ] Implement car entity (game/entities/car.py)
  - Position, rotation, velocity properties
  - Color and size configuration
  - Wheel rendering

- [ ] Implement physics system (game/systems/physics_system.py)
  - Acceleration and braking logic
  - Steering with speed-dependent turning
  - Friction and drag calculations
  - Velocity updates per frame

**Estimated Completion**: After Phase 2

---

### Phase 4: Track System
**Goal**: Load and render multiple tracks from JSON configuration

- [ ] Implement track loader (game/tracks/track_loader.py)
  - Parse JSON track definitions
  - Load track boundaries and checkpoints
  - Validate track data

- [ ] Create first track: Oval Track (tracks/oval_track.json)
  - Define start position
  - Set up checkpoint sequence
  - Configure track boundaries

- [ ] Implement track renderer (game/tracks/track_renderer.py)
  - Draw track surface
  - Render boundaries and checkpoints
  - Handle multiple tracks

**Estimated Completion**: After Phase 3

---

### Phase 5: Lap System & Checkpoints
**Goal**: Implement lap counting and timing mechanics

- [ ] Implement lap system (game/systems/lap_system.py)
  - Track checkpoint crossings
  - Count laps completed
  - Calculate lap times with milliseconds
  - Track best lap time

- [ ] Create checkpoint entity (game/entities/checkpoint.py)
  - Position and visual representation
  - Collision detection for checkpoint crossing

**Estimated Completion**: After Phase 4

---

### Phase 6: User Interface
**Goal**: Add menu system, HUD, and debug overlay

- [ ] Implement main menu (game/ui/menu.py)
  - Start Race option
  - Select Track option
  - Exit Game option
  - Track selection interface

- [ ] Implement HUD (game/ui/hud.py)
  - Display current lap number
  - Show current lap time
  - Display best lap time
  - Show player speed (km/h or pixels/sec)

- [ ] Implement debug overlay (game/ui/debug_overlay.py)
  - Toggle with F1 key
  - Display FPS counter
  - Show player speed
  - Display checkpoint index
  - Show lap number

**Estimated Completion**: After Phase 5

---

### Phase 7: Advanced Features
**Goal**: Add AI opponent and procedural generation

- [ ] Implement AI system (game/systems/ai_system.py)
  - Follow checkpoint sequence
  - Adjust steering toward next checkpoint
  - Respect track boundaries
  - Basic speed variation

- [ ] Implement procedural track generation (Advanced)
  - Generate random track layouts
  - Create checkpoint sequences
  - Define track boundaries algorithmically

**Estimated Completion**: After Phase 6

---

### Phase 8: Testing & Packaging
**Goal**: Ensure quality and create distributable build

- [ ] Write automated tests (tests/)
  - Physics calculations
  - Collision detection
  - Lap counting logic
  - Track loading validation

- [ ] Configure PyInstaller build (build_executable.py)
  - One-file executable mode
  - Include all game assets
  - Handle dependencies properly

- [ ] Create CI/CD pipeline (.github/workflows/ci.yml)
  - Install dependencies
  - Run pytest suite
  - Validate Python imports
  - Attempt PyInstaller build

**Estimated Completion**: After Phase 7

---

## Backlog & Upcoming Features

### Post-MVP Enhancements
- [ ] Drifting mechanics with visual effects
- [ ] Sound effects (engine, collision, lap complete)
- [ ] Background music system
- [ ] Particle effects (tire smoke, sparks)
- [ ] Enhanced AI with pathfinding algorithms
- [ ] Car customization (colors, performance upgrades)
- [ ] Leaderboard system (local storage)
- [ ] Achievements and reward system
- [ ] Multiplayer support (local hotseat or online)
- [ ] Save/load game progress
- [ ] Difficulty levels
- [ ] Power-ups and track items

### Technical Debt & Refactoring
- [ ] Optimize rendering for 60 FPS consistency
- [ ] Memory leak prevention
- [ ] Code documentation completion
- [ ] Unit test coverage improvement
- [ ] Performance profiling and optimization

---

## Development Milestones

### Milestone 1: Playable Demo (Target: Week 1)
**Definition Done**: Game runs with player car on one track, basic controls work, lap counting functional

**Deliverables**:
- Working game window
- Player car with physics
- One complete track
- Basic lap system
- Simple menu

---

### Milestone 2: Complete Core Features (Target: Week 2)
**Definition Done**: All core features implemented and tested, multiple tracks available

**Deliverables**:
- Full HUD implementation
- Debug overlay
- Two additional tracks
- AI opponent (basic)
- CI/CD pipeline working

---

### Milestone 3: Production Ready (Target: Week 3)
**Definition Done**: Polished game with packaging and testing complete

**Deliverables**:
- PyInstaller executable build
- Comprehensive test suite
- Documentation complete
- Performance optimized (60 FPS target)
- Bug fixes and polish

---

## Issue Tracking Template

Each GitHub issue should include:
- **Issue Type**: Feature, Bug, Technical Debt, Enhancement
- **Priority**: High, Medium, Low
- **Acceptance Criteria**: Clear conditions for completion
- **Technical Approach**: Brief description of implementation strategy
- **Dependencies**: Related issues that must be completed first

---

## Notes & Technical Decisions

1. **Arcade Engine Version**: Using latest stable version (>=2.30.0) for best features
2. **Window Resolution**: 1280x720 (HD) as base, scalable
3. **Physics Delta Time**: Frame-rate independent calculations using dt parameter
4. **Track Format**: JSON for flexibility and easy modification without code changes
5. **Asset Strategy**: Starting with shapes to avoid external dependencies
