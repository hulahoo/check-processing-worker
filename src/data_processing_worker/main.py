"""Entrypoint for starting all processes"""

import threading
import subprocess
import os
import shutil

from data_processing_worker.config.log_conf import logger
from data_processing_worker.web.routers.api import execute as flask_app
from data_processing_worker.config.config import settings
from data_processing_worker.apps.models.provider import ProcessProvider
from data_processing_worker.apps.enums import JobStatus


if not os.path.exists(settings.app.dagster_home):
    os.makedirs(settings.app.dagster_home)

shutil.copy(settings.app.config_path, settings.app.dagster_home)

ProcessProvider().delete(status=JobStatus.IN_PROGRESS)

os.environ['DAGSTER_HOME'] = settings.app.dagster_home
path = os.path.dirname(os.path.abspath(__file__))


def start_dagit():
    subprocess.run(['dagit', '-f', f'{path}/worker.py'], check=True)


def start_dagster():
    subprocess.run(['dagster-daemon', 'run', '-f', f'{path}/worker.py'], check=True)


def execute():
    """
    Function entrypoint to start:

    1. Worker to start scoring indicators
    2. Flask application to serve enpoints
    """
    flask_thread = threading.Thread(target=flask_app)
    dagit_thread = threading.Thread(target=start_dagit)
    dagster_thread = threading.Thread(target=start_dagster)

    logger.info("Start Flask app")
    flask_thread.start()

    logger.info("Start Dagster...")
    dagster_thread.start()

    if settings.app.dagit_enabled:
        logger.info("Start Dagit...")
        dagit_thread.start()

