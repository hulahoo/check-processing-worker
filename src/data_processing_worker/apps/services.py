from typing import List
from math import ceil
from datetime import datetime

import requests
from requests.exceptions import RequestException

from data_processing_worker.config.log_conf import logger
from data_processing_worker.apps.models.models import IndicatorActivity, Indicator
from data_processing_worker.apps.models.provider import (
    IndicatorProvider, IndicatorActivityProvider, ContextSourceProvider
)


class IndicatorService:
    def __init__(self):
        self.indicator_provider = IndicatorProvider()
        self.indicator_activity_provider = IndicatorActivityProvider()
        self.context_source_provider = ContextSourceProvider()

    def _get_rv(
        self,
        *,
        tcurrent: datetime,
        tlastseen: datetime,
        t: int,
        a: int = 1
    ) -> float:
        """
        RV = 1 - ((tcurrent - tlastseen) / T) ** 1/A
        зависимость веса индикатора от времени

        :param tcurrent - текущее время
        :param tlastseen - время последнего обновления
        :param T - время жизни индикатора
        :param А - показатель угасания актуальности
        """
        T = t
        A = a
        return max(1 - ((tcurrent - tlastseen).days / T) ** (1/A), 0)

    def _parse_headers(self, headers_str: str):
        if not headers_str:
            return None

        headers = {}

        for header in headers_str.split('\n'):
            key, value = header.split(':')

            headers[key.strip()] = value.strip()

        return headers

    def _update_context(self, indicator: Indicator):
        sources = self.context_source_provider.get_by_type(indicator.ioc_type)

        for source in sources:
            headers = self._parse_headers(source.request_headers)
            url = source.source_url.replace('{value}', indicator.value)

            try:
                request = requests.get(url=url, headers=headers)

                if source.inbound_removable_prefix:
                    data = request.json()[source.inbound_removable_prefix]
                else:
                    data = request.json()

                if not indicator.context:
                    indicator.context = {}

                if source.outbound_appendable_prefix:
                    data = {source.outbound_appendable_prefix: data}
                else:
                    data = {'context': data}

                indicator.context.update(data)
            except RequestException:
                logger.warning(f"Unable to get response from {url}")

    def update_weights(self):
        now = datetime.now()
        logger.info(f"Start calculate indicator weight at: {now}")

        indicators: List[Indicator] = self.indicator_provider.get_all()
        logger.info(f"Retrieved indicators: {indicators}")

        for indicator in indicators:
            if not indicator.feeds:
                indicator.is_archived = True
                self.indicator_provider.update(indicator)
                continue

            self._update_context(indicator)

            logger.info(
                f"Start calculating indicator - id:{indicator.id} weight:{indicator.weight} type:{indicator.ioc_type}"
            )
            if indicator.ioc_type in ['url', 'domain', 'ip', 'filename']:
                RV = self._get_rv(
                    t=14,
                    tcurrent=now,
                    tlastseen=indicator.created_at,
                )
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
                activity_type='update-weight',
                details={
                    'change-from': str(old_weight),
                    'change-to': str(score),
                },
                indicator_id=indicator.id
            ))

        return indicators
