import torch
import torch.nn as nn

class GatedCNN(nn.Module):
    def __init__(self):
        super(GatedCNN, self).__init__()
        self.conv = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.gate = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.fc = nn.Linear(32 * 64 * 64, 2)

    def forward(self, x):
        conv_out = torch.relu(self.conv(x))
        gated = torch.sigmoid(self.gate(x))
        x = conv_out * gated
        x = x.view(x.size(0), -1)
        return self.fc(x)

def predict_layout_class(model, layout_tensor):
    model.eval()
    with torch.no_grad():
        logits = model(layout_tensor)
        predicted_class = torch.argmax(logits, dim=1)
    return predicted_class.item()
