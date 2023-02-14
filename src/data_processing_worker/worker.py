from datetime import datetime
from dagster import (
    job,
    op,
    sensor,
    repository,
    ScheduleDefinition,
    DefaultScheduleStatus,
    DefaultSensorStatus,
    RunRequest
)

from data_processing_worker.apps.services import IndicatorService
from data_processing_worker.apps.models.models import Process
from data_processing_worker.apps.models.provider import IndicatorProvider, ProcessProvider
from data_processing_worker.apps.enums import JobStatus


indicator_provider = IndicatorProvider()
indicator_service = IndicatorService()
process_provider = ProcessProvider()


@op(config_schema={'process_id': int})
def update_indicators_op(context):
    process: Process = process_provider.get_by_id(context.op_config['process_id'])

    process.started_at = datetime.now()
    process.status = JobStatus.IN_PROGRESS
    process_provider.update(process)

    indicator_service.update_weights(process.request['limit'], process.request['offset'])
    indicator_service.archive(process.request['limit'], process.request['offset'])
    indicator_service.update_context(process.request['limit'], process.request['offset'])

    process.finished_at = datetime.now()
    process.status = JobStatus.DONE
    process_provider.update(process)


@job
def update_indicators_job():
    update_indicators_op()


@sensor(job=update_indicators_job, default_status=DefaultSensorStatus.RUNNING, minimum_interval_seconds=60)
def check_jobs():
    if process_provider.get_all_by_statuses([JobStatus.IN_PROGRESS]):
        return

    pending_processes = process_provider.get_all_by_statuses([JobStatus.PENDING])

    for process in pending_processes:
        yield RunRequest(
            run_key=f'Update weight {datetime.now()}',
            run_config={
                'ops': {'update_indicators_op': {'config': {'process_id': process.id}}}
            },
        )

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

    jobs.append(check_jobs)

    return jobs
