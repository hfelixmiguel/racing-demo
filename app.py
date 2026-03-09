"""
Flask Application for 2D Racing Game Demo API

This module contains the main Flask application that serves as the REST API
for the racing game demo when deployed on Vercel.
"""

from flask import Flask, jsonify, request, render_template_string
import os
import logging

# Create Flask application instance
app = Flask(__name__)

# Configuration
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = app.config['ENV'] != 'production'


def get_game_html():
    """HTML template for the racing game interface."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2D Racing Game Demo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            background: #1a1a1a; 
            color: #fff; 
            min-height: 100vh;
        }
        .game-container { 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            padding: 20px; 
        }
        .game-info {
            text-align: center;
            max-width: 700px;
            background: #2d2d2d;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .game-title { 
            color: #4CAF50; 
            font-size: 32px; 
            margin-bottom: 20px;
            font-weight: bold;
        }
        .status-bar {
            background: #3d3d3d;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            display: flex;
            justify-content: space-between;
        }
        .feature-list {
            list-style: none;
            text-align: left;
            margin: 20px 0;
            padding: 0 40px;
        }
        .feature-list li {
            padding: 10px 0;
            border-bottom: 1px solid #444;
            color: #ccc;
        }
        .feature-list li:last-child { 
            border-bottom: none; 
        }
        .action-btn {
            background: #4CAF50;
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 18px;
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        .action-btn:hover { 
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
        }
        .action-btn:active {
            transform: translateY(0);
        }
        .game-section {
            margin: 30px 0;
        }
        .instructions-box {
            background: #1a1a1a;
            padding: 20px;
            border-radius: 8px;
            text-align: left;
            margin: 20px 0;
            font-family: monospace;
            color: #76e94b;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #4CAF50;
            margin-right: 8px;
        }
        .info-icon {
            color: #76e94b;
        }
        h3 { 
            color: #76e94b; 
            font-size: 20px;
            margin-bottom: 15px;
        }
        p {
            color: #ccc;
            line-height: 1.6;
        }
        .highlight {
            background: rgba(76, 175, 80, 0.2);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-info">
            <h1 class="game-title">🏎️ 2D Racing Game Demo</h1>
            <p style="color: #aaa; margin-bottom: 30px;">A top-down racing game built with Python Arcade Engine</p>
            
            <div class="status-bar">
                <span><strong>Status:</strong> <span class="status-indicator"></span>Running</span>
                <span><strong>Version:</strong> 1.0.0</span>
                <span><strong>Engine:</strong> Arcade Python Library</span>
            </div>

            <h3 style="color: #76e94b; margin: 25px 0;">🎮 Start Playing!</h3>
            
            <p>The game is ready to play! You can run it locally on your computer:</p>
            
            <div class="instructions-box">
                <pre style="white-space: pre-wrap; word-wrap: break-word;">pip install arcade
python main.py</pre>
            </div>

            <h3 style="color: #76e94b; margin: 25px 0;" id="features-title">✅ Game Features:</h3>
            <ul class="feature-list">
                <li><strong>🎮 Realistic car physics</strong> with acceleration, braking, and steering</li>
                <li><strong>🏁 Multiple configurable tracks</strong> from JSON files (Oval, City, Desert)</li>
                <li><strong>⏱️ Complete lap counting</strong> and timing system</li>
                <li><strong>🤖 AI opponent</strong> that follows checkpoints</li>
                <li><strong>📷 Smooth camera</strong> following the player car</li>
            </ul>

            <h3 style="color: #76e94b; margin: 25px 0;">⌨️ Controls:</h3>
            <div class="status-bar" style="margin-bottom: 15px;">
                <span><strong>Accelerate:</strong> <span class="highlight">W</span> / <span class="highlight">↑</span></span>
                <span><strong>Brake:</strong> <span class="highlight">S</span> / <span class="highlight">↓</span></span>
            </div>
            <div class="status-bar">
                <span><strong>Turn Left:</strong> <span class="highlight">A</span> / <span class="highlight">←</span></span>
                <span><strong>Turn Right:</strong> <span class="highlight">D</span> / <span class="highlight">→</span></span>
            </div>

            <button class="action-btn" onclick="showGameInstructions()">🎮 Start Game</button>

            <div id="instructions-panel" style="display: none; margin-top: 20px;">
                <h3 style="color: #76e94b;">📋 How to Run the Game:</h3>
                
                <div class="instructions-box">
                    <p><strong>Option 1: Quick Start (Recommended)</strong></p>
                    <pre style="white-space: pre-wrap; word-wrap: break-word;"># Install the Arcade library
pip install arcade

# Run the game
python main.py</pre>
                </div>

                <div class="instructions-box">
                    <p><strong>Option 2: Build Executable (Windows)</strong></p>
                    <pre style="white-space: pre-wrap; word-wrap: break-word;">pip install pyinstaller
python build_executable.py</pre>
                </div>

                <div class="instructions-box">
                    <p><strong>Option 3: Run from GitHub</strong></p>
                    <pre style="white-space: pre-wrap; word-wrap: break-word;"># Clone the repository
git clone https://github.com/hfelixmiguel/racing-demo.git

cd racing-demo
pip install arcade
python main.py</pre>
                </div>
            </div>

        </div>
    </div>

    <script>
        function showGameInstructions() {
            const panel = document.getElementById('instructions-panel');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                window.scrollTo(0, document.body.scrollHeight);
            } else {
                panel.style.display = 'none';
            }
        }

        // Simple interaction to show the page is working
        console.log('Racing Demo - Version 1.0.0');
        console.log('Engine: Arcade Python Library');
        console.log('Status: Running on Vercel');

        // Auto-show instructions after 3 seconds
        setTimeout(() => {
            const panel = document.getElementById('instructions-panel');
            if (!panel || panel.style.display === 'none') {
                panel.style.display = 'block';
            }
        }, 3000);
    </script>
</body>
</html>'''


@app.route('/')
def home():
    """Root endpoint - returns HTML game interface."""
    return render_template_string(get_game_html()), 200, {
        'Content-Type': 'text/html; charset=utf-8'
    }


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'racing-demo',
        'environment': app.config['ENV']
    }), 200


@app.route('/api/game/status')
def game_status():
    """Returns current game status information."""
    return jsonify({
        'game': 'racing-demo',
        'features': [
            '2D Racing Gameplay',
            'Physics-based Car Control',
            'Multiple Tracks',
            'Lap Timing System',
            'AI Opponent',
            'Procedural Track Generation'
        ],
        'deployment': {
            'platform': 'Vercel',
            'engine': 'Flask WSGI'
        }
    }), 200


@app.route('/api/game/info')
def game_info():
    """Returns detailed game information."""
    return jsonify({
        'title': '2D Racing Game Demo',
        'description': 'A top-down 2D racing game built with Python Arcade engine',
        'controls': {
            'accelerate': ['W', 'Up Arrow'],
            'brake': ['S', 'Down Arrow'],
            'turn_left': ['A', 'Left Arrow'],
            'turn_right': ['D', 'Right Arrow']
        },
        'features': {
            'physics': 'Realistic car physics with acceleration, braking, and steering',
            'tracks': 'Multiple configurable tracks from JSON files',
            'lap_system': 'Complete lap counting and timing system',
            'ai_opponent': 'Basic AI opponent that follows checkpoints',
            'camera': 'Smooth camera following the player car'
        }
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger = logging.getLogger(__name__)
    logger.error("Internal server error")
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    """Run the Flask development server."""
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
