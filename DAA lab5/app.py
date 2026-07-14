"""
app.py
======
STEP 2 — RUN THIS ONLY AFTER train_model.py HAS PRODUCED
dropout_model_bundle.pkl AND IT IS SITTING IN THE SAME FOLDER AS THIS FILE.

This single file is both the "frontend" (the form the user sees) and the
"backend" (the code that loads the model and runs the prediction) — that's
normal for a Streamlit app and is plenty for a college project.

Run locally to test:
    pip install -r requirements.txt
    streamlit run app.py

Deploy for free:
    Push this folder (app.py, requirements.txt, dropout_model_bundle.pkl)
    to a GitHub repo, then go to https://share.streamlit.io and point it
    at the repo. You'll get a public URL in a couple of minutes.
"""

import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Student Dropout Risk Predictor", page_icon="🎓", layout="centered")

# ---------------------------------------------------------------------
# Load the trained model bundle
# ---------------------------------------------------------------------
@st.cache_resource
def load_bundle():
    return joblib.load("dropout_model_bundle.pkl")

try:
    bundle = load_bundle()
except FileNotFoundError:
    st.error(
        "dropout_model_bundle.pkl not found. Run train_model.py first, then "
        "place the generated file in this same folder."
    )
    st.stop()

model = bundle["model"]
scaler = bundle["scaler"]
label_encoder = bundle["label_encoder"]
class_names = bundle["class_names"]
feature_names = bundle["feature_names"]
feature_defaults = bundle["feature_defaults"]
importance_df = bundle["feature_importance"]
model_name = bundle["model_name"]


def find_col(*keywords):
    """Find the real column name in the dataset that contains any of the
    given keywords (case-insensitive). Returns None if nothing matches."""
    for col in feature_names:
        low = col.lower()
        if any(k.lower() in low for k in keywords):
            return col
    return None


# ---------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------
st.title("🎓 Student Dropout Risk Predictor")
st.caption(f"Model in use: **{model_name}** (trained on the UCI Student Dropout dataset)")
st.write("Fill in the student's details below to estimate dropout risk.")

with st.form("student_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age at enrollment", 16, 70, 19)
        gender = st.selectbox("Gender", ["Male", "Female"])
        attendance = st.selectbox("Attendance", ["Daytime", "Evening"])
        scholarship = st.selectbox("Scholarship holder?", ["No", "Yes"])
        tuition_paid = st.selectbox("Tuition fees up to date?", ["Yes", "No"])
        debtor = st.selectbox("Debtor?", ["No", "Yes"])
        displaced = st.selectbox("Displaced student?", ["No", "Yes"])

    with col2:
        admission_grade = st.slider("Admission grade (0-200)", 0, 200, 130)
        prev_grade = st.slider("Previous qualification grade (0-200)", 0, 200, 130)
        units_enrolled_1 = st.slider("Curricular units enrolled — Sem 1", 0, 26, 6)
        units_approved_1 = st.slider("Curricular units approved — Sem 1", 0, 26, 5)
        grade_sem1 = st.slider("Average grade — Sem 1 (0-20)", 0.0, 20.0, 12.0)
        units_enrolled_2 = st.slider("Curricular units enrolled — Sem 2", 0, 26, 6)
        units_approved_2 = st.slider("Curricular units approved — Sem 2", 0, 26, 5)
        grade_sem2 = st.slider("Average grade — Sem 2 (0-20)", 0.0, 20.0, 12.0)

    submitted = st.form_submit_button("Predict Dropout Risk")

if submitted:
    # Start from the dataset's median values for every feature ...
    row = feature_defaults.copy()

    # ... then overwrite the ones the user actually filled in.
    # find_col() locates the real column name robustly (handles minor
    # spelling/apostrophe differences in the source dataset).
    def set_if_found(*keywords, value=None):
        col = find_col(*keywords)
        if col is not None:
            row[col] = value

    set_if_found("age at enrollment", value=age)
    set_if_found("gender", value=1 if gender == "Male" else 0)
    set_if_found("daytime/evening", value=1 if attendance == "Daytime" else 0)
    set_if_found("scholarship holder", value=1 if scholarship == "Yes" else 0)
    set_if_found("tuition fees", value=1 if tuition_paid == "Yes" else 0)
    set_if_found("debtor", value=1 if debtor == "Yes" else 0)
    set_if_found("displaced", value=1 if displaced == "Yes" else 0)
    set_if_found("admission grade", value=admission_grade)
    set_if_found("previous qualification (grade)", value=prev_grade)

    for col in feature_names:
        low = col.lower()
        if "1st sem" in low and "enrolled" in low:
            row[col] = units_enrolled_1
        elif "1st sem" in low and "approved" in low:
            row[col] = units_approved_1
        elif "1st sem" in low and "(grade)" in low:
            row[col] = grade_sem1
        elif "2nd sem" in low and "enrolled" in low:
            row[col] = units_enrolled_2
        elif "2nd sem" in low and "approved" in low:
            row[col] = units_approved_2
        elif "2nd sem" in low and "(grade)" in low:
            row[col] = grade_sem2

    # Build the final feature vector in the exact training column order
    X_input = pd.DataFrame([row], columns=feature_names)
    X_scaled = scaler.transform(X_input)

    pred_idx = model.predict(X_scaled)[0]
    pred_label = label_encoder.inverse_transform([pred_idx])[0]
    proba = model.predict_proba(X_scaled)[0]

    st.divider()
    st.subheader("Result")

    if pred_label.lower() == "dropout":
        st.error(f"⚠️ Predicted outcome: **{pred_label}** — this student is flagged as high risk.")
    elif pred_label.lower() == "enrolled":
        st.warning(f"🟡 Predicted outcome: **{pred_label}** — still in progress, monitor closely.")
    else:
        st.success(f"✅ Predicted outcome: **{pred_label}**")

    proba_df = pd.DataFrame({"Outcome": class_names, "Probability": proba}).set_index("Outcome")
    st.bar_chart(proba_df)

    st.subheader("What drives this model's predictions")
    st.caption("Top features the model relies on most, across all students (not specific to this one input).")
    top_features = importance_df.head(8).set_index("feature")
    st.bar_chart(top_features)

st.divider()
st.caption(
    "Dataset: Realinho et al. (2021), Predict Students' Dropout and Academic Success, "
    "UCI Machine Learning Repository, doi.org/10.24432/C5MC89."
)
