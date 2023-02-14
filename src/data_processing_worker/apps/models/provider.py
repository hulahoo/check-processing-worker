from typing import List

from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import desc

from data_processing_worker.config.log_conf import logger
from data_processing_worker.apps.models.base import SyncPostgresDriver
from data_processing_worker.apps.models.models import (
    Indicator, Process, IndicatorActivity, ContextSource, PlatformSetting
)
from data_processing_worker.apps.constants import SERVICE_NAME
from data_processing_worker.apps.enums import JobStatus


class BaseProvider:
    def __init__(self):
        self.session = SyncPostgresDriver().session()
        self.stream_session = SyncPostgresDriver().session(stream=True)

        self.data = []

    def commit(self):
        try:
            with self.session() as session:
                for data in self.data:
                    session.add(session.merge(data))

                session.commit()
        finally:
            self.data = []


class IndicatorProvider(BaseProvider):
    def get_all(self, limit: int = None, offset: int = None):
        with self.stream_session() as session:
            query = session.query(Indicator).filter(
                Indicator.is_archived == False
            ).order_by(desc(Indicator.created_at))

            if limit is not None:
                query = query.limit(limit)

            if offset is not None:
                query = query.offset(offset)

            for row in query.yield_per(100):
                yield row

    def update(self, indicator: Indicator):
        flag_modified(indicator, 'context')
        self.data.append(indicator)

    def get_count(self):
        with self.stream_session() as session:
            query = session.query(Indicator).filter(
                Indicator.is_archived == False
            )

            return query.count()


class ProcessProvider(BaseProvider):
    def get_by_id(self, id_: int):
        with self.session() as session:
            query = session.query(Process).filter(Process.id == id_)

            return query.one()

    def add(self, process: Process):
        with self.session() as session:
            process.service_name = SERVICE_NAME

            session.add(process)
            session.commit()

    def update(self, process: Process):
        logger.info(f"Process to update: {process.id}")

        with self.session() as session:
            session.add(session.merge(process))
            session.commit()

    def delete(self, status: str):
        with self.session() as session:
            session.query(Process).filter(
                Process.service_name == SERVICE_NAME
            ).filter(
                Process.status == status
            ).delete()

            session.commit()

    def get_all_by_statuses(self, statuses: List[str]):
        with self.session() as session:
            query = session.query(Process).filter(
                Process.service_name == SERVICE_NAME
            ).filter(
                Process.status.in_(statuses)
            )

            return query.all()


class IndicatorActivityProvider(BaseProvider):
    def add(self, indicator_activity: IndicatorActivity):
        self.data.append(indicator_activity)


class ContextSourceProvider(BaseProvider):
    def get_by_type(self, ioc_type: str) -> List[ContextSource]:
        with self.session() as session:
            query = session.query(ContextSource).where(ContextSource.ioc_type == ioc_type)

            return query.all()


class PlatformSettingProvider(BaseProvider):
    def get_by_key(self, key: str) -> PlatformSetting:
        with self.session() as session:
            query = session.query(PlatformSetting).where(PlatformSetting.key == key)

            return query.first()
