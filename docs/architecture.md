# Architecture Overview

Cirrus Orbit is intentionally small to focus on design patterns for distributed model serving.

Components
- Orchestrator
  - REST API that accepts jobs and uses a scheduler to choose a worker
  - Simple in-memory job-store for development
  - Communicates with workers over HTTP (httpx)
- Worker
  - Loads models from a shared model store (local FS in this reference)
  - Uses PyTorch for inference
  - Exposes a minimal /infer endpoint
- Storage
  - Local filesystem adapter (app/storage.py) for development
  - In production replace with cloud storage client and artifact metadata
- Scheduler
  - Round-robin implemented in app/scheduler.py

Design considerations
- Model loading is cached in-process to reduce I/O and deserialization cost
- Stateless workers simplify horizontal scaling; shared model store recommended
- Orchestrator keeps minimal state and delegates execution; replace with queue for high availability

Operational extensions
- Add health-check endpoints and service discovery for dynamic worker registration
- Use a message queue (Kafka/RabbitMQ) or task queue (Celery/RQ) for resilient orchestration
- Add model metadata (input/output shapes, pre/post-processing) accompanying artifacts
