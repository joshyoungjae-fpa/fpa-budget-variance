"""
Monthly budget-vs-actual variance report from budget.csv and actuals.csv.

Sign convention: variance_dollars = actual - budget, so a positive number
means overspend and a negative number means underspend.

Flagging: a month/department is flagged "Over Budget" or "Under Budget"
when |variance_pct| exceeds FLAG_THRESHOLD_PCT; otherwise "On Track".
"""

import pandas as pd

BUDGET_CSV = "budget.csv"
ACTUALS_CSV = "actuals.csv"
OUTPUT_CSV = "variance_report.csv"
FLAG_THRESHOLD_PCT = 10.0


def load_data(budget_path: str, actuals_path: str) -> pd.DataFrame:
    budget = pd.read_csv(budget_path)
    actuals = pd.read_csv(actuals_path)
    merged = budget.merge(actuals, on=["department", "month"], how="outer", validate="one_to_one")
    if merged[["budget_amount", "actual_amount"]].isna().any().any():
        missing = merged[merged[["budget_amount", "actual_amount"]].isna().any(axis=1)]
        raise ValueError(f"budget/actuals don't line up for these rows:\n{missing}")
    return merged


def add_variance(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["variance_dollars"] = (df["actual_amount"] - df["budget_amount"]).round(2)
    df["variance_pct"] = (df["variance_dollars"] / df["budget_amount"] * 100).round(1)
    df["flag"] = "On Track"
    df.loc[df["variance_pct"] > FLAG_THRESHOLD_PCT, "flag"] = "Over Budget"
    df.loc[df["variance_pct"] < -FLAG_THRESHOLD_PCT, "flag"] = "Under Budget"
    return df


def add_ytd(df: pd.DataFrame) -> pd.DataFrame:
    """Year-to-date cumulative budget/actual/variance per department, ordered by month."""
    df = df.sort_values(["department", "month"]).copy()
    df["ytd_budget"] = df.groupby("department")["budget_amount"].cumsum().round(2)
    df["ytd_actual"] = df.groupby("department")["actual_amount"].cumsum().round(2)
    df["ytd_variance_dollars"] = (df["ytd_actual"] - df["ytd_budget"]).round(2)
    return df


def main():
    merged = load_data(BUDGET_CSV, ACTUALS_CSV)
    report = add_variance(merged)
    report = add_ytd(report)
    report = report[
        [
            "department",
            "month",
            "budget_amount",
            "actual_amount",
            "variance_dollars",
            "variance_pct",
            "flag",
            "ytd_budget",
            "ytd_actual",
            "ytd_variance_dollars",
        ]
    ]

    report.to_csv(OUTPUT_CSV, index=False)

    with pd.option_context("display.float_format", lambda x: f"{x:,.1f}", "display.width", 160):
        print(report.to_string(index=False))

    flagged = report[report["flag"] != "On Track"]
    print(f"\n{len(flagged)} department-months flagged (>|{FLAG_THRESHOLD_PCT}%| variance):")
    if len(flagged):
        print(flagged[["department", "month", "variance_pct", "flag"]].to_string(index=False))
    else:
        print("none")

    print(f"\nWrote {OUTPUT_CSV} ({len(report)} rows).")


if __name__ == "__main__":
    main()
