# ============================================================
# AGRIMIND AI - LIGHTWEIGHT DISEASE DETECTION
# NO TENSORFLOW
# RENDER SAFE VERSION
# ============================================================

import os
from PIL import Image, ImageStat


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# ============================================================
# IMAGE SETTINGS
# ============================================================

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


# ============================================================
# DISEASE DATABASE
# ============================================================

DISEASE_DATABASE = {

    "healthy": {
        "severity": "Low",
        "description":
            "The submitted crop image does not show strong "
            "visual symptoms of a plant disease.",
        "action":
            "Continue regular crop monitoring and maintain "
            "proper irrigation and field hygiene."
    },

    "leaf_spot": {
        "severity": "Medium",
        "description":
            "The image shows visual patterns that may be "
            "consistent with leaf spot symptoms.",
        "action":
            "Inspect affected leaves carefully and remove "
            "severely affected plant material when appropriate."
    },

    "yellowing": {
        "severity": "Medium",
        "description":
            "Yellowing patterns were observed in the submitted "
            "crop image.",
        "action":
            "Check irrigation, nutrient availability and the "
            "underside of leaves for possible pest activity."
    },

    "possible_blight": {
        "severity": "High",
        "description":
            "The image contains dark or irregular leaf regions "
            "that may be associated with a possible blight-like "
            "symptom.",
        "action":
            "Inspect nearby plants and consult crop-specific "
            "disease management guidance."
    }
}


# ============================================================
# IMAGE VALIDATION
# ============================================================

def validate_image(image_path):

    if not image_path:
        raise ValueError(
            "No image path provided."
        )

    if not os.path.isfile(image_path):
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    extension = os.path.splitext(
        image_path
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only JPG, JPEG, PNG and WEBP images are supported."
        )

    try:

        with Image.open(image_path) as image:
            image.verify()

    except Exception as error:

        raise ValueError(
            f"Invalid image: {error}"
        )


# ============================================================
# IMAGE ANALYSIS
# ============================================================

def analyze_image(image_path):

    validate_image(image_path)

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

    except Exception as error:

        raise ValueError(
            f"Unable to open image: {error}"
        )

    # Keep processing lightweight
    image.thumbnail(
        (256, 256)
    )

    statistics = ImageStat.Stat(
        image
    )

    red = statistics.mean[0]
    green = statistics.mean[1]
    blue = statistics.mean[2]

    brightness = (
        red +
        green +
        blue
    ) / 3

    return {
        "red": red,
        "green": green,
        "blue": blue,
        "brightness": brightness
    }


# ============================================================
# LIGHTWEIGHT DISEASE ANALYSIS
# ============================================================

def detect_visual_condition(image_path):

    values = analyze_image(
        image_path
    )

    red = values["red"]
    green = values["green"]
    blue = values["blue"]
    brightness = values["brightness"]


    # --------------------------------------------------------
    # Very dark image
    # --------------------------------------------------------

    if brightness < 45:

        return "possible_blight", 55.0


    # --------------------------------------------------------
    # Strong reddish / brownish appearance
    # --------------------------------------------------------

    if (
        red > green * 1.25
        and
        red > blue * 1.20
    ):

        return "possible_blight", 62.0


    # --------------------------------------------------------
    # Yellowing appearance
    # --------------------------------------------------------

    if (
        red > blue * 1.35
        and
        green > blue * 1.20
        and
        red > 80
    ):

        return "yellowing", 60.0


    # --------------------------------------------------------
    # Green dominant image
    # --------------------------------------------------------

    if (
        green > red * 1.05
        and
        green > blue * 1.10
    ):

        return "healthy", 70.0


    # --------------------------------------------------------
    # Otherwise possible leaf spot
    # --------------------------------------------------------

    return "leaf_spot", 55.0


# ============================================================
# CLEAN DISEASE NAME
# ============================================================

def clean_disease_name(name):

    names = {

        "healthy":
            "Healthy",

        "leaf_spot":
            "Possible Leaf Spot",

        "yellowing":
            "Possible Leaf Yellowing",

        "possible_blight":
            "Possible Blight"

    }

    return names.get(
        name,
        "Possible Plant Disease"
    )


# ============================================================
# PREDICT DISEASE
# ============================================================

def predict_disease(image_path):

    print("==============================================")
    print("Lightweight disease prediction requested")
    print("Image:", image_path)
    print("==============================================")


    try:

        condition, confidence = (
            detect_visual_condition(
                image_path
            )
        )

        information = DISEASE_DATABASE[
            condition
        ]

        disease_name = clean_disease_name(
            condition
        )


        result = {

            "disease":
                disease_name,

            "confidence":
                round(
                    confidence,
                    2
                ),

            "severity":
                information["severity"],

            "description":
                information["description"],

            "recommended_action":
                information["action"],

            "class_index":
                0,

            "top_predictions": [

                {
                    "disease":
                        disease_name,

                    "confidence":
                        round(
                            confidence,
                            2
                        )
                }

            ],

            "model_status":
                "Lightweight Render-compatible disease analysis"

        }


        print(
            "Disease:",
            disease_name
        )

        print(
            "Confidence:",
            confidence
        )

        return result


    except Exception as error:

        print(
            "❌ Disease detection error:",
            error
        )

        raise RuntimeError(
            f"Disease prediction failed: {error}"
        )


# ============================================================
# ALIAS
# ============================================================

def detect_disease(image_path):

    return predict_disease(
        image_path
    )