import itertools
import threading
import uuid
from typing import Iterator

_job_counter = itertools.count()
_job_counter_lock = threading.Lock()

def next_job_id() -> str:
    # thread-safe incrementing job id plus uuid4 to avoid collisions across processes
    with _job_counter_lock:
        idx = next(_job_counter)
    return f"job-{idx}-{uuid.uuid4().hex[:8]}"
