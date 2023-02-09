import pytz
from math import ceil
from decimal import Decimal
from datetime import datetime

import requests
from requests.exceptions import RequestException

from data_processing_worker.apps.constants import SERVICE_NAME
from data_processing_worker.config.log_conf import logger
from data_processing_worker.apps.models.models import IndicatorActivity, Indicator, PlatformSetting
from data_processing_worker.apps.models.provider import (
    IndicatorProvider, IndicatorActivityProvider, ContextSourceProvider, PlatformSettingProvider
)
from data_processing_worker.apps.utils.context_parser import parse_context


class IndicatorService:
    def __init__(self):
        self.indicator_provider = IndicatorProvider()
        self.indicator_activity_provider = IndicatorActivityProvider()
        self.context_source_provider = ContextSourceProvider()
        self.platform_setting_provider = PlatformSettingProvider()

        self.batch_size = 100

    def _get_rv(
        self,
        *,
        tcurrent: datetime,
        tlastseen: datetime,
        t: int,
        a: float = 1
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
        logger.info(f"tcurrent: {tcurrent}, tlastseen: {tlastseen}, T: {T}, A: {A}")
        logger.info(f"weight = (1 - {tcurrent.day} - {tlastseen.day} / {T} ** (1/{A}))")
        return max(1 - (max((tcurrent - tlastseen).days, 0) / T) ** (1/A), 0)

    def _parse_headers(self, headers_str: str):
        if not headers_str:
            return None

        headers = {}

        for header in headers_str.split('\n'):
            key, value = header.split(':')

            headers[key.strip()] = value.strip()

        return headers

    def _update_context(self, indicator: Indicator):
        if indicator.is_archived:
            return

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
                    prefix = source.outbound_appendable_prefix
                else:
                    prefix = 'context'

                parsed_context = parse_context(prefix, data)

                indicator.context.update(parsed_context)
            except RequestException:
                logger.warning(f"Unable to get response from {url}")

    def _get_settings(self, setting: PlatformSetting, type: str):
        ttl = 14
        weight_decreasing = 1

        if setting and setting.value:
            if setting.value['indicators-ttl'] and type in setting.value['indicators-ttl']:
                ttl = setting.value['indicators-ttl'][type]

            if setting.value['indicators-weight-decreasing'] and type in setting.value['indicators-weight-decreasing']:
                weight_decreasing = setting.value['indicators-weight-decreasing'][type]

        return ttl, weight_decreasing

    def _commit(self, batch_size):
        logger.info(f'commit {batch_size} indicators')

        try:
            self.indicator_provider.commit()
            self.indicator_activity_provider.commit()
        except Exception as e:
            logger.warning(f'commit failed: {e}. The batch is skipped for this run')

    def _update_weight(self, indicator: Indicator, now: datetime):
        if indicator.ioc_type in ['url', 'domain', 'ip', 'filename']:
            setting: PlatformSetting = self.platform_setting_provider.get_by_key(SERVICE_NAME)

            ttl, weight_decreasing = self._get_settings(setting, indicator.ioc_type)

            RV = self._get_rv(
                t=ttl,
                a=weight_decreasing,
                tcurrent=now,
                tlastseen=indicator.created_at.replace(tzinfo=pytz.UTC),
            )
        else:
            RV = 1

        feed_weight = max(feed.weight for feed in indicator.feeds) / 100
        tag_weight = max(tag.weight for tag in indicator.tags) / 100 if indicator.tags else 1.0
        score = ceil(Decimal(feed_weight) * Decimal(tag_weight) * Decimal(RV) * Decimal(100))

        indicator.weight = score

    def _archive(self, indicator: Indicator):
        if not indicator.feeds or indicator.weight == 0:
            indicator.is_archived = True

    def update_context(self):
        now = datetime.now(tz=pytz.UTC)
        logger.info(f"Start update indicator context at: {now}")

        total_indicators_count = 0

        for indicator in self.indicator_provider.get_all():
            self._update_context(indicator)

            self.indicator_provider.update(indicator)

            self.indicator_activity_provider.add(IndicatorActivity(
                activity_type='update-context',
                indicator_id=indicator.id
            ))

            total_indicators_count += 1

            if total_indicators_count % self.batch_size == 0:
                logger.info(f'Total indicators: {total_indicators_count}')
                self._commit(self.batch_size)

        self._commit(total_indicators_count % self.batch_size)

    def archive(self):
        now = datetime.now(tz=pytz.UTC)
        logger.info(f"Start archiving indicator at: {now}")

        total_indicators_count = 0

        for indicator in self.indicator_provider.get_all():
            self._archive(indicator)

            self.indicator_provider.update(indicator)

            self.indicator_activity_provider.add(IndicatorActivity(
                activity_type='archive',
                indicator_id=indicator.id
            ))

            total_indicators_count += 1

            if total_indicators_count % self.batch_size == 0:
                logger.info(f'Total indicators: {total_indicators_count}')
                self._commit(self.batch_size)

        self._commit(total_indicators_count % self.batch_size)

    def update_weights(self):
        now = datetime.now(tz=pytz.UTC)
        logger.info(f"Start calculate indicator weight at: {now}")

        total_indicators_count = 0

        for indicator in self.indicator_provider.get_all():
            logger.info(f"Process indicator {indicator.id}")

            old_weight = indicator.weight

            self._update_weight(indicator, now)

            self.indicator_provider.update(indicator)

            self.indicator_activity_provider.add(IndicatorActivity(
                activity_type='update-weight',
                details={
                    'change-from': str(old_weight),
                    'change-to': str(indicator.weight),
                },
                indicator_id=indicator.id
            ))

            total_indicators_count += 1

            if total_indicators_count % self.batch_size == 0:
                logger.info(f'Total indicators: {total_indicators_count}')
                self._commit(self.batch_size)

        self._commit(total_indicators_count % self.batch_size)
