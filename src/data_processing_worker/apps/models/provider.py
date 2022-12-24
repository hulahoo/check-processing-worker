from typing import List

from sqlalchemy.orm.attributes import flag_modified

from data_processing_worker.config.log_conf import logger
from data_processing_worker.apps.models.base import SyncPostgresDriver
from data_processing_worker.apps.models.models import Indicator, Process, IndicatorActivity, ContextSource


class BaseProvider:
    def __init__(self):
        self.session = SyncPostgresDriver().session()


class IndicatorProvider(BaseProvider):
    def get_all(self):
        query = self.session.query(Indicator)

        return query.all()

    def update(self, indicator: Indicator):
        flag_modified(indicator, 'context')
        self.session.add(self.session.merge(indicator))
        self.session.commit()


class ProcessProvider(BaseProvider):
    def add(self, process: Process):
        self.session.add(process)
        self.session.commit()

    def update(self, process: Process):
        logger.info(f"Updating process: {process.id}")
        self.session.add(process)
        self.session.commit()


class IndicatorActivityProvider(BaseProvider):
    def add(self, indicator_activity: IndicatorActivity):
        self.session.add(indicator_activity)
        self.session.commit()


class ContextSourceProvider(BaseProvider):
    def get_by_type(self, ioc_type: str) -> List[ContextSource]:
        query = self.session.query(ContextSource).where(ContextSource.ioc_type == ioc_type)

        return query.all()
