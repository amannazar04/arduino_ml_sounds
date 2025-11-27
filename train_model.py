# train_model.py
import pandas as pd
import joblib
import os
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

FN = "samples.csv"
MODEL_FILE = "audio_model.joblib"
REQ_FEATS = ["rms","ptp","mean_abs","zcr","do_count","do"]

def load_csv(fn):
    try:
        df = pd.read_csv(fn)
        return df
    except Exception:
        try:
            df = pd.read_csv(fn, encoding="utf-8-sig")
            return df
        except Exception as e:
            print("Failed to read CSV:", e)
            sys.exit(1)

def main():
    if not os.path.exists(FN):
        print("No samples.csv found. Run collect_data.py first.")
        sys.exit(1)
    df = load_csv(FN)
    print("Columns found:", list(df.columns))
    # ensure required columns exist
    missing = [c for c in REQ_FEATS if c not in df.columns]
    if missing:
        print("Missing columns:", missing)
        print("Expected:", REQ_FEATS, "plus 'label'")
        sys.exit(1)
    if "label" not in df.columns:
        print("'label' column missing.")
        sys.exit(1)

    df = df.dropna(subset=REQ_FEATS+["label"])
    X = df[REQ_FEATS].astype(float).values
    y = df["label"].astype(str).values
    if len(y) < 10:
        print("Not enough samples to train. Need at least 10 samples total.")
        sys.exit(1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)
    print("Train accuracy:", clf.score(X_train, y_train))
    print("Test accuracy:", clf.score(X_test, y_test))
    joblib.dump(clf, MODEL_FILE)
    print("Saved model to", MODEL_FILE)

if __name__ == "__main__":
    main()
