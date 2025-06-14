import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import torch
import numpy as np
from ml.gated_cnn.gated_cnn_model import GatedCNN

# Dummy input: 10 grayscale 64x64 images
X = torch.rand(10, 1, 64, 64)
y = torch.randint(0, 2, (10,))  # Binary class labels

model = GatedCNN()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

model.train()
for epoch in range(5):
    outputs = model(X)
    loss = criterion(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

torch.save(model.state_dict(), "models/gated_cnn.pt")
print("✅ GatedCNN model saved to models/gated_cnn.pt")
