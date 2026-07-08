"""
Unit tests for compute_variance.py's core logic.

Run with: python3 test_compute_variance.py
"""

import unittest

import pandas as pd

from compute_variance import add_variance, add_ytd


class TestAddVariance(unittest.TestCase):
    def test_on_track_within_threshold(self):
        df = pd.DataFrame({"budget_amount": [100_000.0], "actual_amount": [105_000.0]})
        result = add_variance(df)
        self.assertEqual(result.loc[0, "variance_dollars"], 5_000.0)
        self.assertEqual(result.loc[0, "variance_pct"], 5.0)
        self.assertEqual(result.loc[0, "flag"], "On Track")

    def test_over_budget_flag_at_threshold_boundary(self):
        df = pd.DataFrame(
            {
                "budget_amount": [100_000.0, 100_000.0],
                "actual_amount": [110_000.0, 111_000.0],
            }
        )
        result = add_variance(df)
        # exactly at the 10% threshold: not flagged (uses strict '>')
        self.assertEqual(result.loc[0, "flag"], "On Track")
        # clearly over (11%, so it stays over threshold even after the
        # variance_pct rounding that happens before the flag check): flagged
        self.assertEqual(result.loc[1, "flag"], "Over Budget")

    def test_under_budget_flag(self):
        df = pd.DataFrame({"budget_amount": [100_000.0], "actual_amount": [85_000.0]})
        result = add_variance(df)
        self.assertEqual(result.loc[0, "variance_pct"], -15.0)
        self.assertEqual(result.loc[0, "flag"], "Under Budget")


class TestAddYTD(unittest.TestCase):
    def test_ytd_accumulates_across_months_per_department(self):
        df = pd.DataFrame(
            {
                "department": ["Sales", "Sales", "Marketing"],
                "month": ["2025-02", "2025-01", "2025-01"],
                "budget_amount": [100_000.0, 100_000.0, 50_000.0],
                "actual_amount": [90_000.0, 110_000.0, 50_000.0],
            }
        )
        result = add_ytd(df).set_index(["department", "month"])

        # Sales Jan: first month, YTD == that month's own numbers.
        self.assertEqual(result.loc[("Sales", "2025-01"), "ytd_budget"], 100_000.0)
        self.assertEqual(result.loc[("Sales", "2025-01"), "ytd_actual"], 110_000.0)

        # Sales Feb: YTD should be the sum of Jan + Feb, in month order
        # (not input row order, since Feb was listed first in the input).
        self.assertEqual(result.loc[("Sales", "2025-02"), "ytd_budget"], 200_000.0)
        self.assertEqual(result.loc[("Sales", "2025-02"), "ytd_actual"], 200_000.0)
        self.assertEqual(result.loc[("Sales", "2025-02"), "ytd_variance_dollars"], 0.0)

        # Marketing is a separate department; its YTD must not include Sales.
        self.assertEqual(result.loc[("Marketing", "2025-01"), "ytd_budget"], 50_000.0)


if __name__ == "__main__":
    unittest.main()
