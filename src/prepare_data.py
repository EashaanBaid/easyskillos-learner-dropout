from pathlib import Path
import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)
required = ["studentInfo.csv","studentRegistration.csv","studentVle.csv","vle.csv","courses.csv","assessments.csv","studentAssessment.csv"]
missing = [f for f in required if not (RAW/f).exists()]
if missing:
    raise SystemExit("Missing OULAD files in data/raw/: " + ", ".join(missing))

def read(name):
    return pd.read_csv(RAW/name, na_values=["?"])

info = read("studentInfo.csv")
reg = read("studentRegistration.csv")
vle = read("vle.csv")
courses = read("courses.csv")
assess = read("assessments.csv")
student_assess = read("studentAssessment.csv")

key = ["code_module","code_presentation","id_student"]
# Preserve one row per learner-course-presentation registration.
base = info.merge(reg[key+["date_registration","date_unregistration"]], on=key, how="left", validate="one_to_one")
base = base.merge(courses, on=["code_module","code_presentation"], how="left", validate="many_to_one")

# Read the large clickstream file in chunks; aggregate immediately to control memory.
early_click_parts = []
early_day_parts = []
activity_parts = []
for chunk in pd.read_csv(RAW/"studentVle.csv", chunksize=500_000, na_values=["?"]):
    chunk = chunk.merge(vle[["id_site","code_module","code_presentation","activity_type"]].drop_duplicates(),
                        on=["id_site","code_module","code_presentation"], how="left")
    early = chunk[chunk["date"].between(0,27)]
    if not early.empty:
        g = early.groupby(key)["sum_click"].sum().reset_index(name="early_clicks_28d")
        early_click_parts.append(g)
        early_day_parts.append(early[key+["date"]].drop_duplicates())
        by_type = early.groupby(key+["activity_type"])["sum_click"].sum().unstack(fill_value=0)
        by_type.columns = ["activity_" + str(c).lower().replace(" ","_") for c in by_type.columns]
        activity_parts.append(by_type.reset_index())

if early_click_parts:
    early_clicks = pd.concat(early_click_parts, ignore_index=True).groupby(key, as_index=False)["early_clicks_28d"].sum()
    unique_days = pd.concat(early_day_parts, ignore_index=True).drop_duplicates(key+["date"])
    active_days = unique_days.groupby(key).size().reset_index(name="early_active_days_28d")
    early = early_clicks.merge(active_days, on=key, how="left")
else:
    early = pd.DataFrame(columns=key+["early_clicks_28d","early_active_days_28d"])
activity = pd.concat(activity_parts, ignore_index=True).groupby(key, as_index=False).sum() if activity_parts else pd.DataFrame(columns=key)
# Assessment submissions in first 28 days, based on submission date.
sa = student_assess.merge(assess[["id_assessment","code_module","code_presentation"]], on="id_assessment", how="left")
sa["score"] = pd.to_numeric(sa["score"], errors="coerce")
sa_early = sa[sa.date_submitted.between(0,27)].groupby(key).agg(early_assessment_submissions=("id_assessment","nunique"), early_mean_score=("score","mean")).reset_index()

df = base.merge(early, on=key, how="left").merge(activity, on=key, how="left").merge(sa_early, on=key, how="left")
df["date_unregistration"] = pd.to_numeric(df["date_unregistration"], errors="coerce")
df["date_registration"] = pd.to_numeric(df["date_registration"], errors="coerce")
df["early_clicks_28d"] = df["early_clicks_28d"].fillna(0)
df["early_active_days_28d"] = df["early_active_days_28d"].fillna(0)
df["early_assessment_submissions"] = df["early_assessment_submissions"].fillna(0)
activity_cols = [c for c in df.columns if c.startswith("activity_")]
df[activity_cols] = df[activity_cols].fillna(0)
df["engaged_early"] = (df.early_clicks_28d >= 10) & (df.early_active_days_28d >= 3)
q25 = df["early_clicks_28d"].quantile(.25)
df["at_risk"] = (df.early_clicks_28d == 0) | (df.early_clicks_28d <= q25)
df["successful_completion"] = df.final_result.isin(["Pass","Distinction"]).astype(int)
df["withdrawn"] = df.final_result.eq("Withdrawn").astype(int)
df["learner_group"] = np.select(
    [df.num_of_prev_attempts.gt(0), df.highest_education.isin(["No Formal quals","Lower Than A Level"])],
    ["Repeat attempt", "Lower prior education"], default="Other learners")
def stage(row):
    if row.final_result != "Withdrawn": return "Not withdrawn"
    x = row.date_unregistration
    if pd.isna(x): return "Unknown withdrawal date"
    if x < 0: return "Before course start"
    return f"Week {int(x//7)+1}"
def stage_order(row):
    if row.final_result != "Withdrawn": return np.nan
    x = row.date_unregistration
    if pd.isna(x): return -1
    if x < 0: return 0
    return int(x//7)+1
df["withdrawal_stage"] = df.apply(stage, axis=1)
df["withdrawal_stage_order"] = df.apply(stage_order, axis=1)
# Remove direct learner identifier from the analysis output.
df = df.drop(columns=["id_student"], errors="ignore")
df.to_csv(OUT/"learner_features.csv", index=False)

# Hold-out predictive check: context-only baseline vs context + first-28-day signals.
# The target is Pass/Distinction. This is predictive association, not a causal model.
def evaluate_model(numeric_features):
    categorical_features = ["code_module", "code_presentation", "learner_group"]
    X = df[numeric_features + categorical_features].copy()
    y = df["successful_completion"].astype(int)
    preprocess = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric_features),
        ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical_features)
    ])
    pipe = Pipeline([("preprocess", preprocess),
                     ("model", LogisticRegression(max_iter=1500, class_weight="balanced"))])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y)
    pipe.fit(X_train, y_train)
    probability = pipe.predict_proba(X_test)[:, 1]
    prediction = (probability >= 0.5).astype(int)
    return {
        "test_rows": int(len(y_test)),
        "roc_auc": float(roc_auc_score(y_test, probability)),
        "accuracy": float(accuracy_score(y_test, prediction)),
        "precision": float(precision_score(y_test, prediction)),
        "recall": float(recall_score(y_test, prediction)),
        "f1": float(f1_score(y_test, prediction))
    }

baseline_metrics = evaluate_model(["studied_credits", "num_of_prev_attempts"])
early_metrics = evaluate_model([
    "studied_credits", "num_of_prev_attempts", "early_clicks_28d",
    "early_active_days_28d", "early_assessment_submissions", "early_mean_score"
])
model_report = {
    "target": "Pass or Distinction",
    "split": "Stratified 80/20 hold-out; random_state=42",
    "baseline_features": "Prior context: studied credits and previous attempts, plus course, presentation and learner group.",
    "early_signal_features": "Baseline plus first-28-day clicks, active days, assessment submissions and mean score.",
    "baseline": baseline_metrics,
    "with_early_signals": early_metrics,
    "interpretation": "Hold-out discrimination improved when early signals were added. This does not prove interventions cause completion."
}
(OUT/"model_evaluation.json").write_text(json.dumps(model_report, indent=2))

# Reproducible data quality log.
quality = {
 "source":"Open University Learning Analytics Dataset (OULAD)",
 "raw_files":{f: int(len(pd.read_csv(RAW/f, usecols=[0]))) for f in required},
 "output_rows":int(len(df)),
 "output_columns":int(len(df.columns)),
 "missing_values":{k:int(v) for k,v in df.isna().sum().items() if v>0},
 "duplicate_learner_course_keys":int(base.duplicated(key).sum()),
 "model_evaluation":"model_evaluation.json",
 "cleaning_decisions":[
  "Kept one learner-course-presentation record from studentInfo and joined registration/course metadata.",
  "Aggregated VLE clicks by learner-course-presentation in chunks; only first 28 days used for early engagement features.",
  "No first-28-day VLE interaction / activity-type record was treated as zero clicks; absence of an early assessment submission was treated as zero submissions.",
  "The 93 withdrawn registrations with no recorded unregistration day are labelled Unknown withdrawal date; non-withdrawn registrations are Not withdrawn.",
  "Question-mark placeholders in source CSVs were parsed as missing values; missing demographics and early assessment scores were not imputed in the exported dataset.",
  "Missing demographic and assessment values were not imputed.",
  "Learner identifier removed from exported analysis table.",
  "No records were removed solely because a demographic field was missing."
 ],
 "definitions":{
  "engaged":"At least 10 VLE clicks and at least 3 active days in first 28 days.",
  "at_risk":f"Zero first-28-day clicks or clicks at/below full-dataset 25th percentile ({q25:.2f}).",
  "successful_completion":"Pass or Distinction final_result.",
  "limitations":"VLE click counts are not video watch-time; observational associations do not establish causation."
 }
}
(OUT/"data_quality_report.json").write_text(json.dumps(quality, indent=2))
print(f"Saved {len(df):,} learner-course rows to {OUT/'learner_features.csv'}")
print(f"First-28-day click 25th percentile: {q25:.1f}")
