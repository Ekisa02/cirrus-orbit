#!/usr/bin/env bash
set -euo pipefail
PORT=${1:-8001}
# Launch worker with uvicorn in the foreground
uvicorn app.worker_api:app --host 0.0.0.0 --port ${PORT}
