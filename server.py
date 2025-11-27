# server.py
from flask import Flask, request, jsonify
import joblib
import os
import numpy as np

MODEL_FILE = "audio_model.joblib"

app = Flask(__name__)
model = None

if os.path.exists(MODEL_FILE):
    try:
        model = joblib.load(MODEL_FILE)
        print("Loaded model:", MODEL_FILE)
    except Exception as e:
        print("Failed to load model:", e)

@app.route("/classify", methods=["POST"])
def classify():
    global model
    j = request.get_json(force=True)
    # expected features: rms, ptp, mean_abs, zcr, do_count, do
    feat = np.array([[ 
        float(j.get("rms", 0.0)),
        int(j.get("ptp", 0)),
        float(j.get("mean_abs", 0.0)),
        float(j.get("zcr", 0.0)),
        int(j.get("do_count", 0)),
        int(j.get("do", 0))
    ]])
    if model is None:
        return jsonify({"label": "unknown", "conf": 0.0})
    probs = model.predict_proba(feat)[0]
    idx = int(np.argmax(probs))
    label = model.classes_[idx]
    conf = float(probs[idx])
    return jsonify({"label": str(label), "conf": conf})

if __name__ == "__main__":
    print("Starting server on port 5000")
    app.run(host="0.0.0.0", port=5000)
