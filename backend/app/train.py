import torch
from torch import nn, optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
from model import DigitCNN

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

lr = 0.001
batch_size = 64
n_epochs = 5

# --- データセットの準備 ---
transform = transforms.Compose([
    transforms.ToTensor(),                                   # [0,255] → [0.0,1.0]
    transforms.Normalize((0.1307,), (0.3081,))               # 平均0.1307, 標準偏差0.3081で標準化
])

# 学習用セット（60,000枚）
train_dataset = datasets.MNIST(
    root="data",        # データ保存先フォルダ
    train=True,         # 学習用データを取得
    download=True,      # 未取得なら自動ダウンロード
    transform=transform # 上で定義した前処理を適用
)

# テスト用セット（10,000枚）
test_dataset = datasets.MNIST(
    root="data",
    train=False,
    download=True,
    transform=transform
)

val_size = 5000
train_size = len(train_dataset) - val_size
train_subset, val_subset = random_split(train_dataset, [train_size, val_size])

train_loader = DataLoader(
    train_subset if 'train_subset' in locals() else train_dataset,
    batch_size=batch_size,
    shuffle=True,       # 毎エポックごとにシャッフル
    num_workers=4       # CPU コア数に応じて調整
)

val_loader = DataLoader(
    val_subset,
    batch_size=batch_size,
    shuffle=False,
    num_workers=4
)

test_loader = DataLoader(
    test_dataset,
    batch_size=batch_size,
    shuffle=False,
    num_workers=4
)

model = DigitCNN().to(device)
optimizer = optim.Adam(model.parameters(), lr=lr)
criterion = nn.CrossEntropyLoss()

def train(model, train_loader, optimizer, criterion):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    epoch_loss = running_loss / len(train_loader.dataset)
    epoch_acc = correct / total
    return epoch_loss, epoch_acc

def validate(model, val_loader, criterion):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    epoch_loss = running_loss / len(val_loader.dataset)
    epoch_acc = correct / total
    return epoch_loss, epoch_acc

def test(model, test_loader):
    with torch.no_grad():
        model.eval()
        correct = 0
        total = 0
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = correct / total
    print(f"Test Accuracy: {accuracy:.2%}")
    return accuracy

def main():

    for epoch in range(n_epochs):
        train_loss, train_acc = train(model, train_loader, optimizer, criterion)
        val_loss, val_acc = validate(model, val_loader, criterion)

        print(f"Epoch [{epoch+1}/{n_epochs}], "
            f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2%}, "
            f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2%}")
        
    torch.save(model.state_dict(), "../mnist_cnn.pth")
    test(model, test_loader)
    
if __name__ == '__main__':
    # Windows 互換／凍結対応（macOS でも無害）
    from multiprocessing import freeze_support
    freeze_support()

    main()
