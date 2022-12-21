from flask import Flask
from flask_wtf.csrf import CSRFProtect
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from data_proccessing_worker.config.log_conf import logger
from data_proccessing_worker.apps.services import IndicatorService


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
    indicator_service.update_weights()

    return app.response_class(
        response={"status": "OK"},
        status=200,
        mimetype=mimetype
    )