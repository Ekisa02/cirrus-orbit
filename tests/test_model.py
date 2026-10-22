import torch
from app.models.model import SimpleModel


def test_model_forward():
    model = SimpleModel(input_dim=3, hidden_dim=4, output_dim=1)
    x = torch.randn(2,3)
    out = model(x)
    assert out.shape == (2,1)
