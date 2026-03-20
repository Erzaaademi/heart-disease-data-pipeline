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