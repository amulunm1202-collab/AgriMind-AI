# ============================================================
# AGRIMIND AI - REAL CROP RECOMMENDATION MODEL TRAINING
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
    "Crop_recommendation.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "crop_recommendation_model.pkl"
)


# ============================================================
# START
# ============================================================

print("\n==============================================")
print("   AGRIMIND AI CROP MODEL TRAINING")
print("==============================================")

print("\nDataset:")
print(DATA_PATH)


# ============================================================
# CHECK DATASET
# ============================================================

if not os.path.isfile(DATA_PATH):

    raise FileNotFoundError(
        f"""
Crop recommendation dataset not found.

Expected:
{DATA_PATH}
"""
    )


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    DATA_PATH
)

print("\nDataset shape:")
print(df.shape)

print("\nOriginal columns:")
print(list(df.columns))


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)


print("\nCleaned columns:")
print(list(df.columns))


# ============================================================
# EXPECTED FEATURES
# ============================================================

FEATURES = [

    "n",
    "p",
    "k",
    "temperature",
    "humidity",
    "ph",
    "rainfall"

]


TARGET = "label"


# ============================================================
# CHECK COLUMNS
# ============================================================

required_columns = FEATURES + [TARGET]

missing_columns = [

    column

    for column in required_columns

    if column not in df.columns

]


if missing_columns:

    raise ValueError(
        "\nMissing columns:\n"
        + str(missing_columns)
        + "\n\nAvailable columns:\n"
        + str(list(df.columns))
    )


print("\n✓ Required columns found.")


# ============================================================
# REMOVE MISSING DATA
# ============================================================

df = df.dropna(
    subset=required_columns
)


print(
    "\nSamples after cleaning:",
    len(df)
)


# ============================================================
# FEATURES AND TARGET
# ============================================================

X = df[
    FEATURES
]

y = df[
    TARGET
]


# ============================================================
# DISPLAY CROPS
# ============================================================

print("\nCrops in dataset:")

for crop in sorted(
    y.unique()
):

    print(
        " -",
        crop
    )


print(
    "\nNumber of crop classes:",
    y.nunique()
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


print(
    "\nTraining samples:",
    len(X_train)
)

print(
    "Testing samples:",
    len(X_test)
)


# ============================================================
# RANDOM FOREST
# ============================================================

print(
    "\nTraining Random Forest..."
)


model = RandomForestClassifier(

    n_estimators=300,

    random_state=42,

    n_jobs=-1

)


model.fit(

    X_train,

    y_train

)


print(
    "✓ Training completed."
)


# ============================================================
# TEST MODEL
# ============================================================

predictions = model.predict(
    X_test
)


accuracy = accuracy_score(

    y_test,

    predictions

)


print("\n==============================================")
print("              MODEL RESULTS")
print("==============================================")


print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)


print(
    "\nClassification report:"
)


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

    "model":
        model,

    "features":
        FEATURES,

    "classes":
        sorted(
            y.unique()
        )

}


with open(

    MODEL_PATH,

    "wb"

) as file:

    pickle.dump(

        model_package,

        file

    )


# ============================================================
# COMPLETE
# ============================================================

print("\n==============================================")
print("       ✓ CROP MODEL SAVED SUCCESSFULLY")
print("==============================================")

print(
    "\nModel:"
)

print(
    MODEL_PATH
)

print(
    "\nFeatures:"
)

print(
    FEATURES
)

print(
    "\nCrop classes:"
)

print(
    len(
        model_package["classes"]
    )
)

print(
    "\nTraining completed."
)