# Heart Disease Data Pipeline

Small Python pipeline: validate and clean heart-disease CSV rows, write accepted/rejected outputs, and emit a JSON summary with basic statistics.

## Requirements

- Python 3.11+
- Dependencies: see `requirements.txt` (uses **pandas** for DataFrames and analysis)

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

From the project root:

```bash
python main.py --input path/to/input.csv --output path/to/output_dir
```

The output directory will contain:

- `cleaned_data.csv` — rows that passed validation
- `rejected_data.csv` — rows that failed, with a `reason` column
- `summary_report.json` — counts, rates, rejection reasons, numeric and categorical summaries

Input CSV headers must **exactly** match either the **train** schema (includes `Heart Disease`) or the **test** schema (no target column). Definitions live in `src/schema.py`.

## Project layout

| Path | Owner | Role |
|------|--------|------|
| `src/schema.py` | Person 1 | Column lists, ranges, allowed labels |
| `src/processing.py` | Person 1 | Cleaning, validation, `process_data()` |
| `src/analysis.py` | Person 2 | Summary report and stats |
| `main.py` | Person 2 | CLI (`argparse`), writes artifacts, console summary |

## Integration note

`processing.process_data(input_path: str)` returns `(cleaned_df, rejected_df)` as pandas `DataFrame`s. The CLI and `analysis` modules depend on that contract.

## License / data

Add your course or team license and data attribution here if required.
