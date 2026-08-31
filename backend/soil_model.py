# ============================================================
# AGRIMIND AI - SOIL ANALYSIS MODEL
# RENDER SAFE VERSION
# ============================================================

import os

import pandas as pd
import numpy as np


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# DATASET PATH
# ============================================================

DATA_PATH = os.path.abspath(

    os.path.join(

        BASE_DIR,
        "..",
        "data",
        "soil_data.csv"

    )

)


# ============================================================
# SOIL FEATURES
# ============================================================

SOIL_FEATURES = [

    "ph",
    "ec",
    "oc",
    "n",
    "p",
    "k",
    "s",
    "zn",
    "b",
    "fe",
    "mn",
    "cu"

]


# ============================================================
# LOAD DATASET
# ============================================================

print("==============================================")
print("Loading soil dataset...")
print("==============================================")


if not os.path.isfile(DATA_PATH):

    raise FileNotFoundError(

        "\nSoil dataset not found.\n"
        f"Expected:\n{DATA_PATH}\n"

    )


try:

    soil_data = pd.read_csv(
        DATA_PATH
    )

except Exception as error:

    raise RuntimeError(
        f"Unable to load soil dataset: {error}"
    )


# ============================================================
# CLEAN COLUMNS
# ============================================================

soil_data.columns = (

    soil_data.columns
    .str.strip()
    .str.lower()
    .str.replace(
        " ",
        "_"
    )

)


print(
    "Soil samples:",
    len(soil_data)
)


# ============================================================
# CHECK FEATURES
# ============================================================

missing_features = [

    feature

    for feature in SOIL_FEATURES

    if feature not in soil_data.columns

]


if missing_features:

    raise ValueError(

        "Missing soil features:\n"
        + str(missing_features)

    )


# ============================================================
# NUMERIC CONVERSION
# ============================================================

for feature in SOIL_FEATURES:

    soil_data[feature] = pd.to_numeric(

        soil_data[feature],

        errors="coerce"

    )


# ============================================================
# DATASET LIMITS
# ============================================================

SOIL_LIMITS = {}


for feature in SOIL_FEATURES:

    values = (

        soil_data[
            feature
        ]
        .dropna()

    )


    if len(values) == 0:

        continue


    SOIL_LIMITS[feature] = {

        "min":
            float(values.min()),

        "max":
            float(values.max()),

        "mean":
            float(values.mean())

    }


print("✓ Soil dataset ready.")


# ============================================================
# SOIL ANALYSIS
# ============================================================

def analyze_soil(values):

    if not isinstance(
        values,
        dict
    ):

        raise ValueError(
            "Soil values must be a dictionary."
        )


    cleaned = {}


    # --------------------------------------------------------
    # READ VALUES
    # --------------------------------------------------------

    for feature in SOIL_FEATURES:

        if feature not in values:

            raise ValueError(
                f"Missing soil value: {feature}"
            )


        try:

            number = float(
                values[feature]
            )

        except Exception:

            raise ValueError(

                f"Invalid value for {feature}: "
                f"{values[feature]}"

            )


        if not np.isfinite(number):

            raise ValueError(
                f"Invalid numeric value for {feature}."
            )


        cleaned[feature] = number


    # ========================================================
    # NUTRIENT STATUS
    # ========================================================

    nutrient_status = {}


    for feature in SOIL_FEATURES:

        value = cleaned[
            feature
        ]


        limits = SOIL_LIMITS.get(
            feature
        )


        if not limits:

            nutrient_status[feature] = {

                "value":
                    value,

                "status":
                    "Unknown"

            }

            continue


        minimum = limits[
            "min"
        ]


        maximum = limits[
            "max"
        ]


        mean = limits[
            "mean"
        ]


        if maximum == minimum:

            relative = 0.5

        else:

            relative = (

                value - minimum

            ) / (

                maximum - minimum

            )


        if relative < 0.25:

            status = "Low"

        elif relative < 0.50:

            status = "Moderate"

        elif relative < 0.75:

            status = "Good"

        else:

            status = "High"


        nutrient_status[feature] = {

            "value":
                round(value, 3),

            "status":
                status,

            "dataset_min":
                round(minimum, 3),

            "dataset_max":
                round(maximum, 3),

            "dataset_mean":
                round(mean, 3)

        }


    # ========================================================
    # PH
    # ========================================================

    ph = cleaned[
        "ph"
    ]


    if 6.0 <= ph <= 7.5:

        ph_score = 100

        ph_status = "Optimal"

    elif (
        5.5 <= ph < 6.0
        or
        7.5 < ph <= 8.0
    ):

        ph_score = 75

        ph_status = "Acceptable"

    elif (
        5.0 <= ph < 5.5
        or
        8.0 < ph <= 8.5
    ):

        ph_score = 50

        ph_status = "Needs attention"

    else:

        ph_score = 25

        ph_status = "Poor"


    score_parts = [

        ph_score

    ]


    # ========================================================
    # NPK
    # ========================================================

    for nutrient in [

        "n",
        "p",
        "k"

    ]:

        status = nutrient_status[
            nutrient
        ]["status"]


        if status == "Low":

            score = 25

        elif status == "Moderate":

            score = 60

        elif status == "Good":

            score = 85

        elif status == "High":

            score = 75

        else:

            score = 50


        score_parts.append(
            score
        )


    # ========================================================
    # ORGANIC CARBON
    # ========================================================

    oc_status = nutrient_status[
        "oc"
    ]["status"]


    if oc_status == "Low":

        score_parts.append(
            30
        )

    elif oc_status == "Moderate":

        score_parts.append(
            60
        )

    elif oc_status == "Good":

        score_parts.append(
            90
        )

    else:

        score_parts.append(
            75
        )


    # ========================================================
    # SCORE
    # ========================================================

    soil_score = round(

        float(
            np.mean(
                score_parts
            )
        ),

        1

    )


    # ========================================================
    # CONDITION
    # ========================================================

    if soil_score >= 80:

        soil_condition = "Good"

    elif soil_score >= 60:

        soil_condition = "Moderate"

    else:

        soil_condition = "Needs Improvement"


    # ========================================================
    # LIMITING FACTORS
    # ========================================================

    limiting_factors = []


    for nutrient in [

        "n",
        "p",
        "k",
        "s",
        "zn",
        "b",
        "fe",
        "mn",
        "cu",
        "oc"

    ]:

        if nutrient not in nutrient_status:

            continue


        if (

            nutrient_status[
                nutrient
            ]["status"]

            == "Low"

        ):

            limiting_factors.append(
                nutrient.upper()
            )


    if ph_status in [

        "Needs attention",
        "Poor"

    ]:

        limiting_factors.append(
            "pH"
        )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    recommendations = []


    if ph_status == "Optimal":

        recommendations.append(

            "Soil pH is within a generally "
            "suitable agricultural range."

        )

    elif ph_status == "Acceptable":

        recommendations.append(

            "Soil pH is acceptable but "
            "should be monitored."

        )

    else:

        recommendations.append(

            "Soil pH may require "
            "crop-specific management."

        )


    if nutrient_status["n"]["status"] == "Low":

        recommendations.append(

            "Nitrogen appears low relative "
            "to the dataset range."

        )


    if nutrient_status["p"]["status"] == "Low":

        recommendations.append(

            "Phosphorus appears low relative "
            "to the dataset range."

        )


    if nutrient_status["k"]["status"] == "Low":

        recommendations.append(

            "Potassium appears low relative "
            "to the dataset range."

        )


    if nutrient_status["oc"]["status"] == "Low":

        recommendations.append(

            "Organic carbon is low relative "
            "to the dataset range."

        )


    if not recommendations:

        recommendations.append(

            "Maintain regular soil monitoring "
            "and balanced nutrient management."

        )


    # ========================================================
    # RESULT
    # ========================================================

    return {

        "success":
            True,

        "soil_score":
            soil_score,

        "soil_condition":
            soil_condition,

        "ph":
            round(
                ph,
                2
            ),

        "ph_status":
            ph_status,

        "nutrients":
            nutrient_status,

        "limiting_factors":
            limiting_factors,

        "recommendations":
            recommendations,

        "sample_count":
            int(
                len(soil_data)
            ),

        "model_status":
            "Real soil dataset analysis",

        "features_used":
            SOIL_FEATURES

    }


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================

def predict_soil_fertility(values):

    return analyze_soil(
        values
    )


# ============================================================
# DATASET INFORMATION
# ============================================================

def get_soil_dataset_info():

    return {

        "dataset":
            DATA_PATH,

        "samples":
            int(
                len(soil_data)
            ),

        "features":
            SOIL_FEATURES,

        "statistics":
            SOIL_LIMITS

    }


print("✓ REAL SOIL ANALYSIS READY")
print("==============================================")