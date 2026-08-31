# ============================================================
# AGRIMIND AI - REAL CROP RECOMMENDATION MODEL
# ============================================================

from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR
    / "data"
    / "Crop_recommendation.csv"
)


# ============================================================
# FEATURES
# ============================================================

FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]

TARGET = "label"


# ============================================================
# GLOBAL MODEL
# ============================================================

model = None
model_accuracy = 0.0


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"""
Crop dataset not found.

Expected location:
{DATASET_PATH}
"""
        )

    df = pd.read_csv(DATASET_PATH)

    print("\n==============================================")
    print("AGRIMIND AI CROP DATASET")
    print("==============================================")

    print("Dataset:", DATASET_PATH)
    print("Rows:", len(df))
    print("Columns:", list(df.columns))

    # --------------------------------------------------------
    # CLEAN COLUMN NAMES
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # --------------------------------------------------------
    # STANDARDIZE NPK
    # --------------------------------------------------------

    rename_map = {
        "n": "N",
        "p": "P",
        "k": "K"
    }

    df.rename(
        columns=rename_map,
        inplace=True
    )

    # --------------------------------------------------------
    # CHECK
    # --------------------------------------------------------

    required_columns = FEATURES + [TARGET]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            f"""
Dataset is missing columns:
{missing}

Available columns:
{list(df.columns)}
"""
        )

    # --------------------------------------------------------
    # KEEP ONLY REQUIRED COLUMNS
    # --------------------------------------------------------

    df = df[
        required_columns
    ].copy()

    # --------------------------------------------------------
    # NUMERIC VALUES
    # --------------------------------------------------------

    for column in FEATURES:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # --------------------------------------------------------
    # LABEL
    # --------------------------------------------------------

    df[TARGET] = (
        df[TARGET]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # --------------------------------------------------------
    # REMOVE INVALID DATA
    # --------------------------------------------------------

    df = df.dropna()

    df = df[
        df[TARGET] != ""
    ]

    if len(df) == 0:

        raise ValueError(
            "Crop dataset contains no valid rows."
        )

    print("Valid rows:", len(df))
    print(
        "Crop classes:",
        df[TARGET].nunique()
    )

    print(
        "Crops:",
        sorted(
            df[TARGET].unique()
        )
    )

    print("==============================================\n")

    return df


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model():

    global model
    global model_accuracy

    df = load_dataset()

    X = df[FEATURES]

    y = df[TARGET]

    # --------------------------------------------------------
    # TRAIN / TEST
    # --------------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.20,

        random_state=42,

        stratify=y
    )

    # --------------------------------------------------------
    # RANDOM FOREST
    # --------------------------------------------------------

    model = RandomForestClassifier(

        n_estimators=500,

        random_state=42,

        n_jobs=-1,

        class_weight="balanced",

        max_features="sqrt"
    )

    print(
        "Training Random Forest..."
    )

    model.fit(
        X_train,
        y_train
    )

    # --------------------------------------------------------
    # TEST
    # --------------------------------------------------------

    predictions = model.predict(
        X_test
    )

    model_accuracy = (
        accuracy_score(
            y_test,
            predictions
        )
        * 100
    )

    print("\n==============================================")
    print("CROP MODEL READY")
    print("==============================================")

    print(
        f"Model accuracy: "
        f"{model_accuracy:.2f}%"
    )

    print(
        "Number of crops:",
        len(model.classes_)
    )

    print(
        "Crops:",
        list(model.classes_)
    )

    print("==============================================\n")


# ============================================================
# ENSURE MODEL
# ============================================================

def ensure_model():

    global model

    if model is None:

        train_model()


# ============================================================
# VALIDATION
# ============================================================

def validate_value(
    value,
    name
):

    try:

        value = float(value)

    except (
        TypeError,
        ValueError
    ):

        raise ValueError(
            f"Invalid {name}: {value}"
        )

    if not np.isfinite(value):

        raise ValueError(
            f"Invalid {name}: {value}"
        )

    return value


# ============================================================
# REAL CROP PREDICTION
# ============================================================

def recommend_crop(

    n,
    p,
    k,

    temperature,
    humidity,

    ph,
    rainfall

):

    ensure_model()

    # --------------------------------------------------------
    # VALIDATE
    # --------------------------------------------------------

    n = validate_value(
        n,
        "Nitrogen"
    )

    p = validate_value(
        p,
        "Phosphorus"
    )

    k = validate_value(
        k,
        "Potassium"
    )

    temperature = validate_value(
        temperature,
        "Temperature"
    )

    humidity = validate_value(
        humidity,
        "Humidity"
    )

    ph = validate_value(
        ph,
        "pH"
    )

    rainfall = validate_value(
        rainfall,
        "Rainfall"
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # THESE ARE THE ACTUAL VALUES SENT BY THE SCAN/API
    # --------------------------------------------------------

    values = [

        n,
        p,
        k,

        temperature,
        humidity,

        ph,
        rainfall

    ]

    input_data = pd.DataFrame(

        [values],

        columns=FEATURES

    )

    # --------------------------------------------------------
    # DEBUG
    # --------------------------------------------------------

    print("\n==============================================")
    print("REAL CROP PREDICTION")
    print("==============================================")

    for feature, value in zip(
        FEATURES,
        values
    ):

        print(
            f"{feature:15}: {value}"
        )

    print("==============================================")

    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    predicted_crop = model.predict(
        input_data
    )[0]

    # --------------------------------------------------------
    # PROBABILITY
    # --------------------------------------------------------

    probabilities = model.predict_proba(
        input_data
    )[0]

    classes = model.classes_

    ranked = []

    for crop, probability in zip(
        classes,
        probabilities
    ):

        ranked.append({

            "crop":
                str(crop),

            "confidence":
                round(
                    float(probability)
                    * 100,
                    2
                )

        })

    # --------------------------------------------------------
    # SORT HIGH → LOW
    # --------------------------------------------------------

    ranked.sort(

        key=lambda item:
            item["confidence"],

        reverse=True

    )

    # --------------------------------------------------------
    # TOP 3
    # --------------------------------------------------------

    top_three = ranked[:3]

    best = top_three[0]

    # --------------------------------------------------------
    # PRINT RESULT
    # --------------------------------------------------------

    print("\nRecommended crop:")
    print(
        best["crop"]
    )

    print(
        "Confidence:",
        best["confidence"],
        "%"
    )

    print("\nTop recommendations:")

    for item in top_three:

        print(
            f"{item['crop']} "
            f"→ "
            f"{item['confidence']}%"
        )

    print("==============================================\n")

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "crop":
            best["crop"],

        "recommended_crop":
            best["crop"],

        "confidence":
            best["confidence"],

        "ml_confidence":
            best["confidence"],

        "top_crops": [

            item["crop"]

            for item in top_three

        ],

        "ranked_crops":
            top_three,

        "alternatives": [

            item["crop"]

            for item
            in top_three[1:]

        ],

        "model":
            "Random Forest Classifier",

        "model_accuracy":
            round(
                model_accuracy,
                2
            ),

        "input_values": {

            "N": n,

            "P": p,

            "K": k,

            "temperature":
                temperature,

            "humidity":
                humidity,

            "ph":
                ph,

            "rainfall":
                rainfall

        },

        "reason":
            (
                f"{best['crop'].title()} "
                f"has the highest model "
                f"probability for the supplied "
                f"soil and environmental "
                f"conditions."
            ),

        "message":
            (
                f"{best['crop'].title()} "
                f"is the recommended crop."
            )

    }


# ============================================================
# MODEL INFORMATION
# ============================================================

def get_model_info():

    ensure_model()

    return {

        "model":
            "Random Forest Classifier",

        "dataset":
            str(DATASET_PATH),

        "features":
            FEATURES,

        "classes":
            len(
                model.classes_
            ),

        "accuracy":
            round(
                model_accuracy,
                2
            ),

        "trained":
            model is not None

    }


# ============================================================
# TRAIN WHEN APP STARTS
# ============================================================

try:

    train_model()

except Exception as error:

    print("\n==============================================")
    print("CROP MODEL TRAINING FAILED")
    print("==============================================")

    print(
        repr(error)
    )

    print("==============================================\n")