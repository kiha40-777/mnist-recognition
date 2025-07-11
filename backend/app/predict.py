import base64, cv2, numpy as np, torch, torch.nn.functional as F
from .model import DigitCNN

# アプリ起動時に一度だけモデルを読み込む
model = DigitCNN()
model.load_state_dict(torch.load("app/mnist_cnn.pth", map_location="cpu"))
model.eval()

def predict_digit(data_url: str):
    # Base64→NumPy→28×28グレースケール
    b = data_url.split(",")[1]
    img = np.frombuffer(base64.b64decode(b), np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (28, 28))
    tensor = torch.from_numpy(img).unsqueeze(0).unsqueeze(0).float() / 255.0
    with torch.no_grad():
        out = model(tensor)
        prob_list = torch.softmax(out, dim=1)[0]

        sorted_probs, sorted_idx = prob_list.sort(descending=True)
        pred_list = sorted_idx.tolist()
        prob_list = sorted_probs.tolist()

    return pred_list, prob_list
