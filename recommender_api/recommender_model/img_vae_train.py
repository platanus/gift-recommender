import torch
from torch import nn, optim, Tensor
import pandas as pd
from .image_autoencoder_model import VAE

BATCH_SIZE = 1481
EPOCHS = 100
LOG_INTERVAL = 5


def loss_function(recon_x: Tensor, x: Tensor, mu: Tensor, logvar: Tensor) -> Tensor:
    mean_squared_error = nn.MSELoss()(recon_x, x)
    kl_divergence = torch.sum(mu.pow(2).add_(logvar.exp()).mul_(-1).add_(1).add_(logvar)).mul_(-0.5)
    return mean_squared_error + kl_divergence


if __name__ == '__main__':

    training_set = pd.read_csv('img_vectors.csv').values
    data_loader = torch.utils.data.DataLoader(training_set, batch_size=BATCH_SIZE, shuffle=True)

    model = VAE()
    if torch.cuda.is_available():
        model.cuda()

    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0
        for batch_idx, data in enumerate(data_loader):
            data = data.float()
            optimizer.zero_grad()
            recon_batch, mu, logvar = model(data)
            loss = loss_function(recon_batch, data, mu, logvar)
            loss.backward()
            train_loss += loss.data
            optimizer.step()
            # if batch_idx % LOG_INTERVAL == 0:
            #     print(f'Train Epoch: {epoch} [{batch_idx*len(data)}/{len(data_loader.dataset)}]')
            #     print(f'({100. * batch_idx / len(data_loader):.0f}%)')
            #     print(f'Loss: {loss.data / len(data):.6f}')

        print(f'=====> Epoch: {epoch} Average Loss: {train_loss / len(data_loader.dataset):.6f}')

        if epoch % 10 == 0:
            print('Checkpointing...')
            torch.save(model, 'img_feature_autoencoder.pth.tar')

    torch.save(model, 'img_feature_autoencoder.pth.tar')
