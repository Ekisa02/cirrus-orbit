# Usage

Creating a sample model

```bash
python scripts/create_sample_model.py
```

Running locally (development)

Start a worker:

```bash
scripts/run_worker.sh 8001
```

Start orchestrator:

```bash
scripts/run_orchestrator.sh 8000
```

Submit a job:

```bash
curl -X POST http://localhost:8000/submit_job -H "Content-Type: application/json" \
  -d '{"model": "sample.pt", "input": [0.1,0.2,0.3]}'
```

Using Docker Compose

```bash
docker compose up --build
```

(Ensure models/sample.pt is created or bind-mount a directory with the model into the worker containers.)
