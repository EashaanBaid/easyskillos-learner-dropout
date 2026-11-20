# Data dictionary

| Field | Meaning |
|---|---|
| `code_module` | Course/module code |
| `code_presentation` | Course presentation / term |
| `final_result` | Final outcome: Pass, Distinction, Fail or Withdrawn |
| `date_registration` | Days relative to course start when learner registered |
| `date_unregistration` | Days relative to course start when learner unregistered; blank for non-withdrawn or unrecorded |
| `early_clicks_28d` | Total VLE clicks during days 0–27 |
| `early_active_days_28d` | Distinct days with at least one VLE interaction during days 0–27 |
| `activity_*` | Click totals for the relevant VLE activity type during days 0–27 |
| `early_assessment_submissions` | Distinct assessments submitted during days 0–27 |
| `early_mean_score` | Mean score for early submitted assessments; missing if no score is recorded |
| `engaged_early` | True when clicks >=10 and active days >=3 in first 28 days |
| `at_risk` | True when first-28-day clicks are zero or <=31 (full dataset 25th percentile) |
| `successful_completion` | 1 for Pass/Distinction, otherwise 0 |
| `withdrawn` | 1 for Withdrawn, otherwise 0 |
| `learner_group` | Derived descriptive group based on prior attempts and education |
| `withdrawal_stage` | Administrative withdrawal timing grouped into course weeks |
| `withdrawal_stage_order` | Numeric order for sorting withdrawal stage chart |

Direct learner identifier `id_student` is excluded from the processed output.
