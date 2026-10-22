import asyncio
import os
import pytest
from fastapi.testclient import TestClient
from app.worker_api import app as worker_app
from app.main import app as orchestrator_app
from app.storage import ensure_model_store, model_path
import torch
from app.models.model import SimpleModel


@pytest.fixture(scope="module")
def sample_model_file(tmp_path_factory):
    # Ensure a model is available in the repository models/ directory.
    # Create a model file at models/sample.pt (used by worker)
    ensure_model_store()
    path = model_path("sample.pt")
    model = SimpleModel()
    for p in model.parameters():
        torch.nn.init.constant_(p, 0.2)
    torch.save(model.state_dict(), path)
    return path


def test_worker_infer(sample_model_file):
    client = TestClient(worker_app)
    resp = client.post("/infer", json={"model": "sample.pt", "input": [0.1, 0.2, 0.3]})
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["ok"] is True
    assert "output" in payload


def test_orchestrator_submit_and_status(monkeypatch):
    # Start worker test client and make orchestrator pick it by registering
    worker_client = TestClient(worker_app)
    orch_client = TestClient(orchestrator_app)

    # Register worker in orchestrator (use a local URL handled by TestClient)
    # The orchestrator uses httpx to call the worker; to integrate easily we mock the httpx client
    import app.main as main_mod
    class DummyResponse:
        def __init__(self, json_data, status_code=200):
            self._json = json_data
            self.status_code = status_code
        def json(self):
            return self._json
        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception(f"HTTP {self.status_code}")

    async def fake_post(url, json):
        # route to test client endpoints
        if url.endswith('/infer'):
            r = worker_client.post('/infer', json=json)
            return DummyResponse(r.json(), r.status_code)
        return DummyResponse({"error": "unknown"}, status_code=404)

    monkeypatch.setattr(main_mod, 'client', type('C', (), {'post': staticmethod(fake_post)})())
    # Replace scheduler workers list with a dummy URL (not actually used by fake_post)
    main_mod.scheduler = main_mod.scheduler.__class__(workers=['http://test-worker'])

    resp = orch_client.post('/submit_job', json={"model": "sample.pt", "input": [0.5,0.5,0.5]})
    assert resp.status_code == 200
    job_id = resp.json()["job_id"]

    # check status
    status_resp = orch_client.get(f'/status/{job_id}')
    assert status_resp.status_code == 200
    data = status_resp.json()
    assert data["status"] in ("done", "failed")
