"""
Summaries and stats for pipeline outputs (Person 2).

Input: cleaned_df (accepted rows) and rejected_df (failed rows + "reason").
Output: JSON-serializable dict, optional console lines. Safe on empty frames or missing columns.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

# Columns we summarize as categorical counts (skip if absent from cleaned_df, e.g. test has no label).
CATEGORICAL_COLUMNS = [
    "Sex",
    "Chest pain type",
    "FBS over 120",
    "EKG results",
    "Exercise angina",
    "Slope of ST",
    "Thallium",
    "Heart Disease",
]


def _safe_total(cleaned_df: pd.DataFrame, rejected_df: pd.DataFrame) -> int:
    """Total rows seen in this run = accepted + rejected (matches process_data split)."""
    return int(len(cleaned_df)) + int(len(rejected_df))


def rejection_reason_counts(rejected_df: pd.DataFrame) -> dict[str, int]:
    """
    Count how often each rejection reason occurred.

    Returns {} if there are no rejections or no "reason" column (defensive).
    """
    if rejected_df.empty or "reason" not in rejected_df.columns:
        return {}
    s = rejected_df["reason"].fillna("(missing reason)").astype(str)
    return {str(k): int(v) for k, v in s.value_counts().items()}


def numeric_summary(cleaned_df: pd.DataFrame) -> dict[str, dict[str, float]]:
    """
    Per-column mean/min/max on cleaned data only, for values that parse as numbers.

    Skips "Heart Disease" (string label). Skips columns with no numeric values after coercion.
    """
    if cleaned_df.empty:
        return {}
    out: dict[str, dict[str, float]] = {}
    for col in cleaned_df.columns:
        if col == "Heart Disease":
            continue
        converted = pd.to_numeric(cleaned_df[col], errors="coerce")
        if not converted.notna().any():
            continue
        out[col] = {
            "mean": float(converted.mean()),
            "min": float(converted.min()),
            "max": float(converted.max()),
        }
    return out


def categorical_distributions(cleaned_df: pd.DataFrame) -> dict[str, dict[str, int]]:
    """
    Value counts for selected low-cardinality columns on accepted rows only.

    Missing values are bucketed as "(missing)" so JSON stays simple.
    """
    if cleaned_df.empty:
        return {}
    dists: dict[str, dict[str, int]] = {}
    for col in CATEGORICAL_COLUMNS:
        if col not in cleaned_df.columns:
            continue
        vc = cleaned_df[col].fillna("(missing)").astype(str).value_counts()
        dists[col] = {str(k): int(v) for k, v in vc.items()}
    return dists


def build_summary_report(
    cleaned_df: pd.DataFrame, rejected_df: pd.DataFrame
) -> dict[str, Any]:
    """
    Build the full summary dict written to summary_report.json.

    When total_rows == 0, rates are 0.0 (avoid divide-by-zero).
    """
    total_rows = _safe_total(cleaned_df, rejected_df)
    accepted_rows = int(len(cleaned_df))
    rejected_rows = int(len(rejected_df))

    if total_rows > 0:
        acceptance_rate = accepted_rows / total_rows
        rejection_rate = rejected_rows / total_rows
    else:
        acceptance_rate = 0.0
        rejection_rate = 0.0

    return {
        "total_rows": total_rows,
        "accepted_rows": accepted_rows,
        "rejected_rows": rejected_rows,
        "acceptance_rate": round(acceptance_rate, 6),
        "rejection_rate": round(rejection_rate, 6),
        "rejection_reasons_count": rejection_reason_counts(rejected_df),
        "numeric_stats_cleaned": numeric_summary(cleaned_df),
        "categorical_distributions_cleaned": categorical_distributions(cleaned_df),
    }


def save_summary_json(report: dict[str, Any], path: Path) -> None:
    """Write UTF-8 JSON with readable indentation; create parent dirs if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def print_console_summary(report: dict[str, Any]) -> None:
    """Human-readable one-screen overview; top 5 rejection reasons by frequency."""
    print("Heart Disease Data Pipeline - summary")
    print(f"  total_rows:      {report['total_rows']}")
    print(f"  accepted_rows:   {report['accepted_rows']}")
    print(f"  rejected_rows:   {report['rejected_rows']}")
    print(f"  acceptance_rate: {report['acceptance_rate']:.2%}")
    print(f"  rejection_rate:  {report['rejection_rate']:.2%}")
    reasons = report.get("rejection_reasons_count") or {}
    top = sorted(reasons.items(), key=lambda x: -x[1])[:5]
    if top:
        print("  top rejection reasons:")
        for reason, count in top:
            print(f"    - {reason}: {count}")
    else:
        print("  top rejection reasons: (none)")
