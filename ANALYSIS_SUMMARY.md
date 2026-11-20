# Analysis summary — actual OULAD records

## Executive results
- 32,593 registrations across seven course modules and multiple presentations.
- 15,385 learners (47.2%) achieved Pass or Distinction.
- 10,156 (31.2%) withdrew; 7,052 (21.6%) failed.
- 2,676 withdrawals were recorded before course start. Of withdrawals with a known post-start date, Week 2 is the largest stage (1,068).
- 93 withdrawn records have no recorded unregistration day.

## Early engagement
Engaged = >=10 clicks and >=3 active days during the first 28 days.
- Engaged: 24,908 learners; 57.5% successful completion; 21.2% withdrawn.
- Not engaged: 7,685 learners; 13.8% successful completion; 63.4% withdrawn.
- At-risk flag: 8,212 learners (25.2%); 16.6% successful completion and 60.3% withdrawn.

## Learner groups
| Group | Learners | At-risk | Successful completion | Withdrawn |
|---|---:|---:|---:|---:|
| Repeat attempt | 4,172 | 34.6% | 33.1% | 35.3% |
| Lower prior education | 11,591 | 29.0% | 40.6% | 34.8% |
| Other learners | 16,830 | 20.2% | 55.2% | 27.6% |

## Predictive check
A stratified 80/20 hold-out logistic regression compared a context-only baseline with a model adding first-28-day activity and assessment signals.
- Baseline ROC-AUC: 0.649.
- With early signals: 0.822.
- Test set: 6,519 learners.
This suggests early signals improve prediction in this dataset; it does not show that changing activity causes completion.

## Activity comparison
| Early VLE activity | Learners with activity | Completion among users | Completion among non-users |
|---|---:|---:|---:|
| Forum (`forumng`) | 22,819 | 57.9% | 22.3% |
| Quiz (`quiz`) | 13,365 | 57.9% | 39.8% |
| Course content (`oucontent`) | 23,149 | 56.3% | 24.9% |
| Generic URL (`url`) | 19,544 | 58.4% | 30.5% |

These comparisons are descriptive and likely reflect underlying engagement differences. OULAD does not separately measure video watch-time; generic URL activity is not a valid video-view measure.
