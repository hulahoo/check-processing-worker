from datetime import datetime
from dagster import job, repository, ScheduleDefinition, op

from data_proccessing_worker.apps.services import IndicatorService
from data_proccessing_worker.apps.models.provider import IndicatorProvider, JobProvider
from data_proccessing_worker.apps.models.models import Job
from data_proccessing_worker.apps.constants import SERVICE_NAME
from data_proccessing_worker.apps.enums import JobStatus


indicator_provider = IndicatorProvider()
indicator_service = IndicatorService()
job_provider = JobProvider()


@op
def update_indicators_op():
    job_ = Job(
        service_name=SERVICE_NAME,
        title='update-weight',
        started_at=datetime.now(),
        status=JobStatus.IN_PROGRESS
    )

    job_provider.add(job_)

    indicator_service.update_weights()

    job_.finished_at = datetime.now()
    job_.status = JobStatus.SUCCESS
    job_provider.update(job_)


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
