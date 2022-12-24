from flask import Flask
from flask_wtf.csrf import CSRFProtect
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from datetime import datetime

from data_processing_worker.config.log_conf import logger
from data_processing_worker.apps.services import IndicatorService
from data_processing_worker.apps.models.models import Process
from data_processing_worker.apps.models.provider import ProcessProvider
from data_processing_worker.apps.constants import SERVICE_NAME
from data_processing_worker.apps.enums import JobStatus


app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

mimetype = 'application/json'


def execute():
    """
    Main function to start Flask application
    """
    logger.info("Starting flask app...")
    app.run(host='0.0.0.0', port='8080')
    logger.info("Flask app starting!")


@app.route('/health/readiness', methods=["GET"])
def readiness():
    """
    Текущее состояние готовности сервиса
    """
    logger.info("Readiness checking started")
    return app.response_class(
        response={"status": "UP"},
        status=200,
        mimetype=mimetype
    )


@app.route('/health/liveness', methods=["GET"])
def liveness():
    """
    Возвращает информацию о работоспособности сервиса
    """
    logger.info("Liveness checking started")
    return app.response_class(
        response={"status": "UP"},
        status=200,
        mimetype=mimetype
    )


@app.route('/metrics', methods=["GET"])
def metrics():
    """
    Возвращает метрики сервиса
    """
    return app.response_class(
        response=generate_latest(),
        status=200,
        mimetype='text/plain',
        content_type=CONTENT_TYPE_LATEST
    )


@app.route('/api', methods=["GET"])
def api_routes():
    return {
        "openapi:": "3.0.0",
        "info": {
            "title": "Воркер актуализации скоринга",
            "version": "0.0.1",
        },
        "paths": {}
        }


@app.route('/api/force-update', methods=["GET"])
def force_update():
    indicator_service = IndicatorService()
    process_provider = ProcessProvider()

    process = Process(
        service_name=SERVICE_NAME,
        title='update-weight',
        started_at=datetime.now(),
        status=JobStatus.IN_PROGRESS
    )

    process_provider.add(process)
    logger.info(f"Process created: {process.id}:{process.service_name}:{process.started_at}:{process.status}")

    indicator_service.update_weights()

    process.finished_at = datetime.now()
    process.status = JobStatus.SUCCESS
    logger.info(f"Process with id: {process.id} is finished successfully. Start update process")
    process_provider.update(process)

    return app.response_class(
        response={"status": "OK"},
        status=200,
        mimetype=mimetype
    )
