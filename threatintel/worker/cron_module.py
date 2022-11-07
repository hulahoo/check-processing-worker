from django.conf import settings
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

from intelhandler.models import Source


def cron_init(func, source: Source):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    time = int(source.update_time_period / 1000)
    print('time', time)

    scheduler.add_job(
        func,
        trigger=CronTrigger(second=f"*/{time}"),
        id=f"{source.name}",
        name=source.name,
        max_instances=1,
        replace_existing=True,
    )
    # scheduler.start()
    register_events(scheduler)
