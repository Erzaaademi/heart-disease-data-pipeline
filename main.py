"""
CLI entrypoint (Person 2): run processing, write CSVs + JSON, print a short summary.

Run from project root:
  python main.py --input data/test.csv --output out/run1
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow "import analysis" / "import processing" when running main.py from repo root
# (src is not installed as a package in this small project).
_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from analysis import (  # noqa: E402
    build_summary_report,
    print_console_summary,
    save_summary_json,
)
from processing import process_data  # noqa: E402


def parse_args() -> argparse.Namespace:
    """Define --input and --output; both required."""
    p = argparse.ArgumentParser(
        description="Run the heart disease data pipeline on one CSV (train or test schema)."
    )
    p.add_argument(
        "--input",
        required=True,
        help="Path to input CSV (headers must match train or test schema).",
    )
    p.add_argument(
        "--output",
        required=True,
        help="Directory for cleaned_data.csv, rejected_data.csv, summary_report.json.",
    )
    return p.parse_args()


def main() -> int:
    """
    Exit 0 on success, 1 on user or validation error.

    ValueError from process_data (bad headers, etc.) is turned into stderr + exit 1.
    """
    args = parse_args()
    input_path = Path(args.input)
    out_dir = Path(args.output)

    if not input_path.is_file():
        print(f"error: input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        cleaned_df, rejected_df = process_data(str(input_path))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    report = build_summary_report(cleaned_df, rejected_df)

    out_dir.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(out_dir / "cleaned_data.csv", index=False)
    rejected_df.to_csv(out_dir / "rejected_data.csv", index=False)
    save_summary_json(report, out_dir / "summary_report.json")

    print_console_summary(report)
    print(f"Wrote outputs under: {out_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
