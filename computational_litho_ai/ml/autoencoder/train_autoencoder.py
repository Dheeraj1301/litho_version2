import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

class AutoEncoder(nn.Module):
    def __init__(self):
        super(AutoEncoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1), nn.ReLU(),
            nn.Conv2d(32, 16, kernel_size=3, padding=1), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(16, 32, kernel_size=3, padding=1), nn.ReLU(),
            nn.ConvTranspose2d(32, 1, kernel_size=3, padding=1), nn.Sigmoid()
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))

def train_autoencoder(layout_tensor, epochs=10, lr=1e-3):
    model = AutoEncoder()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loader = DataLoader(TensorDataset(layout_tensor), batch_size=8)

    model.train()
    for epoch in range(epochs):
        for batch in loader:
            x = batch[0]
            output = model(x)
            loss = criterion(output, x)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    return model
