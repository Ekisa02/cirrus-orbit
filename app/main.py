import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from typing import Dict, Any

from app.config import DEFAULT_WORKERS
from app.scheduler import RoundRobinScheduler
from app.utils import next_job_id

app = FastAPI(title="cirrus-orbit-orchestrator")

# Simple in-memory job store; replace with persistent store in production
job_store: Dict[str, Dict[str, Any]] = {}

scheduler = RoundRobinScheduler(DEFAULT_WORKERS)

client = httpx.AsyncClient(timeout=10.0)

class SubmitRequest(BaseModel):
    model: str
    input: list


@app.post("/submit_job")
async def submit_job(req: SubmitRequest):
    job_id = next_job_id()
    job_store[job_id] = {"status": "queued", "result": None}

    worker_url = scheduler.pick()
    if not worker_url:
        job_store[job_id]["status"] = "failed"
        raise HTTPException(status_code=503, detail="No workers registered")

    job_store[job_id]["status"] = "running"

    # Fire-and-forget orchestration (we still await here to provide synchronous result)
    try:
        r = await client.post(f"{worker_url}/infer", json={"model": req.model, "input": req.input})
        r.raise_for_status()
        payload = r.json()
        job_store[job_id]["status"] = "done"
        job_store[job_id]["result"] = payload
    except Exception as exc:
        job_store[job_id]["status"] = "failed"
        job_store[job_id]["result"] = {"error": str(exc)}

    return {"job_id": job_id}


@app.get("/status/{job_id}")
async def status(job_id: str):
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="job not found")
    return job_store[job_id]


@app.get("/workers")
async def workers():
    return {"workers": scheduler.workers}


@app.post("/workers/register")
async def register_worker(payload: Dict[str, str]):
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="missing url")
    scheduler.register(url)
    return {"registered": url}
