"""
WSGI Application Entry Point for Vercel Deployment

This module serves as the main entry point for the Flask application
when deployed on Vercel. It provides WSGI compatibility and handles
HTTP requests from the Vercel platform.
"""

from flask import Flask, jsonify, request
import os

# Create Flask application instance
app = Flask(__name__)

# Configuration
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = app.config['ENV'] != 'production'


@app.route('/')
def home():
    """Root endpoint - returns game information."""
    return jsonify({
        'name': '2D Racing Game Demo',
        'version': '1.0.0',
        'engine': 'Arcade Python Library',
        'status': 'running',
        'message': 'Game server is running on Vercel'
    }), 200


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
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500


# WSGI Entry Point for Vercel
if __name__ == '__main__':
    # Only run development server when executed directly
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
