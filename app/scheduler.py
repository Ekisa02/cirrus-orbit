from typing import List, Optional
import itertools

class RoundRobinScheduler:
    """Simple round-robin scheduler for worker endpoints."""
    def __init__(self, workers: Optional[List[str]] = None):
        self.workers = list(workers) if workers else []
        self._iter = itertools.cycle(self.workers) if self.workers else None

    def register(self, worker_url: str):
        if worker_url not in self.workers:
            self.workers.append(worker_url)
            self._iter = itertools.cycle(self.workers)

    def unregister(self, worker_url: str):
        if worker_url in self.workers:
            self.workers.remove(worker_url)
            self._iter = itertools.cycle(self.workers) if self.workers else None

    def pick(self) -> Optional[str]:
        if not self._iter:
            return None
        return next(self._iter)
