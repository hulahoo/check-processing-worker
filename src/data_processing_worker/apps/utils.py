import time
from functools import wraps

from data_processing_worker.config.log_conf import logger


def benchmark(fn):
    @wraps(fn)
    def with_profiling(*args, **kwargs):
        logger.info(f"Profiling of: {fn.__name__} function")
        start_time = time.time()
        ret = fn(*args, **kwargs)

        elapsed_time = time.time() - start_time

        logger.info(f"{fn.__name__} finished in {elapsed_time}")

        return ret
    return with_profiling
