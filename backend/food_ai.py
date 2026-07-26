import json
import math
import random
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "food_model.pth"
METADATA_PATH = BASE_DIR / "metadata.json"
LOSS_CURVE_PATH = BASE_DIR / "loss_curve.png"

TIME_OPTIONS = ["아침", "점심", "저녁", "간식", "야식"]
PLACE_OPTIONS = ["집밥", "배달", "외식"]
COMPANION_OPTIONS = ["혼밥", "데이트", "가족식사", "모임", "남자끼리", "여자끼리"]
CATEGORY_OPTIONS = ["한식", "중식", "일식", "양식", "남아시아", "동남아시아"]
PRICE_OPTIONS = ["1만원 이하", "1~2만원", "2~3만원", "3만원 이상", "상관없음"]

MENU_ITEMS = [
    # --- 한식 (10종) ---
    {"name": "김치찌개", "category": "한식", "spice": 2, "price": "1만원 이하", "time": ["점심", "저녁"], "place": ["집밥", "외식", "배달"], "tags": ["국물", "따뜻한", "비", "얼큰", "혼밥", "가족식사"]},
    {"name": "된장찌개", "category": "한식", "spice": 0, "price": "1만원 이하", "time": ["아침", "점심", "저녁"], "place": ["집밥", "외식"], "tags": ["국물", "따뜻한", "든든한", "혼밥", "가족식사"]},
    {"name": "비빔밥", "category": "한식", "spice": 1, "price": "1만원 이하", "time": ["점심", "저녁"], "place": ["외식", "집밥"], "tags": ["든든한", "가벼운", "채소", "혼밥"]},
    {"name": "떡볶이", "category": "한식", "spice": 3, "price": "1만원 이하", "time": ["점심", "간식", "야식"], "place": ["배달", "외식"], "tags": ["매운", "분식", "간식", "여자끼리", "치즈"]},
    {"name": "불고기", "category": "한식", "spice": 0, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["집밥", "외식"], "tags": ["고기", "달콤한", "든든한", "가족식사", "모임"]},
    {"name": "제육볶음", "category": "한식", "spice": 2, "price": "1만원 이하", "time": ["점심", "저녁"], "place": ["외식", "배달", "집밥"], "tags": ["매운", "고기", "든든한", "남자끼리", "혼밥"]},
    {"name": "삼겹살", "category": "한식", "spice": 0, "price": "1~2만원", "time": ["저녁", "야식"], "place": ["외식", "집밥"], "tags": ["고기", "든든한", "모임", "남자끼리", "여자끼리"]},
    {"name": "돼지국밥", "category": "한식", "spice": 1, "price": "1만원 이하", "time": ["아침", "점심", "저녁", "야식"], "place": ["외식", "배달"], "tags": ["국물", "따뜻한", "든든한", "혼밥", "남자끼리"]},
    {"name": "냉면", "category": "한식", "spice": 1, "price": "1만원 이하", "time": ["점심", "저녁"], "place": ["외식", "배달"], "tags": ["시원한", "가벼운", "면", "혼밥"]},
    {"name": "닭갈비", "category": "한식", "spice": 2, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식", "배달"], "tags": ["매운", "고기", "모임", "데이트", "치즈"]},

    # --- 중식 (7종) ---
    {"name": "짜장면", "category": "중식", "spice": 0, "price": "1만원 이하", "time": ["점심", "저녁"], "place": ["배달", "외식"], "tags": ["달콤한", "면", "가벼운", "혼밥", "가족식사"]},
    {"name": "짬뽕", "category": "중식", "spice": 3, "price": "1만원 이하", "time": ["점심", "저녁", "야식"], "place": ["배달", "외식"], "tags": ["국물", "얼큰", "매운", "비", "면", "혼밥"]},
    {"name": "마라탕", "category": "중식", "spice": 4, "price": "1~2만원", "time": ["점심", "저녁", "야식"], "place": ["배달", "외식"], "tags": ["매운", "얼얼한", "국물", "여자끼리", "혼밥"]},
    {"name": "탕수육", "category": "중식", "spice": 0, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["배달", "외식"], "tags": ["바삭한", "모임", "달콤한", "가족식사"]},
    {"name": "꿔바로우", "category": "중식", "spice": 0, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["배달", "외식"], "tags": ["바삭한", "달콤한", "데이트", "여자끼리"]},
    {"name": "볶음밥", "category": "중식", "spice": 0, "price": "1만원 이하", "time": ["점심", "저녁"], "place": ["배달", "외식"], "tags": ["든든한", "간단한", "혼밥"]},
    {"name": "딤섬", "category": "중식", "spice": 0, "price": "2~3만원", "time": ["점심", "저녁"], "place": ["외식"], "tags": ["가벼운", "데이트", "모임"]},

    # --- 일식 (7종) ---
    {"name": "초밥", "category": "일식", "spice": 0, "price": "2~3만원", "time": ["점심", "저녁"], "place": ["외식", "배달"], "tags": ["깔끔한", "데이트", "가벼운", "가족식사"]},
    {"name": "라멘", "category": "일식", "spice": 2, "price": "1~2만원", "time": ["점심", "저녁", "야식"], "place": ["외식", "배달"], "tags": ["국물", "따뜻한", "면", "혼밥", "데이트"]},
    {"name": "돈카츠", "category": "일식", "spice": 0, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식", "배달"], "tags": ["바삭한", "든든한", "혼밥", "데이트"]},
    {"name": "우동", "category": "일식", "spice": 0, "price": "1만원 이하", "time": ["아침", "점심", "저녁"], "place": ["외식", "집밥"], "tags": ["국물", "따뜻한", "가벼운", "면", "혼밥"]},
    {"name": "가츠동", "category": "일식", "spice": 0, "price": "1만원 이하", "time": ["점심", "저녁"], "place": ["외식", "배달"], "tags": ["든든한", "단짠", "혼밥"]},
    {"name": "사케동", "category": "일식", "spice": 0, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식"], "tags": ["깔끔한", "데이트", "여자끼리"]},
    {"name": "야키소바", "category": "일식", "spice": 1, "price": "1~2만원", "time": ["점심", "저녁", "야식"], "place": ["외식"], "tags": ["면", "단짠", "데이트", "남자끼리"]},

    # --- 양식 (7종) ---
    {"name": "파스타", "category": "양식", "spice": 1, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식", "배달"], "tags": ["데이트", "부드러운", "면", "여자끼리"]},
    {"name": "피자", "category": "양식", "spice": 1, "price": "2~3만원", "time": ["점심", "저녁", "야식"], "place": ["배달", "외식"], "tags": ["모임", "치즈", "든든한", "가족식사"]},
    {"name": "햄버거", "category": "양식", "spice": 0, "price": "1만원 이하", "time": ["점심", "저녁", "간식"], "place": ["배달", "외식"], "tags": ["빠른", "간단한", "든든한", "혼밥"]},
    {"name": "치킨", "category": "양식", "spice": 1, "price": "2~3만원", "time": ["저녁", "야식"], "place": ["배달", "외식"], "tags": ["바삭한", "모임", "야식", "남자끼리", "여자끼리"]},
    {"name": "스테이크", "category": "양식", "spice": 0, "price": "3만원 이상", "time": ["점심", "저녁"], "place": ["외식"], "tags": ["고기", "데이트", "든든한", "가족식사"]},
    {"name": "리조또", "category": "양식", "spice": 0, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식"], "tags": ["부드러운", "데이트", "치즈"]},
    {"name": "샐러드", "category": "양식", "spice": 0, "price": "1만원 이하", "time": ["아침", "점심", "간식"], "place": ["외식", "배달", "집밥"], "tags": ["가벼운", "채소", "다이어트", "혼밥", "여자끼리"]},

    # --- 남아시아 (5종) ---
    {"name": "일본식 카레", "category": "남아시아", "spice": 1, "price": "1만원 이하", "time": ["점심", "저녁"], "place": ["외식", "배달", "집밥"], "tags": ["따뜻한", "든든한", "혼밥"]},
    {"name": "인도 난과 커리", "category": "남아시아", "spice": 2, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식"], "tags": ["향신료", "데이트", "부드러운", "모임"]},
    {"name": "탄두리치킨", "category": "남아시아", "spice": 2, "price": "2~3만원", "time": ["저녁"], "place": ["외식"], "tags": ["향신료", "고기", "모임", "데이트"]},
    {"name": "버터치킨커리", "category": "남아시아", "spice": 1, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식", "배달"], "tags": ["부드러운", "달콤한", "데이트"]},
    {"name": "비리야니", "category": "남아시아", "spice": 2, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식"], "tags": ["향신료", "든든한", "이색적인"]},

    # --- 동남아시아 (6종) ---
    {"name": "쌀국수", "category": "동남아시아", "spice": 1, "price": "1~2만원", "time": ["아침", "점심", "저녁"], "place": ["외식", "배달"], "tags": ["국물", "따뜻한", "가벼운", "면", "혼밥"]},
    {"name": "팟타이", "category": "동남아시아", "spice": 1, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식", "배달"], "tags": ["면", "새콤한", "가벼운", "데이트"]},
    {"name": "분짜", "category": "동남아시아", "spice": 1, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식"], "tags": ["새콤한", "가벼운", "채소", "고기", "데이트"]},
    {"name": "나시고랭", "category": "동남아시아", "spice": 1, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식", "배달"], "tags": ["든든한", "단짠", "데이트", "혼밥"]},
    {"name": "뿌팟퐁커리", "category": "동남아시아", "spice": 1, "price": "2~3만원", "time": ["점심", "저녁"], "place": ["외식"], "tags": ["부드러운", "모임", "가족식사", "이색적인"]},
    {"name": "똠얌꿍", "category": "동남아시아", "spice": 3, "price": "1~2만원", "time": ["점심", "저녁"], "place": ["외식"], "tags": ["국물", "새콤한", "매운", "이색적인"]},
]

NLP_RULES = {
    "category": {
        "한식": ["한식", "찌개", "국밥", "떡볶이", "비빔밥", "삼겹살", "제육", "냉면"],
        "중식": ["중식", "짜장", "짬뽕", "마라", "탕수육", "꿔바로우", "딤섬"],
        "일식": ["일식", "초밥", "라멘", "우동", "돈카츠", "돈까스", "사케동"],
        "양식": ["양식", "파스타", "피자", "햄버거", "치킨", "스테이크", "샐러드"],
        "남아시아": ["카레", "커리", "난", "인도", "탄두리"],
        "동남아시아": ["쌀국수", "팟타이", "분짜", "베트남", "태국", "나시고랭"],
    },
    "spice": {
        0: ["순한", "안 매운", "안매운", "담백", "안맵게"],
        1: ["살짝 매운", "약간 매운", "신라면", "진라면 매운맛", "순한 매운맛"],
        2: ["보통 매운", "적당히", "중간 매운", "매콤"],
        3: ["얼큰", "칼칼", "알싸"],
        4: ["매운", "맵게", "화끈"],
        5: ["아주 매운", "아주맵게", "극강", "불닭", "마라"],
    },
    "tag": {
        "국물": ["국물", "탕", "찌개"],
        "따뜻한": ["따뜻", "뜨끈", "뜨거운", "추워", "추운", "춥"],
        "시원한": ["시원", "차가운", "더워", "더운", "덥"],
        "비": ["비", "비와", "비도", "비가"],
        "우울": ["우울", "기분이 안", "힘들", "슬픈", "속상", "힘든"],
        "든든한": ["든든", "배고", "배고파", "푸짐"],
        "가벼운": ["가벼운", "간단", "부담", "다이어트"],
        "바삭한": ["바삭", "튀김"],
        "고기": ["고기", "육류"],
        "치즈": ["치즈"],
        "데이트": ["데이트", "연인", "여친", "남친"],
        "모임": ["모임", "같이", "여럿", "회식"],
        "혼밥": ["혼자", "혼밥"],
        "야식": ["야식", "밤", "늦게"],
        "면": ["면", "면요리"],
    },
}

TAG_OPTIONS = list(NLP_RULES["tag"].keys())


class FoodRecommender(nn.Module):
    def __init__(self, input_dim: int, output_dim: int):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.15),
            nn.Linear(64, 48),
            nn.ReLU(),
            nn.Linear(48, output_dim),
        )

    def forward(self, x):
        return self.network(x)


def _one_hot(value, options):
    return [1.0 if value == option else 0.0 for option in options]


def _multi_hot(values, options):
    selected = set(values or [])
    return [1.0 if option in selected else 0.0 for option in options]


def extract_text_features(text: str):
    text = (text or "").strip()
    categories = []
    tags = []
    spice = None

    for category, words in NLP_RULES["category"].items():
        if any(word in text for word in words):
            categories.append(category)

    if any(word in text for word in NLP_RULES["spice"][0]):
        spice = 0
    else:
        for level, words in NLP_RULES["spice"].items():
            if level == 0:
                continue
            if any(word in text for word in words):
                spice = level

    for tag, words in NLP_RULES["tag"].items():
        if any(word in text for word in words):
            tags.append(tag)

    return {"categories": categories, "spice": spice, "tags": tags}


def normalize_request(payload):
    text_features = extract_text_features(payload.get("naturalText", ""))
    categories = list(dict.fromkeys((payload.get("categories") or []) + text_features["categories"]))

    spice = payload.get("spice", 0)
    if text_features["spice"] is not None:
        spice = text_features["spice"]

    return {
        "time": payload.get("time") or "점심",
        "place": payload.get("place") or "외식",
        "companion": payload.get("companion") or "혼밥",
        "categories": categories or ["한식"],
        "spice": int(spice),
        "price": payload.get("price") or "상관없음",
        "text_tags": text_features["tags"],
    }


def encode_features(sample):
    vector = []
    vector += _one_hot(sample["time"], TIME_OPTIONS)
    vector += _one_hot(sample["place"], PLACE_OPTIONS)
    vector += _one_hot(sample["companion"], COMPANION_OPTIONS)
    vector += _multi_hot(sample["categories"], CATEGORY_OPTIONS)
    vector.append(float(sample["spice"]) / 5.0)
    vector += _one_hot(sample["price"], PRICE_OPTIONS)
    vector += _multi_hot(sample.get("text_tags", []), TAG_OPTIONS)
    return vector


def build_metadata():
    input_dim = (
        len(TIME_OPTIONS) + len(PLACE_OPTIONS) + len(COMPANION_OPTIONS) + 
        len(CATEGORY_OPTIONS) + 1 + len(PRICE_OPTIONS) + len(TAG_OPTIONS)
    )
    return {
        "input_dim": input_dim,
        "labels": [item["name"] for item in MENU_ITEMS],
        "time_options": TIME_OPTIONS,
        "place_options": PLACE_OPTIONS,
        "companion_options": COMPANION_OPTIONS,
        "category_options": CATEGORY_OPTIONS,
        "price_options": PRICE_OPTIONS,
        "tag_options": TAG_OPTIONS, 
    }


def _score_sample_against_menu(sample, item):
    score = 0.0
    if item["category"] in sample["categories"]:
        score += 4.0
    if sample["time"] in item["time"]:
        score += 1.3
    if sample["place"] in item["place"]:
        score += 1.2
    if sample["price"] == item["price"] or sample["price"] == "상관없음":
        score += 0.8
    score += max(0.0, 1.5 - abs(sample["spice"] - item["spice"]) * 0.45)
    
    # 동석자 및 자연어 태그 매칭 점수
    if sample["companion"] in item["tags"]:
        score += 1.0
    for tag in sample.get("text_tags", []):
        if any(tag in item_tag for item_tag in item["tags"]):
            score += 1.1
    return score


def choose_label(sample):
    scores = [_score_sample_against_menu(sample, item) for item in MENU_ITEMS]
    best = max(range(len(scores)), key=scores.__getitem__)
    return best


def make_synthetic_dataset(size=6400, seed=42):
    random.seed(seed)
    rows = []
    labels = []
    for _ in range(size):
        sample = {
            "time": random.choice(TIME_OPTIONS),
            "place": random.choice(PLACE_OPTIONS),
            "companion": random.choice(COMPANION_OPTIONS),
            "categories": random.sample(CATEGORY_OPTIONS, k=random.randint(1, 2)),
            "spice": random.randint(0, 5),
            "price": random.choice(PRICE_OPTIONS),
            "text_tags": random.sample(list(NLP_RULES["tag"].keys()), k=random.randint(0, 2)),
        }
        rows.append(encode_features(sample))
        labels.append(choose_label(sample))
    return torch.tensor(rows, dtype=torch.float32), torch.tensor(labels, dtype=torch.long)


def top_k_accuracy(logits, targets, k):
    _, predicted = logits.topk(k, dim=1)
    return predicted.eq(targets.view(-1, 1)).any(dim=1).float().mean().item()


def train_model(epochs=100, batch_size=64, learning_rate=0.003):
    metadata = build_metadata()
    x, y = make_synthetic_dataset()
    train_size = math.floor(len(x) * 0.8)
    x_train, y_train = x[:train_size], y[:train_size]
    x_test, y_test = x[train_size:], y[train_size:]

    model = FoodRecommender(metadata["input_dim"], len(metadata["labels"]))
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()
    loader = DataLoader(TensorDataset(x_train, y_train), batch_size=batch_size, shuffle=True)
    losses = []

    model.train()
    for _ in range(epochs):
        total_loss = 0.0
        for batch_x, batch_y in loader:
            optimizer.zero_grad()
            loss = criterion(model(batch_x), batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(batch_x)
        losses.append(total_loss / len(x_train))

    model.eval()
    with torch.no_grad():
        logits = model(x_test)
        metrics = {
            "loss": criterion(logits, y_test).item(),
            "accuracy": top_k_accuracy(logits, y_test, 1),
            "top3_accuracy": top_k_accuracy(logits, y_test, 3),
            "top5_accuracy": top_k_accuracy(logits, y_test, 5),
        }

    torch.save(model.state_dict(), MODEL_PATH)
    METADATA_PATH.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    save_loss_curve(losses)
    return metrics


def save_loss_curve(losses):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(7, 4))
    plt.plot(range(1, len(losses) + 1), losses)
    plt.title("Cross-Entropy Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.tight_layout()
    plt.savefig(LOSS_CURVE_PATH)
    plt.close()


def load_model():
    if not MODEL_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError("food_model.pth 또는 metadata.json이 없습니다. backend/train_ai.py를 먼저 실행하세요.")
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    model = FoodRecommender(metadata["input_dim"], len(metadata["labels"]))
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()
    return model, metadata


def predict(payload, model, metadata, top_k=5):
    sample = normalize_request(payload)
    temperature = float(payload.get("temperature", 1.0))
    temperature = min(max(temperature, 0.3), 3.0)

    features = torch.tensor([encode_features(sample)], dtype=torch.float32)
    with torch.no_grad():
        logits = model(features)[0] / temperature

    probabilities = torch.softmax(logits, dim=0)

    for index, item in enumerate(MENU_ITEMS):
        if item["category"] in sample["categories"]:
            probabilities[index] += 0.15
            
        if sample["price"] != "상관없음" and item["price"] == sample["price"]:
            probabilities[index] += 0.20
            
        for tag in sample["text_tags"]:
            if any(tag in item_tag for item_tag in item["tags"]):
                probabilities[index] += 0.08
                
    probabilities = probabilities / probabilities.sum()

    values, indices = torch.topk(probabilities, k=top_k)
    return [
        {
            "rank": rank + 1,
            "name": metadata["labels"][index],
            "prob": f"{values[rank].item() * 100:.1f}%",
        }
        for rank, index in enumerate(indices.tolist())
    ]