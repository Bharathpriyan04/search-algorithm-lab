"""
train_model.py
===============
STEP 1 — RUN THIS FIRST.

This trains the dropout-risk model and saves everything the app needs
into a single file: dropout_model_bundle.pkl

Where to run this:
- Google Colab (recommended, free): colab.research.google.com -> New Notebook
  -> upload this file or paste its contents into a cell -> Run
- Kaggle Notebooks (also free): kaggle.com/code -> New Notebook
- Or locally, after: pip install -r requirements_training.txt

After it finishes, DOWNLOAD "dropout_model_bundle.pkl" from the Colab file
panel (left sidebar -> folder icon -> right-click the file -> Download).
Put that file in the SAME folder as app.py before you run/deploy the app.
"""

import sys
import subprocess
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, f1_score

# ---------------------------------------------------------------------
# 1. Load the dataset (UCI ML Repo id=697 — Predict Students' Dropout
#    and Academic Success). No manual download needed.
# ---------------------------------------------------------------------
try:
    from ucimlrepo import fetch_ucirepo
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "ucimlrepo"])
    from ucimlrepo import fetch_ucirepo

print("Downloading dataset from UCI ML Repository (id=697)...")
dataset = fetch_ucirepo(id=697)
X = dataset.data.features.copy()
y_raw = dataset.data.targets.copy()

target_col = y_raw.columns[0]
y_text = y_raw[target_col]

print(f"\nLoaded {X.shape[0]} students, {X.shape[1]} features.")
print("Class distribution:")
print(y_text.value_counts())

# ---------------------------------------------------------------------
# 2. Encode the target: Dropout / Enrolled / Graduate -> 0 / 1 / 2
# ---------------------------------------------------------------------
le = LabelEncoder()
y = le.fit_transform(y_text)
class_names = list(le.classes_)
print("\nLabel mapping:", dict(zip(class_names, le.transform(class_names))))

feature_names = list(X.columns)

# Save per-feature median values now (used later to auto-fill any
# input field the app's simplified form doesn't ask the user about)
feature_defaults = X.median(numeric_only=True).reindex(feature_names).fillna(0)

# ---------------------------------------------------------------------
# 3. Train / test split (stratified so class balance is preserved)
# ---------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------------------------
# 4. Scale features
# ---------------------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------------------------------------------------------------
# 5. Train several models and compare them (don't just train one!)
# ---------------------------------------------------------------------
models = {
    "Logistic Regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(
        n_estimators=300, class_weight="balanced", random_state=42
    ),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
}

try:
    from xgboost import XGBClassifier
    models["XGBoost"] = XGBClassifier(
        n_estimators=300, eval_metric="mlogloss", random_state=42
    )
except ImportError:
    print("\n(xgboost not installed — skipping it. `pip install xgboost` to include it.)")

results = {}
print("\n" + "=" * 60)
print("TRAINING AND COMPARING MODELS")
print("=" * 60)

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    preds = model.predict(X_test_scaled)
    f1 = f1_score(y_test, preds, average="macro")
    results[name] = (model, f1, preds)
    print(f"\n--- {name} (macro F1 = {f1:.3f}) ---")
    print(classification_report(y_test, preds, target_names=class_names))

# ---------------------------------------------------------------------
# 6. Pick the best model (by macro F1 across all 3 classes)
# ---------------------------------------------------------------------
best_name = max(results, key=lambda k: results[k][1])
best_model, best_f1, best_preds = results[best_name]

print("\n" + "=" * 60)
print(f"BEST MODEL: {best_name}  (macro F1 = {best_f1:.3f})")
print("=" * 60)
print("Confusion matrix (rows = actual, cols = predicted):")
print(class_names)
print(confusion_matrix(y_test, best_preds))

# ---------------------------------------------------------------------
# 7. Feature importance — this powers the "why" explanation in the app
# ---------------------------------------------------------------------
if hasattr(best_model, "feature_importances_"):
    importances = best_model.feature_importances_
elif hasattr(best_model, "coef_"):
    importances = np.abs(best_model.coef_).mean(axis=0)
else:
    importances = np.zeros(len(feature_names))

importance_df = pd.DataFrame(
    {"feature": feature_names, "importance": importances}
).sort_values("importance", ascending=False).reset_index(drop=True)

print("\nTop 10 most important features:")
print(importance_df.head(10).to_string(index=False))

# ---------------------------------------------------------------------
# 8. Save EVERYTHING the app needs into ONE file
# ---------------------------------------------------------------------
bundle = {
    "model": best_model,
    "model_name": best_name,
    "scaler": scaler,
    "label_encoder": le,
    "class_names": class_names,
    "feature_names": feature_names,
    "feature_defaults": feature_defaults,
    "feature_importance": importance_df,
    "test_f1_macro": best_f1,
}
joblib.dump(bundle, "dropout_model_bundle.pkl")

print("\n" + "=" * 60)
print("DONE. Saved -> dropout_model_bundle.pkl")
print("Download this file and place it next to app.py.")
print("=" * 60)
