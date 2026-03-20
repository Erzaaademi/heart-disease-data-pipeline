TRAIN_COLUMNS = [
    "id",
    "Age",
    "Sex",
    "Chest pain type",
    "BP",
    "Cholesterol",
    "FBS over 120",
    "EKG results",
    "Max HR",
    "Exercise angina",
    "ST depression",
    "Slope of ST",
    "Number of vessels fluro",
    "Thallium",
    "Heart Disease"
]

TEST_COLUMNS = [
    "id",
    "Age",
    "Sex",
    "Chest pain type",
    "BP",
    "Cholesterol",
    "FBS over 120",
    "EKG results",
    "Max HR",
    "Exercise angina",
    "ST depression",
    "Slope of ST",
    "Number of vessels fluro",
    "Thallium"
]

REQUIRED_COLUMNS = [
    "id",
    "Age",
    "Sex",
    "Chest pain type",
    "BP",
    "Cholesterol",
    "Max HR",
    "Exercise angina",
    "ST depression",
    "Slope of ST",
    "Number of vessels fluro",
    "Thallium"
]

NUMERIC_RANGES = {
    "id": (0, 10000000),
    "Age": (1, 120),
    "Sex": (0, 1),
    "Chest pain type": (1, 4),
    "BP": (1, 300),
    "Cholesterol": (1, 700),
    "FBS over 120": (0, 1),
    "EKG results": (0, 2),
    "Max HR": (1, 250),
    "Exercise angina": (0, 1),
    "ST depression": (0, 10),
    "Slope of ST": (1, 3),
    "Number of vessels fluro": (0, 4),
    "Thallium": (3, 7)
}

ALLOWED_HEART_DISEASE = {"Presence", "Absence"}

MISSING_VALUES = {"", "NA", "N/A", "null", "None"}