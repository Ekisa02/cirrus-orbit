import os
from typing import List
from app.config import MODEL_STORE_DIR


def ensure_model_store():
    os.makedirs(MODEL_STORE_DIR, exist_ok=True)


def list_models() -> List[str]:
    ensure_model_store()
    return [f for f in os.listdir(MODEL_STORE_DIR) if os.path.isfile(os.path.join(MODEL_STORE_DIR, f))]


def model_path(name: str) -> str:
    ensure_model_store()
    return os.path.join(MODEL_STORE_DIR, name)
