# Cleaning log

## Source
Open University Learning Analytics Dataset (OULAD), seven CSV files:
- `studentInfo.csv`: 32,593 rows
- `studentRegistration.csv`: 32,593 rows
- `studentVle.csv`: 10,655,280 rows
- `vle.csv`: 6,364 rows
- `courses.csv`: 22 rows
- `assessments.csv`: 206 rows
- `studentAssessment.csv`: 173,912 rows

## Processing decisions
1. Joined learner profile and registration on `code_module`, `code_presentation`, and `id_student`; join validated one-to-one.
2. Joined course metadata on course and presentation; join validated many-to-one.
3. Read the 10.65-million-row VLE clickstream in 500,000-row chunks to limit memory use.
4. Joined VLE site metadata on site, module and presentation, then aggregated only days 0–27 for early activity.
5. Aggregated total early clicks, distinct active days and clicks by VLE activity type.
6. Joined assessment submissions to assessment metadata; counted submissions in days 0–27 and calculated mean score where available.
7. Parsed source `?` placeholders as missing values.
8. Treated no first-28-day VLE activity as zero observed clicks; treated no early assessment submission as zero submissions.
9. Filled missing activity-type click counts with zero after the aggregation, because no event for that activity type means no recorded click in that window.
10. Did not impute missing demographic values or early assessment scores.
11. Kept registrations with missing dates. Non-withdrawn learners are labelled Not withdrawn; 93 withdrawn records without an unregistration day are labelled Unknown withdrawal date.
12. Removed the direct `id_student` identifier from the exported feature table. No learner-course records were removed.

## Reconciliation
- Output: 32,593 learner-course-presentation rows.
- Duplicate learner-course-presentation keys before identifier removal: 0.
- Outcomes: Pass 12,361; Distinction 3,024; Fail 7,052; Withdrawn 10,156.
- Missing source fields retained and documented in `data/processed/data_quality_report.json`.

## Why these choices matter
The analysis keeps the full registered population, including learners without recorded VLE activity. This avoids silently dropping low-activity learners and inflating engagement estimates. Structural missing values are distinguished from true zero activity.
