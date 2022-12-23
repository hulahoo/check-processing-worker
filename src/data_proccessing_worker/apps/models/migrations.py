from sqlalchemy import inspect
from sqlalchemy.engine.base import Engine

from data_proccessing_worker.config.log_conf import logger
from data_proccessing_worker.apps.models.base import SyncPostgresDriver
from data_proccessing_worker.apps.models.models import ContextSource, IndicatorContextSourceRelationship


def apply_migrations() -> None:
    """Create migrations for Database"""
    logger.info("Start applying migartions...")
    engine: Engine = SyncPostgresDriver().engine
    tables_list = [
        ContextSource.__tablename__,
        IndicatorContextSourceRelationship.__tablename__
    ]

    if not inspect(engine).has_table(ContextSource.__tablename__):
        ContextSource.__table__.create(engine)
        tables_list.remove(ContextSource.__tablename__)
        logger.info("Table ContextSource created")

    if not inspect(engine).has_table(IndicatorContextSourceRelationship.__tablename__):
        IndicatorContextSourceRelationship.__table__.create(engine)
        tables_list.remove(IndicatorContextSourceRelationship.__tablename__)
        logger.info("Table IndicatorContextSourceRelationship created")

    logger.info(f"Tables already exists: {tables_list}")
    logger.info("Migration applied successfully")
