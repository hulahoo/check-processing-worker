from datetime import datetime
from math import ceil

from data_proccessing_worker.apps.models.provider import IndicatorProvider


class IndicatorService:
    def __init__(self):
        self.indicator_provider = IndicatorProvider()

    def update_weights(self):
        now = datetime.now()

        indicators = self.indicator_provider.get_all()

        for indicator in indicators:
            if not indicator.feeds:
                indicator.is_archived = True

            if indicator.ioc_type in ['url', 'domain', 'ip']:
                day_score = 100 / 14
                score = ceil(day_score * (now - indicator.created_at).days)

                weight = indicator.ioc_weight or 100

                indicator.ioc_weight = weight - score

            indicator.updated_at = now
            self.indicator_provider.update(indicator)

        return indicators
