import torch
from app.models.model import SimpleModel
from app.storage import ensure_model_store, model_path


def create_and_save():
    ensure_model_store()
    model = SimpleModel()
    # initialize with deterministic weights for the example
    for p in model.parameters():
        torch.nn.init.constant_(p, 0.1)
    path = model_path("sample.pt")
    torch.save(model.state_dict(), path)
    print(f"Saved sample model to {path}")


if __name__ == "__main__":
    create_and_save()
