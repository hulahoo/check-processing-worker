import os
import aiohttp
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import BaseCommand

from threatintel.worker.services import chunks
from threatintel.intelhandler.models import Enrichment, Indicator


class Command(BaseCommand):
    help = "Runs consumer."

    def handle(self, *args, **options):
        print("started ")

        scheduler = AsyncIOScheduler()
        enrichments = Enrichment.objects.all()
        tasks = []
        for enrichment in enrichments:
            scheduler.add_job(worker,
                              args=(enrichment,),
                              trigger=CronTrigger(hour="*/1"),
                              replace_existing=False,
                              max_instances=1)
            tasks.append(worker(enrichment))

        scheduler.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))

        try:
            asyncio.get_event_loop().run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass


async def get_from_link_context(link: str, indicator: Indicator):
    try:
        async with aiohttp.ClientSession() as session:
            name = indicator.supplier_name if len(str(indicator.supplier_name)) > 0 else indicator.value

            async with session.get(link.format(name)) as response:
                indicator.enrichment_context = dict(await response.json())
                print(indicator.id, indicator.enrichment_context)
                return indicator
    except Exception as e:
        print(e, indicator.id)


async def worker(enrichment: Enrichment):
    POOL_SIZE = 50
    indicators = Indicator.objects.filter(type=enrichment.type)
    for chunk in chunks(list(indicators), POOL_SIZE):
        await asyncio.gather(*[get_from_link_context(enrichment.link, indicator) for indicator in chunk])
        Indicator.objects.bulk_update(chunk, fields=['enrichment_context'])
