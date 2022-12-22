from data_proccessing_worker.config.log_conf import logger
from data_proccessing_worker.apps.models.base import SyncPostgresDriver
from data_proccessing_worker.apps.models.models import Feed, Indicator, Job, IndicatorActivity


class BaseProvider:
    def __init__(self):
        self.session = SyncPostgresDriver().session()


class FeedProvider(BaseProvider):
    pass


class IndicatorProvider(BaseProvider):
    def get_all(self):
        query = self.session.query(Indicator)

        return query.all()

    def update(self, feed: Feed):
        self.session.add(self.session.merge(feed))
        self.session.commit()


class JobProvider(BaseProvider):
    def add(self, job: Job):
        self.session.add(job)
        self.session.commit()

    def update(self, job: Job):
        logger.info(f"Updating job: {job}")
        self.session.add(job)
        self.session.commit()


class IndicatorActivityProvider(BaseProvider):
    def add(self, indicator_activity: IndicatorActivity):
        self.session.add(indicator_activity)
        self.session.commit()
