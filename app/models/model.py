import torch
import torch.nn as nn

class SimpleModel(nn.Module):
    """A tiny demonstration model: a single hidden linear layer with ReLU."""
    def __init__(self, input_dim: int = 3, hidden_dim: int = 8, output_dim: int = 1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
