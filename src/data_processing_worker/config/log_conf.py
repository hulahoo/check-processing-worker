import sys
import logging

from dagster import get_dagster_logger

logger = get_dagster_logger()
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                              datefmt='%H:%M:%S')
console.setFormatter(formatter)

logger.addHandler(console)
