from datetime import datetime
from dagster import (
    job,
    op,
    repository,
    ScheduleDefinition,
    DefaultScheduleStatus,
    DagsterInstance
)

from data_processing_worker.apps.services import IndicatorService
from data_processing_worker.apps.models.provider import IndicatorProvider, ProcessProvider, JobProvider
from data_processing_worker.apps.models.models import Process
from data_processing_worker.apps.constants import SERVICE_NAME
from data_processing_worker.apps.enums import JobStatus, WorkerJobStatus


indicator_provider = IndicatorProvider()
indicator_service = IndicatorService()
process_provider = ProcessProvider()
job_provider = JobProvider()


@op
def update_indicators_op():
    process = Process(
        service_name=SERVICE_NAME,
        title='update-weight',
        started_at=datetime.now(),
        status=JobStatus.IN_PROGRESS
    )

    process_provider.add(process)

    indicator_service.update_weights()

    process.finished_at = datetime.now()
    process.status = JobStatus.SUCCESS
    process_provider.update(process)


@job
def update_indicators_job():
    update_indicators_op()


@job(name='check_jobs')
def check_jobs():
    job_provider.delete(status=WorkerJobStatus.FINISHED)

    if job_provider.get_all(status=WorkerJobStatus.RUNNING):
        return

    jobs = job_provider.get_all(status=WorkerJobStatus.PENDING)

    for job in jobs:
        job.status = WorkerJobStatus.RUNNING
        job_provider.update(job)

        update_indicators_job.execute_in_process(instance=DagsterInstance.get())

        job.status = WorkerJobStatus.FINISHED
        job_provider.update(job)

        break


@repository
def indicators_repository():
    jobs = [
        ScheduleDefinition(
            job=update_indicators_job,
            cron_schedule='0 0 * * *',
            default_status=DefaultScheduleStatus.STOPPED
        )
    ]

    jobs.append(
        ScheduleDefinition(
            job=check_jobs,
            cron_schedule='* * * * *',
            default_status=DefaultScheduleStatus.RUNNING
        )
    )

    return jobs
