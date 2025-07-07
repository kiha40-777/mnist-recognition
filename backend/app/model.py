import torch
import torch.nn as nn
import torch.nn.functional as F

class DigitCNN(nn.Module):
    def __init__(self):
        super(DigitCNN, self).__init__()
        # 畳み込み層1: 入力チャネル1 → 出力チャネル32
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        # 畳み込み層2: 32 → 64
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        # プーリング後に全結合層へ
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # x: (batch, 1, 28, 28)
        x = F.relu(self.conv1(x))     # → (batch, 32, 28, 28)
        x = F.max_pool2d(x, 2)        # → (batch, 32, 14, 14)
        x = F.relu(self.conv2(x))     # → (batch, 64, 14, 14)
        x = F.max_pool2d(x, 2)        # → (batch, 64, 7, 7)
        x = x.view(-1, 64 * 7 * 7)    # flatten
        x = F.relu(self.fc1(x))       # → (batch, 128)
        x = self.fc2(x)               # → (batch, 10)
        return x
