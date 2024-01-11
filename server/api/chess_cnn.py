import torch
import torch.nn as nn
import torch.nn.functional as F


class ChessCNN(nn.Module):
    def __init__(self):
        super(ChessCNN, self).__init__()
        # Defined CNN architecture here
        self.conv1 = nn.Conv2d(in_channels=15, out_channels=64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 128)
        self.fc2 = nn.Linear(128, 1)

    def forward(self, x):
        # Define the forward pass
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(-1, 128 * 8 * 8)  # Flatten the tensor for the fully connected layer
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
