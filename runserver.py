"""
This script runs the SpinnrAIWebService application using a development server.
"""

from os import environ
from AIWebService import app

if __name__ == '__main__':
    # HOST = environ.get('SERVER_HOST', 'localhost')
    HOST = '0.0.0.0' 
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
