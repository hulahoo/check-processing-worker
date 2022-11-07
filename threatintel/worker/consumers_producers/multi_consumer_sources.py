import json

from dagster import op, job, get_dagster_logger, Field, DynamicOut, DynamicOutput
from kafka import KafkaConsumer, TopicPartition


@op(config_schema={'partitions': Field(list)}, out=DynamicOut())
def consumer_dispatcher_op(context):
    partitions = context.op_config['partitions']

    for partition in partitions:
        yield DynamicOutput(
            value=partition,
            mapping_key=f'partition_{partition}'
        )


@op
def consumer_collector(data):
    return len(data)


def event_worker(data: dict):
    from intelhandler.models import Source
    from intelhandler.models import Task

    # feed: Feed()
    source = Source(**data)
    source.save()
    Task.objects.get_or_create(source_id=source.pk)


@op
def op_consumer(context, partition: int):
    from django.conf import settings
    logger = get_dagster_logger()
    group_id = settings.KAFKA_GROUP_ID
    kafka_ip = settings.KAFKA_IP
    topic = settings.KAFKA_TOPIC

    kafka_consumer = KafkaConsumer(
        bootstrap_servers={f'{kafka_ip}:9092'},
        auto_offset_reset='earliest',
        group_id=group_id,
    )
    topic_partition = TopicPartition(topic, partition)
    topics = [topic_partition]
    kafka_consumer.assign(topics)
    while True:
        for tp, messages in tuple(kafka_consumer.poll(timeout_ms=5000).items()):
            for message in messages:
                data = json.loads(message.value)
                logger.info(f'{data}')
                event_worker(data)


@job
def job_consumer():
    results = consumer_dispatcher_op().map(op_consumer)
    consumer_collector(results.collect())
