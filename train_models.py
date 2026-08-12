import os
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

os.makedirs("models", exist_ok=True)

print("Loading GTD Dataset...")
df = pd.read_csv(
    "data/globalterrorism.csv", encoding="latin1", low_memory=False
)

print("\n--- Training Attack Prediction Model ---")
categorical_features_attack = [
    "country_txt",
    "region_txt",
    "weaptype1_txt",
    "targtype1_txt",
    "gname",
]
passthrough_features_attack = ["success", "suicide"]
features_attack = categorical_features_attack + passthrough_features_attack
target_attack = "attacktype1_txt"

df_attack = df[features_attack + [target_attack]].dropna()

X_a = df_attack[features_attack]
y_a = df_attack[target_attack]
#Split BEFORE fitting encoders to avoid data leakage
Xa_train, Xa_test, ya_train, ya_test = train_test_split(
    X_a, y_a, test_size=0.20, random_state=42, stratify=y_a
)
#Build preprocessor to handle unknown categories gracefully during inference
preprocessor_attack = ColumnTransformer(
    transformers=[
        (
            "cat",
            OrdinalEncoder(
                handle_unknown="use_encoded_value", unknown_value=-1
            ),
            categorical_features_attack,
        ),
        ("pass", "passthrough", passthrough_features_attack),
    ]
)
#Build complete Pipeline containing both preprocessing and classifier
attack_pipeline = Pipeline([
    ("preprocessor", preprocessor_attack),
    (
        "classifier",
        RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
    ),
])
print("Fitting Attack Prediction Pipeline...")
attack_pipeline.fit(Xa_train, ya_train)

acc_a = accuracy_score(ya_test, attack_pipeline.predict(Xa_test))
print(f"Attack Model Accuracy: {acc_a * 100:.2f}%")

#Dump only the entire pipeline (no separate encoder dictionaries required)
joblib.dump(attack_pipeline, "models/attack_prediction_model.pkl")

print("\n--- Training Threat Level Model ---")
df_threat = (
    df[[
        "country_txt",
        "region_txt",
        "attacktype1_txt",
        "weaptype1_txt",
        "targtype1_txt",
        "nkill",
        "nwound",
    ]]
    .dropna()
    .copy()
)

df_threat["impact"] = df_threat["nkill"] + df_threat["nwound"]

def classify_threat(x):
  if x <= 2:
    return "LOW"
  elif x <= 10:
    return "MEDIUM"
  return "HIGH"

df_threat["threat_level"] = df_threat["impact"].apply(classify_threat)

#Feature separation for Threat Level pipeline
categorical_features_threat = [
    "country_txt",
    "region_txt",
    "attacktype1_txt",
    "weaptype1_txt",
    "targtype1_txt",
]
numeric_features_threat = ["nkill", "nwound"]

X_t = df_threat[categorical_features_threat + numeric_features_threat]
y_t = df_threat["threat_level"]

#Split BEFORE fitting preprocessing pipeline
Xt_train, Xt_test, yt_train, yt_test = train_test_split(
    X_t, y_t, test_size=0.20, random_state=42, stratify=y_t
)
#Define ColumnTransformer for Threat Level
preprocessor_threat = ColumnTransformer(
    transformers=[
        (
            "cat",
            OrdinalEncoder(
                handle_unknown="use_encoded_value", unknown_value=-1
            ),
            categorical_features_threat,
        ),
        ("num", "passthrough", numeric_features_threat),
    ]
)

#Pipeline bundling preprocessor and model
threat_pipeline = Pipeline([
    ("preprocessor", preprocessor_threat),
    (
        "classifier",
        RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
    ),
])
print("Fitting Threat Level Pipeline...")
threat_pipeline.fit(Xt_train, yt_train)

acc_t = accuracy_score(yt_test, threat_pipeline.predict(Xt_test))
print(f"Threat Model Accuracy: {acc_t * 100:.2f}%")
#Save single consolidated pipeline pkl
joblib.dump(threat_pipeline, "models/threat_level_model.pkl")

print("\nModel training complete. Files saved in models/")