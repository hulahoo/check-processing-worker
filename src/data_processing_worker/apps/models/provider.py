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


class IndicatorProvider(BaseProvider):
    def get_all(self):
        query = self.stream_session.query(Indicator).order_by(desc(Indicator.created_at))

        for row in query.yield_per(100):
            yield row

    def update(self, indicator: Indicator, commit: bool = False):
        flag_modified(indicator, 'context')
        self.session.add(self.session.merge(indicator))

        if commit:
            self.session.commit()


class ProcessProvider(BaseProvider):
    def get_by_id(self, id_: int):
        query = self.session.query(Process).filter(Process.id == id_)

        return query.one()

    def add(self, process: Process):
        current_process = self.session.query(Process).filter(
            Process.service_name == SERVICE_NAME
        ).filter(
            Process.name == process.name
        ).filter(
            Process.status.in_([JobStatus.IN_PROGRESS, JobStatus.PENDING])
        ).count()

        if not current_process:
            process.service_name = SERVICE_NAME

            self.session.add(process)
            self.session.commit()

    def update(self, process: Process):
        logger.info(f"Process to update: {process.id}")
        self.session.add(process)
        self.session.commit()

    def delete(self, status: str):
        self.session.query(Process).filter(
            Process.service_name == SERVICE_NAME
        ).filter(
            Process.status == status
        ).delete()

        self.session.commit()

    def get_all_by_statuses(self, statuses: List[str]):
        query = self.session.query(Process).filter(
            Process.service_name == SERVICE_NAME
        ).filter(
            Process.status.in_(statuses)
        )

        return query.all()


class IndicatorActivityProvider(BaseProvider):
    def add(self, indicator_activity: IndicatorActivity, commit: bool = False):
        self.session.add(indicator_activity)

        if commit:
            self.session.commit()


class ContextSourceProvider(BaseProvider):
    def get_by_type(self, ioc_type: str) -> List[ContextSource]:
        query = self.session.query(ContextSource).where(ContextSource.ioc_type == ioc_type)

        return query.all()


class PlatformSettingProvider(BaseProvider):
    def get_by_key(self, key: str) -> PlatformSetting:
        query = self.session.query(PlatformSetting).where(PlatformSetting.key == key)

        return query.first()
