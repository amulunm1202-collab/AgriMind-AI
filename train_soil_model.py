# ============================================================
# AGRIMIND AI - SOIL MODEL TRAINING
# ============================================================

import os
import sys
import pickle
import pandas as pd

# Make console output UTF-8 safe (Windows cp1252 cannot encode emoji).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "soil_data.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "soil_fertility_model.pkl"
)


# ============================================================
# CHECK DATASET
# ============================================================

if not os.path.isfile(DATA_PATH):

    raise FileNotFoundError(
        f"""
Soil dataset not found.

Expected:
{DATA_PATH}

Create this structure:

AgriMind AI/
├── train_soil_model.py
├── data/
│   └── soil_data.csv
├── models/
└── backend/
"""
    )


print("\n==============================================")
print("       AGRIMIND AI SOIL MODEL TRAINING")
print("==============================================")

print("\nDataset:")
print(DATA_PATH)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(DATA_PATH)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(list(df.columns))

print("\nFirst rows:")
print(df.head())


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


print("\nCleaned columns:")
print(list(df.columns))


# ============================================================
# TARGET COLUMN
# ============================================================

possible_targets = [
    "fertility",
    "soil_fertility",
    "fertility_level",
    "label",
    "class",
    "target"
]

target_column = None

for column in possible_targets:

    if column in df.columns:

        target_column = column

        break


if target_column is None:

    raise ValueError(
        "\nCould not find the soil fertility target column.\n"
        "Available columns:\n"
        + str(list(df.columns))
    )


print(
    "\nTarget column:",
    target_column
)


# ============================================================
# REMOVE EMPTY ROWS
# ============================================================

df = df.dropna()

print(
    "\nRows after cleaning:",
    len(df)
)


# ============================================================
# FEATURES
# ============================================================

X = df.drop(
    columns=[target_column]
)

y = df[target_column]


# ============================================================
# KEEP NUMERIC FEATURES
# ============================================================

numeric_columns = X.select_dtypes(
    include=["number"]
).columns.tolist()


if len(numeric_columns) == 0:

    raise ValueError(
        "No numeric soil features were found."
    )


X = X[numeric_columns]


print("\nFeatures used:")

for column in numeric_columns:

    print(
        " -",
        column
    )


print("\nTarget classes:")

print(
    sorted(
        y.astype(str).unique()
    )
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# RANDOM FOREST MODEL
# ============================================================

print("\nTraining Random Forest...")


model = RandomForestClassifier(

    n_estimators=300,

    random_state=42,

    class_weight="balanced",

    n_jobs=-1
)


model.fit(
    X_train,
    y_train
)


# ============================================================
# EVALUATION
# ============================================================

predictions = model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print("\n==============================================")
print("MODEL RESULTS")
print("==============================================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


print("\nClassification report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


model_package = {

    "model": model,

    "features": numeric_columns,

    "target_column": target_column
}


with open(
    MODEL_PATH,
    "wb"
) as file:

    pickle.dump(
        model_package,
        file
    )


print("\n==============================================")
print("✓ SOIL MODEL SAVED")
print("==============================================")

print(
    MODEL_PATH
)

print("\nFeatures saved:")
print(numeric_columns)

print("\nTraining completed successfully.")