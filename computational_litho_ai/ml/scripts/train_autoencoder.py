import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import torch
import numpy as np
from ml.autoencoder.train_autoencoder import AutoEncoder, train_autoencoder




# Dummy input: 10 grayscale images of size 64x64
dummy_input = torch.rand(10, 1, 64, 64)

print("✅ Starting training...")
model = train_autoencoder(dummy_input, epochs=3)
print("✅ Training done!")

# ✅ Ensure directory exists
os.makedirs("models", exist_ok=True)

# ✅ Save model
torch.save(model.state_dict(), "models/autoencoder.pt")
print("✅ Model saved to models/autoencoder.pt")
