from datetime import datetime
from math import ceil

from data_proccessing_worker.apps.models.models import IndicatorActivity
from data_proccessing_worker.apps.models.provider import IndicatorProvider, IndicatorActivityProvider


class IndicatorService:
    def __init__(self):
        self.indicator_provider = IndicatorProvider()
        self.indicator_activity_provider =  IndicatorActivityProvider()

    def _get_RV(self, tcurrent: datetime, tlastseen: datetime, T, A=1) -> float:
        """
        RV = 1 - ((tcurrent - tlastseen) / T) ** 1/A
        зависимость веса индикатора от времени

        :param tcurrent - текущее время
        :param tlastseen - время последнего обновления
        :param T - время жизни индикатора
        :param А - показатель угасания актуальности
        """
        return max(1 - ((tcurrent - tlastseen).days / T) ** (1/A), 0)

    def update_weights(self):
        now = datetime.now()

        indicators = self.indicator_provider.get_all()

        for indicator in indicators:
            if not indicator.feeds:
                indicator.is_archived = True
                continue

            if indicator.ioc_type in ['url', 'domain', 'ip', 'filename']:
                RV = self._get_RV(now, indicator.created_at, 14)
            else:
                RV = 1

            feed_weight = max(feed.weight for feed in indicator.feeds) / 100
            tag_weight = max(tag.weight for tag in indicator.tags) / 100 if indicator.tags else 1.0

            score = ceil(feed_weight * tag_weight * RV * 100)

            old_weight = indicator.ioc_weight
            indicator.ioc_weight = score

            if indicator.ioc_weight == 0:
                indicator.is_archived = True

            indicator.updated_at = now
            self.indicator_provider.update(indicator)

            self.indicator_activity_provider.add(IndicatorActivity(
                type='update-weight',
                details={
                    'change-from': str(old_weight),
                    'change-to': str(score),
                },
                indicator_id=indicator.id
            ))

        return indicators
