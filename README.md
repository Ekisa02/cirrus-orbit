# Cirrus Orbit

Cirrus Orbit is a reference distributed cloud system for model serving and orchestration built with FastAPI and PyTorch. It demonstrates a clear, modular architecture for distributed inference: an orchestrator that schedules jobs, lightweight workers that load models and run inference, and pluggable storage and scheduling components.

Key features
- FastAPI-based REST endpoints for orchestrator and workers
- Simple round-robin scheduler for worker selection
- PyTorch model definition + loader with caching
- Local storage adapter (extensible to S3, NFS, etc.)
- Example scripts to generate sample model and run services
- Docker Compose example to run orchestrator + multiple workers
- Tests exercising core components

Architecture

  [Client] -> [Orchestrator API] -> [Scheduler] -> [Worker APIs]
                                         |                 |
                                         v                 v
                                    [Job Store]       [Model Store]

- Orchestrator: Accepts job submissions and delegates inference requests to registered workers. Maintains job state and results.
- Worker: Loads PyTorch models (with caching) and performs inference on incoming requests.
- Storage: Local filesystem adapter in this reference; easily replaced with cloud storage client.
- Scheduler: Round-robin scheduler; replaceable for more complex strategies (load-aware, priority, batch-aware, etc.).

Quickstart

Prerequisites
- Python 3.9+
- (Optional) Docker & Docker Compose

1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Create a sample model (writes models/sample.pt)

```bash
python scripts/create_sample_model.py
```

3) Run one or more worker processes (example runs a single worker on port 8001)

```bash
# From repository root
scripts/run_worker.sh 8001
```

4) Run orchestrator (defaults to port 8000)

```bash
scripts/run_orchestrator.sh
```

5) Submit a job (example using curl)

```bash
curl -X POST "http://localhost:8000/submit_job" -H "Content-Type: application/json" \
  -d '{"model": "sample.pt", "input": [0.1, 0.2, 0.3]}'
```

This will return a job id. Poll job status:

```bash
curl http://localhost:8000/status/<job_id>
```

Docker Compose

A sample docker-compose.yml is included to run one orchestrator and two workers locally. Ensure you have created the sample model before starting compose or mount a model artifact into the workers.

Extending
- Replace storage/local adapter with a cloud-backed implementation (e.g., S3) in app/storage.py
- Implement more advanced scheduling in app/scheduler.py
- Add batching and model warm-start functionality in workers

Repository layout

- app/: application modules (orchestrator, worker, model loader, scheduler, storage)
- scripts/: convenience scripts for producing a sample model and launching services
- tests/: pytest tests
- docs/: additional architecture and usage details

License

MIT
