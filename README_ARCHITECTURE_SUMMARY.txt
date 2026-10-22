Orchestrator -> Scheduler (RoundRobin) -> Worker(s)
Workers load models from MODEL_STORE_DIR (local FS) and expose /infer
Model loading is cached via lru_cache in app/models/loader.py
