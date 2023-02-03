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
from data_processing_worker.apps.models.provider import IndicatorProvider, ProcessProvider
from data_processing_worker.apps.enums import JobStatus


indicator_provider = IndicatorProvider()
indicator_service = IndicatorService()
process_provider = ProcessProvider()


@op
def update_indicators_op():
    indicator_service.update_weights()

@job
def update_indicators_job():
    update_indicators_op()


@job(name='check_jobs')
def check_jobs():
    if process_provider.get_all_by_statuses([JobStatus.IN_PROGRESS]):
        return

    pending_processes = process_provider.get_all_by_statuses([JobStatus.PENDING])

    for process in pending_processes:
        process.started_at = datetime.now()
        process.status = JobStatus.IN_PROGRESS
        process_provider.update(process)

        update_indicators_job.execute_in_process(instance=DagsterInstance.get())

        process.finished_at = datetime.now()
        process.status = JobStatus.DONE
        process_provider.update(process)

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
