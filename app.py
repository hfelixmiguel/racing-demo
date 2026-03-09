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
        body { font-family: Arial, sans-serif; background: #1a1a1a; color: #fff; }
        .game-container { 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            padding: 20px; 
        }
        .game-info {
            text-align: center;
            max-width: 600px;
            background: #2d2d2d;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .game-title { 
            color: #4CAF50; 
            font-size: 28px; 
            margin-bottom: 20px;
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
        }
        .feature-list li {
            padding: 8px 0;
            border-bottom: 1px solid #444;
        }
        .feature-list li:last-child { border-bottom: none; }
        .action-btn {
            background: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
        }
        .action-btn:hover { background: #45a049; }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-info">
            <h1 class="game-title">🏎️ 2D Racing Game Demo</h1>
            <p>A top-down racing game built with Python Arcade Engine</p>
            
            <div class="status-bar">
                <span><strong>Status:</strong> Running</span>
                <span><strong>Version:</strong> 1.0.0</span>
                <span><strong>Engine:</strong> Arcade Python Library</span>
            </div>

            <h3 style="color: #4CAF50; margin: 20px 0;">Game Features:</h3>
            <ul class="feature-list">
                <li>🎮 Realistic car physics with acceleration, braking, and steering</li>
                <li>🏁 Multiple configurable tracks from JSON files</li>
                <li>⏱️ Complete lap counting and timing system</li>
                <li>🤖 AI opponent that follows checkpoints</li>
                <li>📷 Smooth camera following the player car</li>
            </ul>

            <h3 style="color: #4CAF50; margin: 20px 0;">Controls:</h3>
            <div class="status-bar" style="margin-bottom: 15px;">
                <span><strong>Accelerate:</strong> W / Up Arrow</span>
                <span><strong>Brake:</strong> S / Down Arrow</span>
            </div>
            <div class="status-bar">
                <span><strong>Turn Left:</strong> A / Left Arrow</span>
                <span><strong>Turn Right:</strong> D / Right Arrow</span>
            </div>

            <button class="action-btn" onclick="window.alert('Game is running on Vercel!\\n\\nThe game uses Python Arcade library which requires a native window.\\nFor browser-based gameplay, please check the GitHub repository for instructions.')">🎮 Start Game</button>
        </div>
    </div>

    <script>
        // Simple interaction to show the page is working
        console.log('Racing Demo - Version 1.0.0');
        console.log('Engine: Arcade Python Library');
        console.log('Status: Running on Vercel');
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
