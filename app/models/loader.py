import os
from functools import lru_cache
from typing import Optional
import torch
from .model import SimpleModel
from app.config import MODEL_STORE_DIR


@lru_cache(maxsize=8)
def load_model(filename: str, device: Optional[str] = None) -> SimpleModel:
    """Load a model from the local model store and return a constructed PyTorch model with state loaded.

    This function uses an LRU cache to avoid repeatedly re-loading model weights in a single process.
    """
    if device is None:
        device = "cpu"
    path = os.path.join(MODEL_STORE_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")

    # Create model instance with expected shape. In a real system, store metadata with the artifact.
    model = SimpleModel()
    state = torch.load(path, map_location=device)
    model.load_state_dict(state)
    model.eval()
    return model
