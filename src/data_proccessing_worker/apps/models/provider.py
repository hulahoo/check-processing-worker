from typing import List
from datetime import datetime
from sqlalchemy import and_

from data_proccessing_worker.apps.models.base import SyncPostgresDriver
from data_proccessing_worker.apps.models.models import Feed, Indicator


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
