"""
Flask API for Racing Demo - Vercel Deployment

This module provides a REST API backend for the racing game,
optimized for deployment on Vercel platform.
"""

from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Game configuration
GAME_CONFIG = {
    "game_version": "1.0.0",
    "max_players": 4,
    "supported_tracks": ["oval", "city", "desert"],
    "features": {
        "leaderboard": True,
        "multiplayer": False,
        "ai_opponent": True,
        "procedural_tracks": False
    },
    "physics": {
        "max_speed": 200,
        "acceleration": 150,
        "friction": 0.98,
        "turning_radius": 0.3
    }
}

@app.route('/')
def index():
    """Root endpoint - API information"""
    return jsonify({
        "name": "Racing Demo API",
        "version": GAME_CONFIG["game_version"],
        "description": "REST API for 2D Racing Game",
        "endpoints": {
            "/api/status": "Get server status",
            "/api/config": "Get game configuration",
            "/api/tracks": "List available tracks",
            "/api/leaderboard": "Get leaderboard (coming soon)",
            "/api/health": "Health check"
        }
    })

@app.route('/api/status', methods=['GET'])
def status():
    """Get server status and runtime information"""
    return jsonify({
        "status": "running",
        "version": GAME_CONFIG["game_version"],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "environment": os.environ.get("VERCEL_ENV", "development"),
        "build_id": os.environ.get("VERCEL_GIT_COMMIT_SHA", "unknown")
    })

@app.route('/api/config', methods=['GET'])
def config():
    """Get complete game configuration"""
    return jsonify(GAME_CONFIG)

@app.route('/api/tracks', methods=['GET'])
def tracks():
    """List all available tracks with metadata"""
    track_info = {
        "oval": {"name": "Oval Track", "length_km": 4.0, "difficulty": "easy"},
        "city": {"name": "City Circuit", "length_km": 3.2, "difficulty": "medium"},
        "desert": {"name": "Desert Rally", "length_km": 5.5, "difficulty": "hard"}
    }
    
    return jsonify({
        "tracks": GAME_CONFIG["supported_tracks"],
        "details": track_info,
        "count": len(GAME_CONFIG["supported_tracks"])
    })

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    """Get leaderboard (placeholder for future implementation)"""
    return jsonify({
        "leaderboard": [],
        "message": "Leaderboard feature not yet implemented",
        "coming_soon": True,
        "estimated_release": "v1.1.0"
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint for load balancers"""
    return jsonify({
        "healthy": True,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "racing-demo-api"
    }), 200

@app.route('/api/pong', methods=['GET'])
def pong():
    """Simple ping-pong endpoint for quick health checks"""
    return jsonify({"ping": "pong"})

if __name__ == '__main__':
    # Development mode only
    app.run(host='0.0.0.0', port=5000, debug=True)