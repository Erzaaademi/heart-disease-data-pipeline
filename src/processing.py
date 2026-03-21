import csv
import os
from schema import  (
    TRAIN_COLUMNS,
    TEST_COLUMNS,
    REQUIRED_COLUMNS,
    NUMERIC_RANGES,
    ALLOWED_HEART_DISEASE,
    MISSING_VALUES
)


def clean_value(value):
    if value is None:
        return None

    value = str(value).strip()

    if value in MISSING_VALUES:
        return None

    return value


def clean_row(row, expected_columns):
    cleaned_row = {}

    for column in expected_columns:
        cleaned_row[column] = clean_value(row.get(column))

    return cleaned_row
def check_columns(actual_columns, file_type):
    if file_type == "train":
        return actual_columns == TRAIN_COLUMNS
    elif file_type == "test":
        return actual_columns == TEST_COLUMNS
    return False


def validate_row(row, seen_ids, file_type):
    for column in REQUIRED_COLUMNS:
        if row.get(column) is None:
            return False, f"missing required value in {column}"

    for column, (min_value, max_value) in NUMERIC_RANGES.items():
        value = row.get(column)

        if value is None:
            return False, f"missing numeric value in {column}"

        try:
            number = float(value)
        except ValueError:
            return False, f"invalid number in {column}"

        if number < min_value or number > max_value:
            return False, f"out of range value in {column}"

    row_id = row["id"]
    if row_id in seen_ids:
        return False, "duplicate id"
    seen_ids.add(row_id)

    if file_type == "train":
        target = row.get("Heart Disease")
        if target is None:
            return False, "missing Heart Disease value"
        if target not in ALLOWED_HEART_DISEASE:
            return False, "invalid Heart Disease value"

    return True, "accepted"

def load_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        columns = reader.fieldnames
    return columns, rows


def save_csv(file_path, rows, headers):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def process_file(input_file, output_folder, file_type):
    columns, rows = load_csv(input_file)

    if not check_columns(columns, file_type):
        raise ValueError("Column names do not match expected schema")

    expected_columns = TRAIN_COLUMNS if file_type == "train" else TEST_COLUMNS

    cleaned_rows = []
    rejected_rows = []
    seen_ids = set()

    for row in rows:
        cleaned_row = clean_row(row, expected_columns)
        is_valid, reason = validate_row(cleaned_row, seen_ids, file_type)

        if is_valid:
            cleaned_rows.append(cleaned_row)
        else:
            rejected_row = cleaned_row.copy()
            rejected_row["reason"] = reason
            rejected_rows.append(rejected_row)

    os.makedirs(output_folder, exist_ok=True)

    cleaned_file = os.path.join(output_folder, f"{file_type}_cleaned_data.csv")
    rejected_file = os.path.join(output_folder, f"{file_type}_rejected_data.csv")

    cleaned_headers = expected_columns
    rejected_headers = expected_columns + ["reason"]

    save_csv(cleaned_file, cleaned_rows, cleaned_headers)
    save_csv(rejected_file, rejected_rows, rejected_headers)

    return {
        "total_rows": len(rows),
        "accepted_rows": len(cleaned_rows),
        "rejected_rows": len(rejected_rows)
    }