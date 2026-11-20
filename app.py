
from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Learner Retention | EasySkillOS",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
:root {
    --ink:#172033;
    --muted:#64748b;
    --line:#e5eaf2;
    --blue:#2563eb;
    --teal:#0f766e;
}

.block-container {
    max-width:1480px;
    padding-top:1.2rem;
    padding-bottom:3rem;
}

[data-testid="stAppViewContainer"] {
    background:#f6f8fc;
}

/* Transparent Streamlit header */
[data-testid="stHeader"] {
    background:transparent !important;
    box-shadow:none !important;
}

/* Hide only Deploy */
[data-testid="stAppDeployButton"] {
    display:none !important;
}

/* Keep toolbar and sidebar reopen controls visible */
[data-testid="stToolbar"] {
    visibility:visible !important;
    opacity:1 !important;
}

[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    pointer-events:auto !important;
}

[data-testid="stDecoration"] {
    display:none !important;
}

[data-testid="stSidebar"] {
    background:#ffffff;
    border-right:1px solid #e5eaf2;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color:#526079;
}

[data-testid="stMetric"] {
    background:#fff;
    border:1px solid #e5eaf2;
    border-radius:16px;
    padding:17px 18px;
    box-shadow:0 4px 16px rgba(20,36,70,.045);
}

[data-testid="stMetricLabel"] {
    color:#64748b;
    font-size:.82rem;
    font-weight:650;
}

[data-testid="stMetricValue"] {
    color:#172033;
    font-weight:750;
    letter-spacing:-.035em;
}

[data-testid="stMetricDelta"] {
    font-size:.78rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap:8px;
    border-bottom:1px solid #e5eaf2;
}

.stTabs [data-baseweb="tab"] {
    background:#fff;
    border:1px solid #e5eaf2;
    border-radius:10px 10px 0 0;
    padding:10px 16px;
    color:#526079;
}

.stTabs [aria-selected="true"] {
    color:#1d4ed8!important;
    border-bottom:2px solid #2563eb!important;
}

[data-testid="stPlotlyChart"] {
    background:#fff;
    border:1px solid #e8edf5;
    border-radius:16px;
    padding:8px 8px 2px;
    box-shadow:0 4px 16px rgba(20,36,70,.035);
}

[data-testid="stDataFrame"] {
    border:1px solid #e5eaf2;
    border-radius:12px;
    overflow:hidden;
}

div[data-testid="stAlert"] {
    border-radius:12px;
}

.hero {
    background:linear-gradient(
        115deg,#102a56 0%,#1d4ed8 58%,#0f766e 100%
    );
    padding:28px 30px;
    border-radius:20px;
    color:white;
    margin:0 0 18px 0;
    box-shadow:0 12px 28px rgba(29,78,216,.16);
}

.hero-kicker {
    font-size:.72rem;
    text-transform:uppercase;
    letter-spacing:.14em;
    font-weight:750;
    opacity:.78;
    margin-bottom:8px;
}

.hero h1 {
    font-size:2rem;
    line-height:1.15;
    margin:0 0 8px 0;
    color:#fff;
    font-weight:800;
    letter-spacing:-.04em;
}

.hero p {
    font-size:.94rem;
    margin:0;
    color:rgba(255,255,255,.86);
}

.section-note {
    color:#64748b;
    font-size:.84rem;
    margin-top:-8px;
    margin-bottom:12px;
}

.sidebar-note {
    background:#f1f5f9;
    border:1px solid #e2e8f0;
    border-radius:12px;
    padding:12px;
    color:#475569;
    font-size:.8rem;
    line-height:1.5;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    border-radius:10px;
    border-color:#d8e1ee;
    background:#fbfdff;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] label {
    font-size:.86rem;
    font-weight:650;
    color:#34445e;
}

[data-testid="stSidebar"] h2 {
    font-size:1.25rem;
    font-weight:750;
    color:#172033;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap:.75rem;
}

div[data-testid="stDownloadButton"] button {
    border-radius:10px;
}

@media (max-width:800px) {
    .hero {padding:22px;}
    .hero h1 {font-size:1.55rem;}
    .block-container {
        padding-left:1rem;
        padding-right:1rem;
    }
}
</style>

<div class="hero">
  <div class="hero-kicker">
    EasySkillOS · Learning analytics · Project 01
  </div>
  <h1>Where do learners drop off?</h1>
  <p>
    Understand retention, spot early risk signals, and focus learner
    support where it can make a difference.
  </p>
</div>
""", unsafe_allow_html=True)


# LOAD DATA
DATA = Path("data/processed/learner_features.csv")
MODEL_FILE = Path("data/processed/model_evaluation.json")
QUALITY_FILE = Path("data/processed/data_quality_report.json")

if not DATA.exists():
    st.warning(
        "Processed data not found. Place the seven OULAD CSV files "
        "in data/raw/ and run the preparation script."
    )
    st.code(
        "python src/prepare_data.py\n"
        "python -m streamlit run app.py"
    )
    st.markdown(
        "[Download OULAD from UCI]"
        "(https://archive.ics.uci.edu/dataset/349/open+university+"
        "learning+analytics+dataset)"
    )
    st.stop()

df = pd.read_csv(DATA)

model_report = (
    json.loads(MODEL_FILE.read_text())
    if MODEL_FILE.exists() else {}
)

quality = (
    json.loads(QUALITY_FILE.read_text())
    if QUALITY_FILE.exists() else {}
)

df["course_term"] = (
    df["code_module"].astype(str)
    + " · "
    + df["code_presentation"].astype(str)
)


# SIDEBAR FILTERS
with st.sidebar:
    st.header("Dashboard filters")

    course_options = ["All courses"] + sorted(
        df["course_term"].dropna().astype(str).unique().tolist()
    )

    term_options = ["All terms"] + sorted(
        df["code_presentation"].dropna().astype(str).unique().tolist()
    )

    group_options = ["All learner groups"] + sorted(
        df["learner_group"].dropna().astype(str).unique().tolist()
    )

    selected_course = st.selectbox(
        "Course / presentation", course_options
    )

    selected_term = st.selectbox(
        "Term", term_options
    )

    selected_group = st.selectbox(
        "Learner group", group_options
    )

    st.divider()

    st.markdown("""
    <div class='sidebar-note'>
      <b>At-risk rule</b><br>
      Fixed against the full dataset: zero clicks or ≤31 clicks
      in the first 28 days. Filters change the view, not the threshold.
    </div>
    """, unsafe_allow_html=True)


# APPLY FILTERS
filter_mask = pd.Series(True, index=df.index)

if selected_course != "All courses":
    filter_mask &= df["course_term"].astype(str).eq(selected_course)

if selected_term != "All terms":
    filter_mask &= df["code_presentation"].astype(str).eq(selected_term)

if selected_group != "All learner groups":
    filter_mask &= df["learner_group"].astype(str).eq(selected_group)

d = df.loc[filter_mask].copy()

if d.empty:
    st.info("No learners match these filters.")
    st.stop()


# KPI METRICS
n = len(d)
success = d["successful_completion"].mean() * 100
withdrawal = d["withdrawn"].mean() * 100
risk = d["at_risk"].mean() * 100

k1, k2, k3, k4 = st.columns(4)

k1.metric("Learner registrations", f"{n:,}")
k2.metric("Pass / distinction", f"{success:.1f}%")
k3.metric("Withdrawn", f"{withdrawal:.1f}%")
k4.metric("Early at-risk", f"{risk:.1f}%")

st.caption(
    "Successful completion = Pass or Distinction. Fail and Withdrawn "
    "are not counted as successful completion. All headline metrics "
    "respond to the filters in the sidebar."
)

overview, engagement, checks_tab = st.tabs([
    "Retention overview",
    "Early engagement & activities",
    "Data quality & definitions"
])


# TAB 1: RETENTION OVERVIEW
with overview:

    st.subheader("Retention and withdrawal")

    st.markdown(
        "<div class='section-note'>Start with the final outcome mix, "
        "then compare when withdrawals happen and which learner groups "
        "may need earlier support.</div>",
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    outcome = (
        d["final_result"]
        .value_counts()
        .rename_axis("Outcome")
        .reset_index(name="Learners")
    )

    
    fig_outcome = px.bar(
        outcome,
        x="Outcome",
        y="Learners",
        text="Learners",
        title="1 · Final learner outcomes",
        template="plotly_white",
        color="Outcome",
        color_discrete_map={
            "Pass": "#2563eb",
            "Withdrawn": "#0f766e",
            "Fail": "#f59e0b",
            "Distinction": "#94a3b8"
        },
        category_orders={
            "Outcome": ["Pass", "Withdrawn", "Fail", "Distinction"]
        }
    )

    fig_outcome.update_layout(
        showlegend=True,
        height=420,
        margin=dict(l=20, r=20, t=105, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.12,
            xanchor="center",
            x=0.5,
            title_text=""
        ),
        font=dict(size=12),
        title=dict(font=dict(size=16)),
        xaxis_title="Outcome",
        yaxis_title="Learners"
    )

    fig_outcome.update_traces(
        texttemplate="%{y:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    left.plotly_chart(
        fig_outcome,
        width="stretch",
        config={"displayModeBar": False}
    )


    left.caption(
        f"Takeaway: {int(d['withdrawn'].sum()):,} of {n:,} "
        f"filtered registrations ({withdrawal:.1f}%) ended as Withdrawn."
    )

    # WITHDRAWAL TIMING
    # Missing dates are excluded from this chart, not deleted from data.

    withdrawn_records = d[d["withdrawn"] == 1].copy()

    missing_withdrawal_dates = int(
        withdrawn_records["date_unregistration"].isna().sum()
    )

    withdrawal_timing = withdrawn_records[
        withdrawn_records["date_unregistration"].notna()
        & withdrawn_records["withdrawal_stage"].notna()
        & (
            withdrawn_records["withdrawal_stage"]
            != "Unknown withdrawal date"
        )
    ].copy()

    w = (
        withdrawal_timing
        .groupby(
            ["withdrawal_stage", "withdrawal_stage_order"],
            as_index=False
        )
        .size()
        .rename(columns={"size": "Learners"})
        .sort_values("withdrawal_stage_order")
    )

    if not w.empty:

        right.plotly_chart(
            px.bar(
                w,
                x="withdrawal_stage",
                y="Learners",
                text_auto=True,
                title="2 · When did learners withdraw?",
                template="plotly_white",
                color_discrete_sequence=["#0f766e"]
            ),
            width="stretch"
        )

        peak = w.loc[w["Learners"].idxmax()]

        right.caption(
            f"Takeaway: the largest recorded withdrawal stage is "
            f"{peak['withdrawal_stage']} "
            f"({int(peak['Learners']):,} learners). "
            f"{missing_withdrawal_dates:,} withdrawn records with "
            "missing dates are excluded from this chart."
        )

    else:
        right.info(
            "No withdrawals with recorded dates match these filters."
        )

    st.subheader("Which learner groups need more support?")

    g = (
        d.groupby("learner_group", as_index=False)
        .agg(
            at_risk_rate=("at_risk", "mean"),
            completion_rate=("successful_completion", "mean"),
            registrations=("final_result", "size")
        )
    )

    g["At-risk rate (%)"] = g["at_risk_rate"] * 100
    g["Successful completion (%)"] = g["completion_rate"] * 100

    left, right = st.columns(2)

    left.plotly_chart(
        px.bar(
            g,
            x="learner_group",
            y="At-risk rate (%)",
            text_auto=".1f",
            title="3 · Early at-risk rate by learner group",
            template="plotly_white",
            color_discrete_sequence=["#f59e0b"]
        ),
        width="stretch"
    )

    if not g.empty:
        highest = g.sort_values(
            "At-risk rate (%)", ascending=False
        ).iloc[0]

        left.caption(
            f"Takeaway: {highest['learner_group']} has the highest "
            f"early at-risk rate "
            f"({highest['At-risk rate (%)']:.1f}%)."
        )

    right.plotly_chart(
        px.bar(
            g,
            x="learner_group",
            y="Successful completion (%)",
            text_auto=".1f",
            title="4 · Successful completion by learner group",
            template="plotly_white",
            color_discrete_sequence=["#2563eb"]
        ),
        width="stretch"
    )

    if not g.empty:
        lowest = g.sort_values(
            "Successful completion (%)"
        ).iloc[0]

        right.caption(
            f"Takeaway: {lowest['learner_group']} has the lowest "
            f"successful completion rate "
            f"({lowest['Successful completion (%)']:.1f}%)."
        )


# TAB 2: EARLY ENGAGEMENT
with engagement:

    st.subheader("Do early behaviours signal completion?")

    st.markdown(
        "<div class='section-note'>Explore first-28-day learning "
        "activity and its relationship with later outcomes. These are "
        "descriptive signals, not causal effects.</div>",
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    box = d.copy()

    box["Outcome"] = box["successful_completion"].map({
        0: "Not completed",
        1: "Pass / distinction"
    })

    left.plotly_chart(
        px.box(
            box,
            x="Outcome",
            y="early_clicks_28d",
            points=False,
            title="5 · First-28-day clicks by final outcome",
            labels={
                "early_clicks_28d":
                "VLE clicks in first 28 days"
            },
            template="plotly_white",
            color_discrete_sequence=["#2563eb", "#0f766e"]
        ),
        width="stretch"
    )

    med = box.groupby("Outcome")["early_clicks_28d"].median()

    if len(med) == 2:
        left.caption(
            f"Takeaway: median early clicks are "
            f"{med.get('Pass / distinction', 0):.0f} for completers "
            f"vs {med.get('Not completed', 0):.0f} for others."
        )

    cols = [
        "early_clicks_28d",
        "early_active_days_28d",
        "early_assessment_submissions",
        "successful_completion"
    ]

    right.plotly_chart(
        px.imshow(
            d[cols].corr(numeric_only=True),
            text_auto=".2f",
            aspect="auto",
            title="6 · Early activity and completion associations",
            color_continuous_scale="Blues"
        ),
        width="stretch"
    )

    right.caption(
        "Takeaway: positive correlations show association, "
        "not proof that activity causes completion."
    )

    engaged_rates = d.groupby("engaged_early").agg(
        learners=("successful_completion", "size"),
        completion=("successful_completion", "mean")
    )

    if {True, False}.issubset(set(engaged_rates.index)):
        rate_eng = engaged_rates.loc[True, "completion"] * 100
        rate_not = engaged_rates.loc[False, "completion"] * 100

        st.markdown(
            f"**Engaged early:** {rate_eng:.1f}% successful completion "
            f"· **Not engaged early:** {rate_not:.1f}%"
        )

    if model_report:
        b_auc = model_report["baseline"]["roc_auc"]
        e_auc = model_report["with_early_signals"]["roc_auc"]

        st.info(
            f"Hold-out prediction check (20% test set, "
            f"{model_report['with_early_signals']['test_rows']:,} "
            f"learners): ROC-AUC improved from **{b_auc:.3f}** "
            f"for prior-context features to **{e_auc:.3f}** after "
            "adding first-28-day activity and assessment signals. "
            "Predictive association is not causation."
        )

    st.subheader("Which activities are associated with completion?")

    act_cols = [
        c for c in d.columns if c.startswith("activity_")
    ]

    if act_cols:

        activity = pd.DataFrame({
            "Activity": [
                c.replace("activity_", "") for c in act_cols
            ],
            "Mean clicks per learner": [
                d[c].mean() for c in act_cols
            ],
            "Learners using activity": [
                int((d[c] > 0).sum()) for c in act_cols
            ],
            "Completion among users (%)": [
                d.loc[d[c] > 0, "successful_completion"].mean() * 100
                if (d[c] > 0).any() else 0
                for c in act_cols
            ]
        }).sort_values(
            "Mean clicks per learner", ascending=False
        ).head(12)

        st.plotly_chart(
            px.bar(
                activity,
                x="Activity",
                y="Mean clicks per learner",
                title="7 · Average first-28-day clicks by activity type",
                template="plotly_white",
                color_discrete_sequence=["#2563eb"]
            ),
            width="stretch"
        )

        most_used = ", ".join(
            activity.head(3)["Activity"].tolist()
        )

        st.caption(
            "Takeaway: the three highest average-click activity "
            f"types in this filtered view are {most_used}."
        )

        selected_types = [
            c for c in ["forumng", "quiz", "url", "oucontent"]
            if "activity_" + c in d.columns
        ]

        compare_rows = []

        for typ in selected_types:
            c = "activity_" + typ

            for flag, label in [
                (True, "Used"),
                (False, "No recorded use")
            ]:
                subset = d[(d[c] > 0) == flag]

                if len(subset):
                    compare_rows.append({
                        "Activity": typ,
                        "Group": label,
                        "Completion rate (%)":
                            subset["successful_completion"].mean() * 100,
                        "Learners": len(subset)
                    })

        compare = pd.DataFrame(compare_rows)

        if not compare.empty:
            
            fig_compare = px.bar(
                compare,
                x="Activity",
                y="Completion rate (%)",
                color="Group",
                barmode="group",
                hover_data=["Learners"],
                title="8 · Completion by early use of activities",
                template="plotly_white",
                color_discrete_map={
                    "Used": "#2563eb",
                    "No recorded use": "#94a3b8"
                }
            )

            fig_compare.update_layout(
                height=430,
                margin=dict(l=20, r=20, t=105, b=50),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.12,
                    xanchor="center",
                    x=0.5,
                    title_text="Activity usage"
                )
            )

            st.plotly_chart(
                fig_compare,
                width="stretch",
                config={"displayModeBar": False}
            )


        st.caption(
            "Takeaway: forum and quiz users have higher observed "
            "completion than non-users, but this may reflect "
            "pre-existing engagement. URL is a generic link category, "
            "not a verified video measure."
        )

    st.warning(
        "Video watch-time is not available as a distinct OULAD measure. "
        "Do not interpret URL clicks or course-content clicks as video viewing."
    )

    st.subheader("What-if: improve early engagement")

    pct = st.slider(
        "Share of currently non-engaged learners who hypothetically "
        "reach the early-engagement threshold",
        0, 10, 10, 1
    )

    if {True, False}.issubset(set(engaged_rates.index)):

        nonengaged_n = int(
            engaged_rates.loc[False, "learners"]
        )

        shifted = round(nonengaged_n * pct / 100)

        uplift = max(0, rate_eng - rate_not) / 100

        estimated_extra = round(shifted * uplift)

        projected = (
            int(d["successful_completion"].sum()) + estimated_extra
        ) / n * 100

        st.metric(
            "Illustrative projected completion",
            f"{projected:.1f}%",
            f"+{estimated_extra:,} estimated completions"
        )

        st.caption(
            f"Scenario: {shifted:,} currently non-engaged learners "
            "move into the engaged group; the observed completion-rate "
            "gap is applied as an illustrative uplift. This is not "
            "causal and does not measure first-module completion. "
            "OULAD does not include a reliable first-module completion field."
        )


# TAB 3: DATA QUALITY
with checks_tab:

    st.subheader("Data checks")

    st.markdown(
        "<div class='section-note'>Review missingness, data "
        "preparation choices, metric definitions, and limitations "
        "before drawing conclusions.</div>",
        unsafe_allow_html=True
    )

    missing_withdrawal = int(
        d.loc[
            d["withdrawn"] == 1,
            "date_unregistration"
        ].isna().sum()
    )

    checks = pd.DataFrame({
        "Check": [
            "Learner-course registrations in filtered view",
            "Missing final outcomes",
            "Missing early mean assessment score",
            "Withdrawn records with no unregistration day",
            "Duplicate learner-course keys in prepared dataset"
        ],
        "Value": [
            len(d),
            int(d["final_result"].isna().sum()),
            int(d["early_mean_score"].isna().sum()),
            missing_withdrawal,
            quality.get(
                "duplicate_learner_course_keys",
                "See quality report"
            )
        ]
    })

    st.dataframe(
        checks,
        width="stretch",
        hide_index=True
    )

    st.markdown(
        "**Missing-value treatment:** no activity record in the first "
        "28 days is treated as zero observed clicks; no assessment "
        "submission is zero submissions. Demographic values and missing "
        "assessment scores remain missing. Unregistration dates are "
        "structurally blank for learners who did not withdraw; "
        "93 withdrawn records have no recorded withdrawal day."
    )

    st.subheader("Definitions")

    st.markdown("""
    - **Engaged:** at least 10 VLE clicks and activity on at least 3 distinct days during days 0–27.
    - **At risk:** zero first-28-day clicks or clicks at/below the full-dataset 25th percentile (31 clicks). This is an operational flag, not a diagnosis.
    - **Successful completion:** final result is Pass or Distinction.
    - **Learner group:** Repeat attempt takes priority; otherwise Lower prior education means No Formal quals or Lower Than A Level; all others are Other learners.
    - **Withdrawal stage:** administrative unregistration day grouped into course weeks. This is not the exact moment of disengagement.
    """)

    st.subheader("Prepared dataset missing values")

    miss = pd.DataFrame([
        {"Field": k, "Missing rows": v}
        for k, v in quality.get("missing_values", {}).items()
        if v and k != "withdrawal_stage_order"
    ])

    if not miss.empty:
        st.dataframe(
            miss.sort_values("Missing rows", ascending=False),
            width="stretch",
            hide_index=True
        )

    st.subheader("Source file row counts")

    raw_counts = pd.DataFrame([
        {"Source CSV": k, "Rows": v}
        for k, v in quality.get("raw_files", {}).items()
    ])

    if not raw_counts.empty:
        st.dataframe(
            raw_counts,
            width="stretch",
            hide_index=True
        )

    st.subheader("Limitations")

    st.markdown("""
    - Activity and completion are observational; association does not establish causation.
    - Video watch-time is not separately measured.
    - The dataset does not contain a reliable first-module completion flag.
    - Learner groups are descriptive, not a basis for punitive decisions. Use aggregated reporting and support-oriented interventions.
    """)

    st.download_button(
        "Download filtered learner table",
        d.to_csv(index=False).encode("utf-8"),
        "filtered_learner_features.csv",
        "text/csv"
    )

    if quality:
        st.download_button(
            "Download data quality report",
            json.dumps(quality, indent=2).encode("utf-8"),
            "data_quality_report.json",
            "application/json"
        )


# FOOTER
st.divider()

st.caption(
    "OULAD · Kuzilek, Hlosta & Zdrahal (2017), Scientific Data. "
    "Learner IDs are removed from the prepared analysis table."
)
