from fastapi import FastAPI
from pydantic import BaseModel
from .predict import predict_digit
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 設定（フロントホストを適宜置き換え）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-react-app.com", "http://localhost:3000"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class ImageRequest(BaseModel):
    image: str  # data:image/png;base64,...

@app.post("/predict")
async def predict(req: ImageRequest):
    digit, prob = predict_digit(req.image)
    return {"digits": digit, "probs": prob}
