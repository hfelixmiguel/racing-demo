"""
Flask Wrapper for Racing Demo - Vercel Deployment

This module provides a WSGI-compatible HTTP server that serves the racing game
via websockets and canvas rendering, making it compatible with Vercel deployment.
"""

import json
import asyncio
from datetime import datetime
from typing import Optional
import arcade
from flask import Flask, request, jsonify, Response
import threading
import base64

app = Flask(__name__)

# Game state management
game_state = {
    "running": False,
    "player_position": {"x": 0, "y": 0},
    "player_velocity": {"x": 0, "y": 0},
    "speed": 0,
    "lap_number": 1,
    "lap_time": 0.0,
    "best_lap_time": 999999.0,
    "checkpoints_passed": [],
    "fps": 60,
    "debug_mode": False
}

# Game loop variables
game_thread = None
stop_event = threading.Event()
last_frame_time = 0.0
frame_count = 0


def create_game_window(width: int = 800, height: int = 600) -> arcade.Window:
    """Create the Arcade game window."""
    return arcade.Window(
        width=width,
        height=height,
        title="Racing Demo - Vercel Version",
        window_resizable=True
    )


def update_game(dt: float):
    """Update game state (placeholder for actual game logic)."""
    global frame_count, last_frame_time
    
    if not game_state["running"]:
        return
    
    # Simple physics simulation
    player = game_state["player_position"]
    velocity = game_state["player_velocity"]
    
    # Apply drag/friction
    velocity["x"] *= 0.98
    velocity["y"] *= 0.98
    
    # Update position
    player["x"] += velocity["x"] * dt * 100
    player["y"] += velocity["y"] * dt * 100
    
    # Calculate speed
    game_state["speed"] = abs(velocity["x"]) + abs(velocity["y"])
    
    # Update frame count for FPS calculation
    current_time = datetime.now().timestamp()
    if current_time - last_frame_time >= 1.0:
        game_state["fps"] = frame_count
        frame_count = 0
        last_frame_time = current_time
    
    frame_count += 1


def render_game_to_png(window: arcade.Window) -> bytes:
    """Render the game window to a PNG image."""
    # Create a simple rendering for demo purposes
    img_data = bytearray(4 * window.width * window.height)
    
    # Fill with background color (sky blue)
    for y in range(window.height):
        for x in range(window.width):
            idx = (y * window.width + x) * 4
            img_data[idx] = 135  # R - Sky blue
            img_data[idx + 1] = 206  # G
            img_data[idx + 2] = 235  # B
            img_data[idx + 3] = 255  # Alpha
    
    # Draw player car (red rectangle)
    player = game_state["player_position"]
    if player:
        px, py = int(player["x"]), int(player["y"])
        for dy in range(-10, 10):
            for dx in range(-15, 15):
                idx = ((py + dy) * window.width + (px + dx)) * 4
                if 0 <= py + dy < window.height and 0 <= px + dx < window.width:
                    img_data[idx] = 255  # R - Red
                    img_data[idx + 1] = 69  # G
                    img_data[idx + 2] = 57  # B
                    img_data[idx + 3] = 255  # Alpha
    
    return bytes(img_data)


@app.route('/api/start', methods=['POST'])
def start_game():
    """Start the game."""
    global game_state, stop_event
    
    game_state["running"] = True
    game_state["lap_number"] = 1
    game_state["lap_time"] = 0.0
    game_state["checkpoints_passed"] = []
    
    return jsonify({
        "status": "started",
        "message": "Game started successfully"
    })


@app.route('/api/stop', methods=['POST'])
def stop_game():
    """Stop the game."""
    global game_state
    
    game_state["running"] = False
    game_state["speed"] = 0
    
    return jsonify({
        "status": "stopped",
        "message": "Game stopped"
    })


@app.route('/api/reset', methods=['POST'])
def reset_game():
    """Reset the game to initial state."""
    global game_state
    
    game_state["running"] = False
    game_state["player_position"] = {"x": 0, "y": 0}
    game_state["player_velocity"] = {"x": 0, "y": 0}
    game_state["speed"] = 0
    game_state["lap_number"] = 1
    game_state["lap_time"] = 0.0
    game_state["best_lap_time"] = 999999.0
    game_state["checkpoints_passed"] = []
    
    return jsonify({
        "status": "reset",
        "message": "Game reset successfully"
    })


@app.route('/api/state', methods=['GET'])
def get_game_state():
    """Get current game state."""
    return jsonify(game_state.copy())


@app.route('/api/input', methods=['POST'])
def handle_input():
    """Handle player input."""
    global game_state
    
    data = request.json or {}
    inputs = data.get('inputs', {})
    
    # Update velocity based on input
    if 'up' in inputs:
        game_state["player_velocity"]["y"] += 0.5
    if 'down' in inputs:
        game_state["player_velocity"]["y"] -= 0.5
    if 'left' in inputs:
        game_state["player_velocity"]["x"] -= 0.5
    if 'right' in inputs:
        game_state["player_velocity"]["x"] += 0.5
    
    # Clamp velocity
    max_speed = 10.0
    speed = abs(game_state["player_velocity"]["x"]) + abs(game_state["player_velocity"]["y"])
    if speed > max_speed:
        scale = max_speed / speed
        game_state["player_velocity"]["x"] *= scale
        game_state["player_velocity"]["y"] *= scale
    
    return jsonify({
        "status": "input_received",
        "velocity": game_state["player_velocity"].copy()
    })


@app.route('/api/toggle-debug', methods=['POST'])
def toggle_debug():
    """Toggle debug mode."""
    global game_state, game_thread
    
    game_state["debug_mode"] = not game_state["debug_mode"]
    
    return jsonify({
        "status": "debug_toggled",
        "debug_mode": game_state["debug_mode"]
    })


@app.route('/ws/game', methods=['GET'])
def websocket_endpoint():
    """WebSocket endpoint for real-time game updates."""
    # Note: Vercel doesn't support WebSocket servers directly
    # This is a fallback to simulate real-time updates via polling
    return jsonify({
        "message": "Use /api/poll for updates (Vercel compatibility)",
        "poll_url": "/api/poll"
    })


@app.route('/api/poll', methods=['GET'])
def poll_game():
    """Polling endpoint for game state updates."""
    # Simulate game update
    if game_state["running"]:
        update_game(1.0 / 60)
    
    return jsonify(game_state.copy())


@app.route('/canvas/render', methods=['GET'])
def render_canvas():
    """Render game frame as base64 PNG."""
    window = create_game_window()
    img_data = render_game_to_png(window)
    window.close()
    
    return Response(
        base64.b64encode(img_data).decode('utf-8'),
        mimetype='image/png'
    )


@app.route('/api/info', methods=['GET'])
def get_info():
    """Get application information."""
    return jsonify({
        "name": "Racing Demo",
        "version": "1.0.0",
        "platform": "Vercel (Flask WSGI)",
        "description": "2D Racing Game - Web-Compatible Version",
        "controls": {
            "accelerate": "W or Up Arrow",
            "brake": "S or Down Arrow",
            "turn_left": "A or Left Arrow",
            "turn_right": "D or Right Arrow"
        },
        "endpoints": {
            "start_game": "/api/start (POST)",
            "stop_game": "/api/stop (POST)",
            "reset_game": "/api/reset (POST)",
            "get_state": "/api/state (GET)",
            "handle_input": "/api/input (POST)",
            "toggle_debug": "/api/toggle-debug (POST)",
            "poll_updates": "/api/poll (GET)",
            "render_canvas": "/canvas/render (GET)"
        }
    })


@app.route('/<path:path>', methods=['GET', 'POST'])
def serve_static(path: str):
    """Serve static files and HTML interface."""
    if path == '' or path == '/':
        return render_index()
    return app.send_static_file(path)


def render_index():
    """Render the main HTML page."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Racing Demo - Vercel</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 600px;
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
        }}
        .controls {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: left;
        }}
        .controls h3 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        .control-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
        }}
        .control-item:last-child {{ border-bottom: none; }}
        button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.2em;
            border-radius: 50px;
            cursor: pointer;
            margin: 10px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }}
        button:disabled {{
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }}
        .status {{
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            font-weight: bold;
        }}
        .status.running {{ background: #d4edda; color: #155724; }}
        .status.stopped {{ background: #f8d7da; color: #721c24; }}
        canvas {{
            max-width: 100%;
            border-radius: 10px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏎️ Racing Demo</h1>
        <p class="subtitle">Vercel Deployment - Flask WSGI</p>
        
        <div class="controls">
            <h3>Controls</h3>
            <div class="control-item">
                <span>Accelerate:</span>
                <strong>W / ↑</strong>
            </div>
            <div class="control-item">
                <span>Brake:</span>
                <strong>S / ↓</strong>
            </div>
            <div class="control-item">
                <span>Turn Left:</span>
                <strong>A / ←</strong>
            </div>
            <div class="control-item">
                <span>Turn Right:</span>
                <strong>D / →</strong>
            </div>
        </div>
        
        <button id="startBtn" onclick="startGame()">Start Game</button>
        <button id="stopBtn" onclick="stopGame()" disabled>Stop Game</button>
        <button id="resetBtn" onclick="resetGame()" disabled>Reset</button>
        
        <div id="status" class="status stopped">Status: Stopped</div>
        
        <canvas id="gameCanvas" width="800" height="600"></canvas>
    </div>
    
    <script>
        let gameRunning = false;
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        function startGame() {
            fetch('/api/start', {{ method: 'POST' }})
                .then(res => res.json())
                .then(data => {{
                    gameRunning = true;
                    updateStatus();
                    document.getElementById('startBtn').disabled = true;
                    document.getElementById('stopBtn').disabled = false;
                    document.getElementById('resetBtn').disabled = false;
                }});
        }
        
        function stopGame() {
            fetch('/api/stop', {{ method: 'POST' }})
                .then(res => res.json())
                .then(data => {{
                    gameRunning = false;
                    updateStatus();
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('stopBtn').disabled = true;
                }});
        }
        
        function resetGame() {
            fetch('/api/reset', {{ method: 'POST' }})
                .then(res => res.json())
                .then(data => {{
                    gameRunning = false;
                    updateStatus();
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('stopBtn').disabled = true;
                }});
        }
        
        function updateStatus() {{
            const statusDiv = document.getElementById('status');
            statusDiv.className = 'status ' + (gameRunning ? 'running' : 'stopped');
            statusDiv.textContent = 'Status: ' + (gameRunning ? 'Running' : 'Stopped');
        }}
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => {{
            if (!gameRunning) return;
            
            const inputs = {};
            switch(e.key.toLowerCase()) {{
                case 'w': case 'arrowup': inputs.up = true; break;
                case 's': case 'arrowdown': inputs.down = true; break;
                case 'a': case 'arrowleft': inputs.left = true; break;
                case 'd': case 'arrowright': inputs.right = true; break;
            }}
            
            if (Object.keys(inputs).length > 0) {{
                fetch('/api/input', {{ method: 'POST', headers: {{'Content-Type': 'application/json'}} }}, 
                    body: JSON.stringify({{inputs}}))
                    .then(res => res.json())
                    .then(data => console.log('Input received:', data));
            }}
        }});
        
        // Poll for game state updates
        setInterval(() => {{
            if (gameRunning) {{
                fetch('/api/poll')
                    .then(res => res.json())
                    .then(state => console.log('Game state:', state));
            }}
        }}, 100);
        
        // Render canvas
        function render() {{
            ctx.fillStyle = '#87CEEB';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            if (gameRunning) {{
                fetch('/canvas/render')
                    .then(res => res.blob())
                    .then(blob => {{
                        const url = URL.createObjectURL(blob);
                        const img = new Image();
                        img.onload = () => ctx.drawImage(img, 0, 0);
                        img.src = url;
                    }});
            }}
        }}
        
        setInterval(render, 1000 / 60);
    </script>
</body>
</html>"""

    return Response(html, mimetype='text/html')


# WSGI entry point for Vercel/Gunicorn
def application(environ, start_response):
    """WSGI application callable."""
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [app.wsgi_app(environ, start_response)]


if __name__ == '__main__':
    # For local development
    app.run(host='0.0.0.0', port=5000, debug=True)
