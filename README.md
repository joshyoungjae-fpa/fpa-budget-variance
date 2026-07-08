# Budget vs. Actual Variance — FP&A Practice Project

A mock company's monthly budget and actuals by department, for practicing
budget-vs-actual variance analysis with Claude Code, hands-on.

## What's in this folder
- `budget.csv` — monthly budgeted opex for 5 departments (Sales, Marketing,
  R&D, Customer Success, G&A), Jan–Dec 2025.
- `actuals.csv` — actual monthly spend for the same departments/months.
- `compute_variance.py` — joins the two, computes $ and % variance, flags
  months that are meaningfully over/under budget, and rolls up
  year-to-date (YTD) budget/actual/variance per department.

## Columns
| column | meaning |
|---|---|
| department | Sales / Marketing / R&D / Customer Success / G&A |
| month | YYYY-MM |
| budget_amount | budgeted spend for that department/month |
| actual_amount | actual spend for that department/month |

Note: R&D's budget steps up starting July (an approved headcount ramp) —
that's a real planned change, not noise, and worth treating differently
from an unplanned overspend.

## How to run this session

1. Open a terminal, `cd` into this folder.
2. Run `claude` to start a session.
3. Paste this as your first prompt:

```
I have two CSVs: budget.csv (department, month, budget_amount) and
actuals.csv (department, month, actual_amount).

Write a Python script using pandas that joins them by department and month,
then computes:
- variance_dollars (actual - budget)
- variance_pct
- a flag: "Over Budget" / "Under Budget" if |variance_pct| exceeds 10%,
  else "On Track"
- year-to-date (YTD) cumulative budget, actual, and variance per department

Output a clean CSV (variance_report.csv) and print a summary table to the
terminal, plus a short list of just the flagged department-months.
```

4. Let it read the files, write the script, and **run it**. Some months
   are deliberately over/under budget for real reasons (a trade show, a
   late start date, annual audit fees) — see if it can help you explain
   *why*, not just report *that* a number moved.

## Good follow-up prompts once it works
- "Which department has the worst YTD variance, and is it trending better
  or worse each quarter?"
- "Add a rolling 3-month average variance_pct per department to spot a
  trend instead of one noisy month."
- "Chart YTD budget vs. actual per department as a bar chart."
- "Write a CLAUDE.md for this project so next month I can just drop in a
  new month's actuals and ask you to rerun it."

## What to watch for as you learn
- Does it ask before overwriting files, or just do it?
- When a number looks flagged, does it explain the likely driver before
  suggesting an action, or just report the flag?
- Try `/clear` after this session finishes, then reopen and ask "what
  does this project do?" — see how much it picks up from CLAUDE.md alone.
