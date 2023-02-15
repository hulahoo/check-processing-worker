import json

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from data_processing_worker.config.log_conf import logger

from data_processing_worker.apps.models.models import Process
from data_processing_worker.apps.models.provider import ProcessProvider, IndicatorProvider

from data_processing_worker.apps.services import IndicatorService
from data_processing_worker.apps.enums import JobStatus


app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

mimetype = 'application/json'

indicator_service = IndicatorService()
process_provider = ProcessProvider()
indicator_provider = IndicatorProvider()


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
    if process_provider.get_all_by_statuses([JobStatus.IN_PROGRESS, JobStatus.PENDING]):
        return

    chunk_size = 1000
    indicators_count = indicator_provider.get_count()

    for i in range(0, indicators_count, chunk_size):
        process_provider.add(Process(
            status=JobStatus.PENDING,
            name=f'update indicators weight',
            request={
                'limit': chunk_size,
                'offset': i
            }
        ))

    return app.response_class(
        response={"status": "Started"},
        status=200,
        content_type=mimetype
    )


@app.route('/api/force-update/statistics', methods=["GET"])
def force_update_statistics():
    result = []

    for process in process_provider.get_all_by_statuses([JobStatus.PENDING, JobStatus.IN_PROGRESS]):
        result.append({
            "process_status": process.status,
            "process_name": process.name,
        })

    return app.response_class(
        response=json.dumps(result),
        status=200,
        content_type=mimetype
    )
