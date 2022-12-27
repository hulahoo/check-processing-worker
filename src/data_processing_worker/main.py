"""Entrypoint for starting all processes"""

import threading
import subprocess
import os

from data_processing_worker.config.log_conf import logger
from data_processing_worker.web.routers.api import execute as flask_app


def start_worker():
    path = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(['dagit', '-f', f'{path}/worker.py'], check=True)


def execute():
    """
    Function entrypoint to start:

    1. Worker to start scoring indicators
    2. Flask application to serve enpoints
    """
    flask_thread = threading.Thread(target=flask_app)
    worker_thread = threading.Thread(target=start_worker)

    logger.info("Start Flask app")
    flask_thread.start()

    logger.info("Start worker")
    worker_thread.start()
