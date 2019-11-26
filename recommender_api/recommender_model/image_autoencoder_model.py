from torch import nn, Tensor
from typing import Tuple

ZDIMS = 20  # Number of output dimensions


class VAE(nn.Module):
    def __init__(self, zdims: int = ZDIMS):
        super(VAE, self).__init__()
        self.zdims = zdims

        # Encoder
        self.input_to_hidden = nn.Linear(1280, 640)
        self.relu = nn.ReLU()
        self.mu = nn.Linear(640, self.zdims)
        self.logvar = nn.Linear(640, self.zdims)

        # Decoder
        self.bottleneck_to_hidden = nn.Linear(self.zdims, 640)
        self.hidden_to_output = nn.Linear(640, 1280)
        self.sigmoid = nn.Sigmoid()

    def encode(self, x: Tensor) -> Tuple[Tensor, Tensor]:
        hidden: Tensor = self.relu(self.input_to_hidden(x))
        return self.mu(hidden), self.logvar(hidden)

    def reparameterize(self, mu: Tensor, logvar: Tensor) -> Tensor:
        if self.training:
            std: Tensor = logvar.mul(0.5).exp_()
            eps: Tensor = Tensor(std.data.new(std.size()).normal_())
            return eps.mul(std).add_(mu)
        else:
            return mu

    def decode(self, z: Tensor) -> Tensor:
        hidden: Tensor = self.relu(self.bottleneck_to_hidden(z))
        return self.sigmoid(self.hidden_to_output(hidden))

    def forward(self, x: Tensor) -> Tuple[Tensor, Tensor, Tensor]:
        mu, logvar = self.encode(x)
        z: Tensor = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar
