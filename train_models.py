import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

os.makedirs("models", exist_ok=True)

print("Loading GTD Dataset...")
df = pd.read_csv(
    "data/globalterrorism.csv", encoding="latin1", low_memory=False
)

print("\n--- Training Attack Prediction Model ---")
features_attack = [
    "country_txt",
    "region_txt",
    "weaptype1_txt",
    "targtype1_txt",
    "gname",
    "success",
    "suicide",
]
target_attack = "attacktype1_txt"

df_attack = df[features_attack + [target_attack]].dropna()

encoders_attack = {}
for col in ["country_txt", "region_txt", "weaptype1_txt", "targtype1_txt", "gname"]:
  le = LabelEncoder()
  df_attack[col] = le.fit_transform(df_attack[col])
  encoders_attack[col] = le

target_encoder_attack = LabelEncoder()
df_attack[target_attack] = target_encoder_attack.fit_transform(
    df_attack[target_attack]
)

X_a = df_attack[features_attack]
y_a = df_attack[target_attack]

Xa_train, Xa_test, ya_train, ya_test = train_test_split(
    X_a, y_a, test_size=0.20, random_state=42
)

model_attack = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
model_attack.fit(Xa_train, ya_train)

acc_a = accuracy_score(ya_test, model_attack.predict(Xa_test))
print(f"Attack Model Accuracy: {acc_a * 100:.2f}%")

joblib.dump(model_attack, "models/attack_prediction_model.pkl")
joblib.dump(encoders_attack, "models/feature_encoders.pkl")
joblib.dump(target_encoder_attack, "models/target_encoder.pkl")

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

encoders_threat = {}
for col in [
    "country_txt",
    "region_txt",
    "attacktype1_txt",
    "weaptype1_txt",
    "targtype1_txt",
]:
  le = LabelEncoder()
  df_threat[col] = le.fit_transform(df_threat[col])
  encoders_threat[col] = le

target_encoder_threat = LabelEncoder()
df_threat["threat_level"] = target_encoder_threat.fit_transform(
    df_threat["threat_level"]
)

X_t = df_threat.drop(columns=["threat_level", "impact"])
y_t = df_threat["threat_level"]

Xt_train, Xt_test, yt_train, yt_test = train_test_split(
    X_t, y_t, test_size=0.20, random_state=42
)

model_threat = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
model_threat.fit(Xt_train, yt_train)

acc_t = accuracy_score(yt_test, model_threat.predict(Xt_test))
print(f"Threat Model Accuracy: {acc_t * 100:.2f}%")

joblib.dump(model_threat, "models/threat_level_model.pkl")
joblib.dump(encoders_threat, "models/threat_encoders.pkl")
joblib.dump(target_encoder_threat, "models/threat_target_encoder.pkl")

print("\nModel training complete. Files saved in models/")