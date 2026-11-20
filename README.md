# Where Do Learners Drop Off? — EasySkillOS Project 01

**Learning Analytics · Moderate level · Open University Learning Analytics Dataset (OULAD)**

A reproducible analytics project that cleans anonymised learner records, measures first-28-day engagement, evaluates early signals of successful completion, and presents an interactive Streamlit dashboard with an action memo.

## Verified dataset findings
- 32,593 learner-course-presentation registrations.
- Final outcomes: 12,361 Pass, 3,024 Distinction, 7,052 Fail, 10,156 Withdrawn.
- Successful completion (Pass/Distinction): 47.2%.
- Withdrawn: 31.2%.
- 2,676 recorded withdrawals occurred before course start; among post-start withdrawals with a recorded date, Week 2 is the most common stage (1,068).
- Early engagement is associated with 57.5% successful completion vs 13.8% among learners not meeting the engagement definition.
- Hold-out ROC-AUC improved from 0.649 (prior-context baseline) to 0.822 after adding first-28-day activity and assessment signals. This is predictive association, not causation.

## Project structure
```text
.
├── app.py
├── requirements.txt
├── README.md
├── CLEANING_LOG.md
├── DATA_DICTIONARY.md
├── ANALYSIS_SUMMARY.md
├── RECOMMENDATIONS.md
├── WALKTHROUGH_SCRIPT.md
├── src/
│   └── prepare_data.py
└── data/
    ├── raw/                  # Original OULAD CSVs; not bundled (large)
    └── processed/
        ├── learner_features.csv
        ├── data_quality_report.json
        └── model_evaluation.json
```

## Run the dashboard immediately
The ZIP includes the prepared, anonymised learner-level feature table, so you can launch the dashboard without reprocessing the 454 MB clickstream file.

### Mac Apple Silicon setup
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL printed by Streamlit (normally `http://localhost:8501`).

## Reproduce the cleaning and feature engineering
1. Download the OULAD archive from the [UCI dataset page](https://archive.ics.uci.edu/dataset/349/open+university+learning+analytics+dataset).
2. Extract the seven CSVs into `data/raw/`: `studentInfo.csv`, `studentRegistration.csv`, `studentVle.csv`, `vle.csv`, `courses.csv`, `assessments.csv`, and `studentAssessment.csv`.
3. Run:
```bash
python src/prepare_data.py
```
The script reads the large `studentVle.csv` in chunks and regenerates the processed CSV and JSON reports.

## Dashboard contents (8 charts)
1. Final learner outcomes.
2. Withdrawal timing.
3. Early at-risk rate by learner group.
4. Successful completion by learner group.
5. First-28-day clicks by final outcome.
6. Early activity/completion association matrix.
7. Average first-28-day clicks by VLE activity type.
8. Completion by early use of forum, quiz, generic URL and course-content categories.

Filters: course/presentation, term, and learner group. Includes a data quality tab, definitions, model validation and an illustrative what-if control.

## Definitions
- **Engaged:** at least 10 VLE clicks and at least 3 distinct active days during days 0–27.
- **At risk:** zero first-28-day clicks or clicks at/below the full-dataset 25th percentile (31 clicks).
- **Successful completion:** final result is Pass or Distinction.
- **Learner group:** Repeat attempt takes priority; otherwise Lower prior education means No Formal quals or Lower Than A Level; all others are Other learners.

## Important limitations
- OULAD records VLE clicks, not reliable video watch-time. Generic URL clicks cannot be assumed to be video views.
- It does not provide a reliable first-module completion flag. The what-if slider is therefore an early-engagement proxy, not the exact requested module-completion scenario.
- Activity and completion are observational. Correlation and model performance do not prove an activity or intervention causes completion.
- 93 withdrawn records have no recorded unregistration day; these remain labelled Unknown withdrawal date.
- The prepared table excludes the direct learner identifier. The original source archive is not included in this project ZIP because its clickstream file is large.

## Deployment
Push this folder to a GitHub repository. In Streamlit Community Cloud, choose **Create app**, select the repository and branch, set the main file to `app.py`, then deploy. The processed CSV is included, so the app can start without the raw source archive. A live URL requires the user's GitHub and Streamlit accounts and a deployment action.

## Citation
Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). Open University Learning Analytics Dataset (OULAD). *Scientific Data*, 4, 170171. https://doi.org/10.1038/sdata.2017.171
