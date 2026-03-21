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