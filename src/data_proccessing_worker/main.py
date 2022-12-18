"""Entrypoint for starting all processes"""

import threading

from data_proccessing_worker.web.routers.api import execute as flask_app
from data_proccessing_worker.models.migrations import apply_migrations

def execute():
    """
    Function entrypoint to start:

    1. Worker to start scoring indicators
    2. Flask application to serve enpoints
    3. Apply migrations
    """
    apply_migrations()
    
    flask_thread = threading.Thread(target=flask_app)
    flask_thread.start()
    