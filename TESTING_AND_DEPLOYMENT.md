# Two-person usability test and submission checklist

## Test with two viewers
Ask each person to use the dashboard for 2–3 minutes without coaching.

1. Can you identify the most common recorded withdrawal stage?
2. Can you identify the learner group with the highest early at-risk rate?
3. Can you explain how early engagement relates to successful completion?
4. Can you find the comparison between forum and quiz activity?
5. Is it clear why the dashboard does not claim to measure video watch-time?
6. What label, chart or definition was confusing?

Record each person's confusion and the change made. Do not claim this test is complete until two people have actually reviewed the dashboard.

## Submission checklist
- [x] Actual OULAD dataset processed; 32,593 learner-course rows.
- [x] Cleaning log and data dictionary.
- [x] Eight dashboard charts and filters for course/presentation, term and learner group.
- [x] Data quality and assumptions page.
- [x] One-page recommendation memo.
- [x] What-if control using an explicitly labelled early-engagement proxy.
- [x] Walkthrough script.
- [ ] Deploy the Streamlit app and paste the live URL into the submission.
- [ ] Record a short screen walkthrough.
- [ ] Ask two people to test the dashboard and document any fixes.

## Publish the live dashboard
1. Create a GitHub repository, e.g. `learner-dropoff-analytics`.
2. Upload the contents of this project folder (not the outer ZIP itself).
3. Open Streamlit Community Cloud and choose **Create app**.
4. Select the GitHub repository, branch `main`, and main file `app.py`.
5. Deploy. The prepared dataset is included, so no raw CSV upload is needed for the dashboard.
6. Open the public app URL and test all three filters before submitting.
