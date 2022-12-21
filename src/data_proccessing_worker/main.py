"""Entrypoint for starting all processes"""

import threading
import subprocess
import os

from data_proccessing_worker.web.routers.api import execute as flask_app
from data_proccessing_worker.apps.models.migrations import apply_migrations


def start_worker():
    path = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(['dagit', '-f', f'{path}/worker.py'], check=True)


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

    worker_thread = threading.Thread(target=start_worker)
    worker_thread.start()
