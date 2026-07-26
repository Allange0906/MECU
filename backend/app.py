from flask import Flask, Response, jsonify, request

from food_ai import load_model, predict


app = Flask(__name__)

model = None
metadata = None


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


@app.route("/predict", methods=["OPTIONS"])
@app.route("/debug/nlp", methods=["OPTIONS"])
def handle_options():
    return Response(status=204)


def ensure_model_loaded():
    global model, metadata
    if model is None or metadata is None:
        model, metadata = load_model()


@app.get("/health")
def health():
    try:
        ensure_model_loaded()
        return jsonify({"ok": True, "labels": len(metadata["labels"])})
    except FileNotFoundError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 503


@app.post("/predict")
def recommend():
    try:
        ensure_model_loaded()
        payload = request.get_json(force=True) or {}
        return json_response(predict(payload, model, metadata))
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 503
    except Exception as exc:
        return jsonify({"error": f"추천 처리 중 오류가 발생했습니다: {exc}"}), 400


@app.post("/debug/nlp")
def debug_nlp():
    from food_ai import extract_text_features, normalize_request

    payload = request.get_json(force=True) or {}
    return json_response(
        {
            "extracted": extract_text_features(payload.get("naturalText", "")),
            "normalized": normalize_request(payload),
        }
    )


def json_response(data, status=200):
    import json

    return Response(
        json.dumps(data, ensure_ascii=False),
        status=status,
        mimetype="application/json; charset=utf-8",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
