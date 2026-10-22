from typing import List

# Default settings for development/demo. For production, override via env or config file.
ORCHESTRATOR_HOST = "0.0.0.0"
ORCHESTRATOR_PORT = 8000

# Worker default port if launched standalone
DEFAULT_WORKER_PORT = 8001

# Where model artifacts live in this reference repository
MODEL_STORE_DIR = "models"

# Default known workers for orchestrator at startup. In production, worker discovery would be dynamic.
DEFAULT_WORKERS: List[str] = ["http://localhost:8001"]
