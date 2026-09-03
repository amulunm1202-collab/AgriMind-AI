# ============================================================
# AGRIMIND AI - PEST DETECTION
# ============================================================

import os
from PIL import Image


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "pest_model.pt"
)


# ============================================================
# GLOBAL MODEL
# ============================================================

model = None


# ============================================================
# PEST INFORMATION
# ============================================================

PEST_DATABASE = {

    "aphid": {
        "severity": "Medium",
        "description": "Aphids are small insects that feed on plant sap.",
        "action": "Inspect leaves and monitor the affected crop regularly."
    },

    "aphids": {
        "severity": "Medium",
        "description": "Aphids are small insects that feed on plant sap.",
        "action": "Inspect leaves and monitor the affected crop regularly."
    },

    "whitefly": {
        "severity": "Medium",
        "description": "Whiteflies are small insects that feed on plant sap.",
        "action": "Inspect the underside of leaves and monitor the crop."
    },

    "whiteflies": {
        "severity": "Medium",
        "description": "Whiteflies are small insects that feed on plant sap.",
        "action": "Inspect the underside of leaves and monitor the crop."
    },

    "thrips": {
        "severity": "Medium",
        "description": "Thrips can damage young leaves and flowers.",
        "action": "Inspect young leaves and flowers regularly."
    },

    "caterpillar": {
        "severity": "High",
        "description": "Caterpillars can eat leaves and damage crop growth.",
        "action": "Inspect leaves for caterpillars and crop damage."
    },

    "beetle": {
        "severity": "Medium",
        "description": "Beetles may feed on leaves and cause visible damage.",
        "action": "Inspect leaves and monitor the crop regularly."
    },

    "leaf miner": {
        "severity": "Medium",
        "description": "Leaf miners create tunnels inside leaves.",
        "action": "Remove severely affected leaves and monitor new growth."
    }
}


# ============================================================
# LOAD YOLO MODEL
# ============================================================

def get_model():

    global model

    if model is not None:
        return model

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            f"Pest model not found:\n{MODEL_PATH}"
        )

    print("==============================================")
    print("Loading YOLO pest model...")
    print("==============================================")

    try:

        # Import only when model is actually needed
        from ultralytics import YOLO

        model = YOLO(MODEL_PATH)

        print("✓ Pest model loaded")
        print("Classes:", model.names)

        return model

    except ImportError:

        raise RuntimeError(
            "Ultralytics is not installed. "
            "Run: pip install ultralytics"
        )

    except Exception as error:

        raise RuntimeError(
            f"Unable to load pest model: {error}"
        )


# ============================================================
# VALIDATE IMAGE
# ============================================================

def validate_image(image_path):

    if not image_path:

        raise ValueError(
            "No image was provided."
        )

    if not os.path.isfile(image_path):

        raise FileNotFoundError(
            f"Image not found:\n{image_path}"
        )

    try:

        with Image.open(image_path) as image:

            image.verify()

    except Exception as error:

        raise ValueError(
            f"Invalid image: {error}"
        )


# ============================================================
# GET PEST INFORMATION
# ============================================================

def get_pest_information(pest_name):

    name = str(
        pest_name
    ).lower().strip()

    # Exact match
    if name in PEST_DATABASE:

        return PEST_DATABASE[name]

    # Partial match
    for key in PEST_DATABASE:

        if key in name or name in key:

            return PEST_DATABASE[key]

    # Unknown pest
    return {

        "severity": "Medium",

        "description":
            "The pest detection model identified an agricultural pest.",

        "action":
            "Inspect the affected crop and monitor it regularly."
    }


# ============================================================
# PREDICT PEST
# ============================================================

def predict_pest(image_path):

    print("==============================================")
    print("Pest prediction requested")
    print("Image:", image_path)
    print("==============================================")

    # Validate image
    validate_image(
        image_path
    )

    # Load model
    current_model = get_model()

    try:

        results = current_model.predict(

            source=image_path,

            device="cpu",

            imgsz=640,

            conf=0.10,

            verbose=False
        )

    except Exception as error:

        raise RuntimeError(
            f"Pest prediction failed: {error}"
        )

    # No result
    if not results:

        return {

            "pest": "Healthy",

            "confidence": 0,

            "severity": "Low",

            "description":
                "No pest was detected.",

            "recommended_action":
                "Continue monitoring the crop.",

            "detections": [],

            "model_status":
                "YOLO pest detection model"
        }

    result = results[0]

    # ========================================================
    # NO DETECTIONS
    # ========================================================

    if (
        result.boxes is None
        or
        len(result.boxes) == 0
    ):

        return {

            "pest": "Healthy",

            "confidence": 0,

            "severity": "Low",

            "description":
                "No pest was detected in the submitted image.",

            "recommended_action":
                "Continue monitoring the crop.",

            "detections": [],

            "model_status":
                "YOLO pest detection model"
        }

    # ========================================================
    # PROCESS DETECTIONS
    # ========================================================

    detections = []

    for box in result.boxes:

        try:

            class_id = int(
                box.cls[0].item()
            )

            confidence = float(
                box.conf[0].item()
            )

            class_name = result.names.get(
                class_id,
                f"Class {class_id}"
            )

            detections.append({

                "pest":
                    str(class_name),

                "confidence":
                    round(
                        confidence * 100,
                        2
                    ),

                "class_id":
                    class_id
            })

        except Exception as error:

            print(
                "Detection processing error:",
                error
            )

    # ========================================================
    # NO VALID DETECTIONS
    # ========================================================

    if not detections:

        return {

            "pest": "Healthy",

            "confidence": 0,

            "severity": "Low",

            "description":
                "No pest was detected.",

            "recommended_action":
                "Continue monitoring the crop.",

            "detections": [],

            "model_status":
                "YOLO pest detection model"
        }

    # ========================================================
    # SORT
    # ========================================================

    detections.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    best = detections[0]

    pest_name = best["pest"]

    confidence = best["confidence"]

    # ========================================================
    # INFORMATION
    # ========================================================

    information = get_pest_information(
        pest_name
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    response = {

        "pest":
            pest_name,

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
            "YOLO pest detection model"
    }

    print(
        "✓ Pest:",
        pest_name
    )

    print(
        "✓ Confidence:",
        confidence,
        "%"
    )

    return response


# ============================================================
# ALIAS
# ============================================================

def detect_pest(image_path):

    return predict_pest(
        image_path
    )