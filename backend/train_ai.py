from food_ai import LOSS_CURVE_PATH, METADATA_PATH, MODEL_PATH, train_model


if __name__ == "__main__":
    metrics = train_model()
    print("모델 학습 완료")
    print(f"- model: {MODEL_PATH}")
    print(f"- metadata: {METADATA_PATH}")
    print(f"- loss curve: {LOSS_CURVE_PATH}")
    print(f"- loss: {metrics['loss']:.4f}")
    print(f"- accuracy: {metrics['accuracy'] * 100:.2f}%")
    print(f"- top-3 accuracy: {metrics['top3_accuracy'] * 100:.2f}%")
    print(f"- top-5 accuracy: {metrics['top5_accuracy'] * 100:.2f}%")
