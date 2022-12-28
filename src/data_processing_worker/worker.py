from datetime import datetime
from dagster import job, repository, ScheduleDefinition, op, DefaultScheduleStatus

from data_processing_worker.apps.services import IndicatorService
from data_processing_worker.apps.models.provider import IndicatorProvider, ProcessProvider
from data_processing_worker.apps.models.models import Process
from data_processing_worker.apps.constants import SERVICE_NAME
from data_processing_worker.apps.enums import JobStatus


indicator_provider = IndicatorProvider()
indicator_service = IndicatorService()
process_provider = ProcessProvider()


@op
def update_indicators_op():
    process_ = Process(
        service_name=SERVICE_NAME,
        title='update-weight',
        started_at=datetime.now(),
        status=JobStatus.IN_PROGRESS
    )

    process_provider.add(process_)

    indicator_service.update_weights()

    process_.finished_at = datetime.now()
    process_.status = JobStatus.SUCCESS
    process_provider.update(process_)


@job
def update_indicators_job():
    update_indicators_op()


@repository
def indicators_repository():
    jobs = [
        ScheduleDefinition(
            job=update_indicators_job,
            cron_schedule='0 0 * * *',
            default_status=DefaultScheduleStatus.RUNNING
        )
    ]

    return jobs
