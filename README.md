# mecommender

Flutter 앱과 Flask/PyTorch 서버를 연결한 음식 추천 프로젝트입니다.

## AI 보완 내용

- 범주형 입력을 정수 라벨이 아니라 원-핫/멀티-핫 인코딩으로 처리합니다.
- 학습 후 Cross-Entropy Loss, Accuracy, Top-3 Accuracy, Top-5 Accuracy를 출력합니다.
- `loss_curve.png`를 저장해 학습 손실 감소 과정을 시각화합니다.
- 자연어 문장에서 음식 선호 키워드를 추출해 추천 피처로 변환합니다.
- Softmax Temperature Scaling으로 추천의 확정성과 다양성을 조절합니다.

## 서버 실행

```powershell
cd C:\Users\junyi\Flutter_Projects\mecommender\backend
python -m pip install -r requirements.txt
python train_ai.py
python app.py
```

서버가 켜진 뒤 Flutter 앱에서 설문을 입력하면 `http://127.0.0.1:5050/predict`로 추천 요청을 보냅니다.
기존에 5000번 포트에서 예전 Flask 서버가 실행 중이어도 충돌하지 않도록 새 서버는 5050번 포트를 사용합니다.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.
