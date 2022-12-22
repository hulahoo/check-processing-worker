from typing import List
from math import ceil
from datetime import datetime

from data_proccessing_worker.config.log_conf import logger
from data_proccessing_worker.apps.models.models import IndicatorActivity, Indicator
from data_proccessing_worker.apps.models.provider import IndicatorProvider, IndicatorActivityProvider


class IndicatorService:
    def __init__(self):
        self.indicator_provider = IndicatorProvider()
        self.indicator_activity_provider = IndicatorActivityProvider()

    def _get_rv(self, tcurrent: datetime, tlastseen: datetime, T, A=1) -> float:
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
        logger.info(f"Start calculate indicator weight at: {now}")

        indicators: List[Indicator] = self.indicator_provider.get_all()
        logger.info(f"Retrieved indicators: {indicators}")

        for indicator in indicators:
            if not indicator.feeds:
                indicator.is_archived = True
                continue
            logger.info(
                f"Start calculating indicator - id:{indicator.id} weight:{indicator.weight} type:{indicator.ioc_type}"
            )
            if indicator.ioc_type in ['url', 'domain', 'ip', 'filename']:
                RV = self._get_rv(now, indicator.created_at, 14)
            else:
                RV = 1
            logger.info(f"RV is: {RV}")

            feed_weight = max(feed.weight for feed in indicator.feeds) / 100
            logger.info(f"Calculated feed weight: {feed_weight}")

            tag_weight = max(tag.weight for tag in indicator.tags) / 100 if indicator.tags else 1.0
            logger.info(f"Calculated tag weight: {tag_weight}")

            score = ceil(feed_weight * tag_weight * RV * 100)
            logger.info(f"Total calculated score: {score}")

            old_weight = indicator.weight
            indicator.weight = score

            if indicator.weight == 0:
                logger.info("Indicator weight is 0. Set it to archive")
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
