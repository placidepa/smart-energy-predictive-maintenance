import torch
import torch.nn as nn

class AnomalyAutoencoder(nn.Module):
    def __init__(self, input_features=3, window_size=60):
        super(AnomalyAutoencoder, self).__init__()
        self.input_dim = input_features * window_size
        
        # Encoder: Compress the electrical signature
        self.encoder = nn.Sequential(
            nn.Linear(self.input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16) # Latent space
        )
        
        # Decoder: Attempt to reconstruct normal behavior
        self.decoder = nn.Sequential(
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, self.input_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = x.view(x.size(0), -1) # Flatten the time-series window
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded.view(x.size(0), -1, 3) # Reshape back to window size