"""
WSGI Entry Point for Vercel Deployment

This module provides the WSGI application callable that Vercel uses
to deploy Flask applications. It's required for Vercel to recognize
the Flask app as the entrypoint.
"""

from app import app as flask_app


def application(environ, start_response):
    """
    WSGI Application Callable
    
    This is the entry point that Vercel uses to run the Flask application.
    
    Args:
        environ: WSGI environment dictionary
        start_response: Callable that takes status code and headers
        
    Returns:
        Iterable of response bodies
    """
    return flask_app.wsgi_app(environ, start_response)