from sqlalchemy import inspect
from sqlalchemy.engine.base import Engine

from data_proccessing_worker.config.log_conf import logger
from data_proccessing_worker.apps.models.base import SyncPostgresDriver
from data_proccessing_worker.apps.models.models import IndicatorsContextSources


def apply_migrations() -> None:
    """Create migrations for Database"""
    logger.info("Start applying migartions...")
    engine: Engine = SyncPostgresDriver().engine
    tables_list = [IndicatorsContextSources.__tablename__]

    if not inspect(engine).has_table("indicators_context_sources"):
        IndicatorsContextSources.__table__.create(engine)
        tables_list.remove(IndicatorsContextSources.__tablename__)
        logger.info("Table IndicatorsContextSources created")

    logger.info(f"Tables already exists: {tables_list}")
    logger.info("Migration applied successfully")
