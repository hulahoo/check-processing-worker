# cron_worker
import logging
import random
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from intelhandler.models import Task, Source, Feed
from worker.services import choose_type

logger = logging.getLogger(__name__)


def source_downloads_worker(source_id):
    obj: Source = Source.objects.get(id=source_id)

    feed_raw = {"feed": {
        "link": obj.path,
        "confidence": random.randint(0, 1000000),
        "source_id": obj.id,
        "format_of_feed": obj.format,
        "name": obj.name
    },

        "raw_indicators": obj.raw_indicators,
        "config": {
            "limit": obj.max_rows,
            "is_instead_full": obj.is_instead_full
        }
    }
    feed = Feed(**feed_raw["feed"])

    method = choose_type(obj.format.lower())
    config = feed_raw.get('config', {})
    result = method(feed, feed_raw['raw_indicators'], config)

    return len(result)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def create_task_scheduler(scheduler, task):
    source = task.source
    update_time_period = source.update_time_period // 1000 if source.update_time_period > 0 else 1

    print(f'add source, interval time {update_time_period}')

    scheduler.add_job(
        source_downloads_worker,
        args=(source.id,),
        trigger=CronTrigger(second=f"*/{update_time_period}"),
        id=f"{source.name}",
        name=source.name,
        max_instances=1,
        replace_existing=False,
    )


def clear_jobs():
    DjangoJobStore().remove_all_jobs()


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()

        scheduler.add_jobstore(DjangoJobStore(), "default")
        clear_jobs()
        return

        tasks = Task.objects.all()
        for task in tasks:
            create_task_scheduler(scheduler, task)
        tasks.update(is_scheduled=True)

        logger.info("Added job 'my_job'.")
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

        while True:
            tasks = Task.objects.filter(is_scheduled=False)
            for task in tasks:
                create_task_scheduler(scheduler, task)
            tasks.update(is_scheduled=True)
            time.sleep(10)
