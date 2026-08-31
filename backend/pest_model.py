# ============================================================
# AGRIMIND AI - REAL YOLO PEST DETECTION MODEL
# ============================================================

import os

from PIL import Image
from ultralytics import YOLO


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "models",
        "pest_model.pt"
    )
)


# ============================================================
# CHECK MODEL
# ============================================================

if not os.path.isfile(MODEL_PATH):

    raise FileNotFoundError(
        "\n==============================================\n"
        "REAL PEST MODEL NOT FOUND\n"
        "==============================================\n"
        f"Expected:\n{MODEL_PATH}\n\n"
        "Put pest_model.pt inside:\n"
        "AgriMind AI/models/\n"
    )


# ============================================================
# LOAD YOLO MODEL
# ============================================================

print("\n==============================================")
print("       LOADING REAL PEST MODEL")
print("==============================================")

try:

    model = YOLO(
        MODEL_PATH
    )

    print("✓ REAL PEST MODEL LOADED")
    print("Model:", MODEL_PATH)
    print("Classes:", model.names)

except Exception as error:

    print("❌ PEST MODEL LOAD ERROR:")
    print(error)

    raise


# ============================================================
# IMAGE VALIDATION
# ============================================================

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


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
# PEST INFORMATION
# ============================================================

PEST_DATABASE = {

    "aphids": {
        "severity": "Medium",
        "description":
            "Small insects that feed on plant sap and "
            "may cause curling or yellowing of leaves.",
        "action":
            "Inspect the underside of leaves and follow "
            "appropriate integrated pest management."
    },

    "whiteflies": {
        "severity": "Medium",
        "description":
            "Small white insects that feed on plant sap "
            "and may cause yellowing and reduced growth.",
        "action":
            "Monitor the underside of leaves and use "
            "appropriate integrated pest management."
    },

    "thrips": {
        "severity": "Medium",
        "description":
            "Small insects that feed on plant tissue and "
            "may cause silvery patches or distortion.",
        "action":
            "Inspect flowers and young leaves and follow "
            "appropriate integrated pest management."
    },

    "caterpillar": {
        "severity": "High",
        "description":
            "Leaf-eating larvae that can damage leaves "
            "and young plant growth.",
        "action":
            "Inspect leaves for larvae and feeding damage "
            "and follow suitable crop-specific management."
    },

    "beetle": {
        "severity": "Medium",
        "description":
            "Beetles can feed on leaves and create holes "
            "or damaged leaf margins.",
        "action":
            "Inspect plants regularly and follow "
            "crop-specific pest management."
    },

    "leaf miner": {
        "severity": "Medium",
        "description":
            "Larvae that create winding tunnels inside "
            "plant leaves.",
        "action":
            "Remove severely affected leaves and monitor "
            "new growth."
    },

    "healthy": {
        "severity": "Low",
        "description":
            "No pest was detected by the trained model "
            "in the submitted image.",
        "action":
            "Continue regular crop monitoring."
    }
}


# ============================================================
# GET PEST INFORMATION
# ============================================================

def get_pest_information(
    pest_name
):

    pest_name_lower = str(
        pest_name
    ).lower()

    # Exact match

    if pest_name_lower in PEST_DATABASE:

        return PEST_DATABASE[
            pest_name_lower
        ]


    # Partial matching

    for name, information in PEST_DATABASE.items():

        if name in pest_name_lower:

            return information


    # Special handling

    if (
        "aphid"
        in pest_name_lower
    ):

        return PEST_DATABASE[
            "aphids"
        ]


    if (
        "thrips"
        in pest_name_lower
    ):

        return PEST_DATABASE[
            "thrips"
        ]


    if (
        "caterpillar"
        in pest_name_lower
    ):

        return PEST_DATABASE[
            "caterpillar"
        ]


    if (
        "beetle"
        in pest_name_lower
    ):

        return PEST_DATABASE[
            "beetle"
        ]


    if (
        "whitefly"
        in pest_name_lower
        or
        "white fly"
        in pest_name_lower
    ):

        return PEST_DATABASE[
            "whiteflies"
        ]


    return {

        "severity": "Medium",

        "description":
            "The trained YOLO model detected "
            "an agricultural pest class.",

        "action":
            "Inspect the affected crop carefully "
            "and follow crop-specific pest management."
    }


# ============================================================
# REAL PEST PREDICTION
# ============================================================

def predict_pest(
    image_path
):

    print("\n==============================================")
    print("          REAL PEST DETECTION")
    print("==============================================")

    print(
        "Image:",
        image_path
    )


    # ========================================================
    # VALIDATE IMAGE
    # ========================================================

    validate_image(
        image_path
    )


    # ========================================================
    # RUN YOLO
    # ========================================================

    try:

        results = model.predict(

            source=image_path,

            conf=0.10,

            verbose=False

        )

    except Exception as error:

        raise RuntimeError(
            f"YOLO prediction failed: {error}"
        )


    # ========================================================
    # CHECK RESULTS
    # ========================================================

    if not results:

        raise RuntimeError(
            "YOLO returned no result."
        )


    result = results[0]


    # ========================================================
    # DEBUG OUTPUT
    # ========================================================

    print("\n==============================================")
    print("        YOLO PEST MODEL DEBUG")
    print("==============================================")

    print(
        "Number of detections:",
        len(result.boxes)
        if result.boxes is not None
        else 0
    )


    # ========================================================
    # NO DETECTION
    # ========================================================

    if (
        result.boxes is None
        or
        len(result.boxes) == 0
    ):

        print(
            "NO PEST DETECTED"
        )

        print(
            "=============================================="
        )

        return {

            "pest":
                "Healthy",

            "confidence":
                0.0,

            "severity":
                "Low",

            "description":
                PEST_DATABASE[
                    "healthy"
                ]["description"],

            "recommended_action":
                PEST_DATABASE[
                    "healthy"
                ]["action"],

            "detections":
                [],

            "model_status":
                "Real YOLO pest detection model"

        }


    # ========================================================
    # PROCESS DETECTIONS
    # ========================================================

    detections = []


    for box in result.boxes:

        class_id = int(
            box.cls[0].item()
        )

        confidence = float(
            box.conf[0].item()
        )


        class_name = result.names.get(

            class_id,

            f"Unknown class {class_id}"

        )


        class_name = str(
            class_name
        )


        confidence_percent = round(

            confidence * 100,

            2

        )


        print(
            f"Class ID: {class_id} | "
            f"Class: {class_name} | "
            f"Confidence: {confidence_percent}%"
        )


        detections.append({

            "pest":
                class_name,

            "confidence":
                confidence_percent,

            "class_id":
                class_id

        })


    # ========================================================
    # SORT BY CONFIDENCE
    # ========================================================

    detections.sort(

        key=lambda item:
            item["confidence"],

        reverse=True

    )


    # ========================================================
    # BEST DETECTION
    # ========================================================

    best_detection = detections[0]


    detected_pest = (
        best_detection["pest"]
    )


    confidence = (
        best_detection["confidence"]
    )


    # ========================================================
    # GET INFORMATION
    # ========================================================

    information = get_pest_information(

        detected_pest

    )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    final_result = {

        "pest":
            detected_pest,

        "confidence":
            confidence,

        "severity":
            information["severity"],

        "description":
            information["description"],

        "recommended_action":
            information["action"],

        "detections":
            detections,

        "model_status":
            "Real YOLO pest detection model"

    }


    # ========================================================
    # TERMINAL OUTPUT
    # ========================================================

    print("\n----------------------------------------------")

    print(
        "BEST PEST:",
        detected_pest
    )

    print(
        "CONFIDENCE:",
        confidence,
        "%"
    )

    print(
        "SEVERITY:",
        information["severity"]
    )

    print(
        "ALL DETECTIONS:",
        detections
    )

    print(
        "==============================================\n"
    )


    return final_result


# ============================================================
# ALIAS
# ============================================================

def detect_pest(
    image_path
):

    return predict_pest(
        image_path
    )