from dagster import job, repository, ScheduleDefinition, op

from data_proccessing_worker.apps.services import IndicatorService
from data_proccessing_worker.apps.models.provider import IndicatorProvider


indicator_provider = IndicatorProvider()
indicator_service = IndicatorService()


@op
def update_indicators_op():
    indicator_service.update_weights()


@job
def update_indicators_job():
    update_indicators_op()


@repository
def indicators_repository():
    jobs = [
        ScheduleDefinition(
            job=update_indicators_job,
            cron_schedule='0 0 * * *'
        )
    ]

    return jobs
