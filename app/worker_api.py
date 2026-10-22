from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
import torch

from app.models.loader import load_model
from app.storage import list_models

app = FastAPI(title="cirrus-orbit-worker")

class InferRequest(BaseModel):
    model: str
    input: List[float]


@app.post("/infer")
async def infer(req: InferRequest):
    # verify model exists in local storage
    if req.model not in list_models():
        raise HTTPException(status_code=404, detail=f"model {req.model} not found on worker")

    try:
        model = load_model(req.model)
        # convert input to tensor, ensure batch dimension
        x = torch.tensor(req.input, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            out = model(x)
        # convert to python types
        out_list = out.squeeze(0).tolist()
        if isinstance(out_list, float):
            out_list = [out_list]
        return {
            "ok": True,
            "model": req.model,
            "output": out_list,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/models")
async def models():
    return {"models": list_models()}
