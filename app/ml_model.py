import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = "model.pkl"
ENCODERS_PATH = "encoders.pkl"

# 🔥 GLOBAL CACHE (avoid reloading every time)
model = None
encoders = None


# ================= LOAD MODEL =================
def load_model():
    global model, encoders

    if model is None or encoders is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODERS_PATH):
            print("⚠ Model not found. Training new model...")
            train_model()

        model = joblib.load(MODEL_PATH)
        encoders = joblib.load(ENCODERS_PATH)


# ================= TRAIN MODEL =================
def train_model():
    df = pd.read_csv("data/hr.csv")

    # Convert target
    df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})

    # Features
    features = [
        'Age',
        'MonthlyIncome',
        'JobSatisfaction',
        'WorkLifeBalance',
        'YearsAtCompany',
        'YearsInCurrentRole',
        'YearsSinceLastPromotion',
        'DistanceFromHome',
        'JobRole',
        'Department'
    ]

    df = df[features + ['Attrition']].dropna()

    enc = {}

    # Encode categorical safely
    for col in df.select_dtypes(include='object').columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        enc[col] = le

    X = df[features]
    y = df['Attrition']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model_local = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )

    model_local.fit(X_train, y_train)

    joblib.dump(model_local, MODEL_PATH)
    joblib.dump(enc, ENCODERS_PATH)

    print("✅ ML Model trained & saved!")


# ================= AI EXPLANATION =================
def generate_reason(data, prob):
    reasons = []

    if data.get("MonthlyIncome", 0) < 30000:
        reasons.append("Low salary")

    if data.get("JobSatisfaction", 3) <= 2:
        reasons.append("Low job satisfaction")

    if data.get("WorkLifeBalance", 3) <= 2:
        reasons.append("Poor work-life balance")

    if data.get("DistanceFromHome", 0) > 15:
        reasons.append("Long commute")

    if data.get("YearsAtCompany", 0) > 5 and data.get("JobSatisfaction", 3) <= 2:
        reasons.append("Possible burnout")

    if not reasons:
        return "Stable employee"

    return ", ".join(reasons)


# ================= SAFE ENCODING =================
def safe_encode(df, encoders):
    for col, le in encoders.items():
        if col in df.columns:
            try:
                df[col] = le.transform(df[col].astype(str))
            except:
                df[col] = 0  # fallback for unknown category
    return df


# ================= PREDICT =================
def predict(data_dict):
    load_model()

    df = pd.DataFrame([data_dict])

    # Encode safely
    df = safe_encode(df, encoders)

    expected_features = [
        'Age',
        'MonthlyIncome',
        'JobSatisfaction',
        'WorkLifeBalance',
        'YearsAtCompany',
        'YearsInCurrentRole',
        'YearsSinceLastPromotion',
        'DistanceFromHome',
        'JobRole',
        'Department'
    ]

    # Fill missing values safely
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0

    df = df[expected_features]

    # Prediction
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]

    # Explanation
    reason = generate_reason(data_dict, prob)

    return int(pred), float(prob), reason