# Mecommender AI Backend

이 서버는 Flutter 앱의 설문 입력과 자연어 문장을 받아 음식 추천 결과를 반환합니다.

## 실행 순서

```powershell
cd C:\Users\junyi\Flutter_Projects\mecommender\backend
python -m pip install -r requirements.txt
python train_ai.py
python app.py
```

`train_ai.py`를 실행하면 다음 파일이 생성됩니다.

- `food_model.pth`: PyTorch 모델 가중치
- `metadata.json`: 원-핫 인코딩 범주와 음식 라벨
- `loss_curve.png`: Cross-Entropy Loss 학습 곡선

서버 주소는 `http://127.0.0.1:5050`입니다.

## 학술적 보완 포인트

- 범주형 입력을 단순 정수로 바꾸지 않고 원-핫/멀티-핫 인코딩으로 변환해 순서성 편향을 줄였습니다.
- Cross-Entropy Loss, Accuracy, Top-3 Accuracy, Top-5 Accuracy를 출력해 추천 모델을 정량 평가합니다.
- 자연어 문장에서 `국물`, `얼큰`, `비`, `매운` 같은 키워드를 추출해 정형 피처로 연결합니다.
- `temperature` 값으로 Softmax 분포의 날카로움을 조절해 추천의 다양성과 확정성 사이의 균형을 조절합니다.
