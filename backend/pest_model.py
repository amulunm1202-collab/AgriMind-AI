# ============================================================
# AGRIMIND AI - YOLO PEST DETECTION
# RENDER CPU / LOW MEMORY VERSION
# ============================================================

import os
from PIL import Image

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
# GLOBAL MODEL
# LAZY LOADING
# ============================================================

model = None

# ============================================================
# ALLOWED IMAGE TYPES
# ============================================================

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}

# ============================================================
# PEST DATABASE
# ============================================================

PEST_DATABASE = {

    "aphids": {
        "severity": "Medium",
        "description":
            "Small insects that feed on plant sap and may "
            "cause curling or yellowing of leaves.",
        "action":
            "Inspect the underside of leaves and follow "
            "appropriate integrated pest management."
    },

    "whiteflies": {
        "severity": "Medium",
        "description":
            "Small white insects that feed on plant sap and "
            "may cause yellowing and reduced growth.",
        "action":
            "Monitor the underside of leaves and follow "
            "appropriate integrated pest management."
    },

    "thrips": {
        "severity": "Medium",
        "description":
            "Small insects that feed on plant tissue and may "
            "cause silvery patches or distortion.",
        "action":
            "Inspect flowers and young leaves and follow "
            "appropriate integrated pest management."
    },

    "caterpillar": {
        "severity": "High",
        "description":
            "Leaf-eating larvae that can damage leaves and "
            "young plant growth.",
        "action":
            "Inspect leaves for larvae and follow suitable "
            "crop-specific management."
    },

    "beetle": {
        "severity": "Medium",
        "description":
            "Beetles can feed on leaves and create holes or "
            "damaged leaf margins.",
        "action":
            "Inspect plants regularly and follow "
            "crop-specific pest management."
    },

    "leaf miner": {
        "severity": "Medium",
        "description":
            "Larvae that create winding tunnels inside leaves.",
        "action":
            "Remove severely affected leaves and monitor "
            "new growth."
    },

    "healthy": {
        "severity": "Low",
        "description":
            "No pest was detected by the trained model in "
            "the submitted image.",
        "action":
            "Continue regular crop monitoring."
    }
}

# ============================================================
# LOAD YOLO MODEL
# ============================================================

def get_model():

    global model

    if model is not None:
        return model

    if not os.path.isfile(MODEL_PATH):

        raise FileNotFoundError(
            "Pest model not found.\n"
            f"Expected location:\n{MODEL_PATH}"
        )

    print("==============================================")
    print("Loading YOLO pest model...")
    print("==============================================")

    try:

        from ultralytics import YOLO

        model = YOLO(MODEL_PATH)

        print("✓ YOLO pest model loaded.")
        print("Classes:", model.names)

    except Exception as error:

        print("❌ YOLO model loading failed:")
        print(error)

        raise RuntimeError(
            f"Unable to load pest model: {error}"
        )

    return model


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
# PEST INFORMATION
# ============================================================

def get_pest_information(pest_name):

    name = str(
        pest_name
    ).lower().strip()

    if name in PEST_DATABASE:
        return PEST_DATABASE[name]

    if "aphid" in name:
        return PEST_DATABASE["aphids"]

    if "whitefly" in name or "white fly" in name:
        return PEST_DATABASE["whiteflies"]

    if "thrips" in name:
        return PEST_DATABASE["thrips"]

    if "caterpillar" in name:
        return PEST_DATABASE["caterpillar"]

    if "beetle" in name:
        return PEST_DATABASE["beetle"]

    if "leaf miner" in name:
        return PEST_DATABASE["leaf miner"]

    return {
        "severity": "Medium",
        "description":
            "The trained YOLO model detected an "
            "agricultural pest class.",
        "action":
            "Inspect the affected crop carefully and "
            "follow crop-specific pest management."
    }


# ============================================================
# PREDICT PEST
# ============================================================

def predict_pest(image_path):

    print("==============================================")
    print("YOLO pest prediction requested")
    print("Image:", image_path)
    print("==============================================")

    # Validate image
    validate_image(image_path)

    # Load model only when required
    current_model = get_model()

    try:

        results = current_model.predict(

            source=image_path,

            # CPU
            device="cpu",

            # Lower image size = lower memory
            imgsz=320,

            # Detection threshold
            conf=0.25,

            # Only one image
            batch=1,

            verbose=False

        )

    except Exception as error:

        print("❌ YOLO prediction error:")
        print(error)

        raise RuntimeError(
            f"YOLO prediction failed: {error}"
        )

    # ========================================================
    # CHECK RESULT
    # ========================================================

    if not results:

        return {
            "pest": "Healthy",
            "confidence": 0.0,
            "severity": "Low",
            "description":
                PEST_DATABASE["healthy"]["description"],
            "recommended_action":
                PEST_DATABASE["healthy"]["action"],
            "detections": [],
            "model_status":
                "Real YOLO pest detection model"
        }

    result = results[0]

    # ========================================================
    # NO DETECTION
    # ========================================================

    if (
        result.boxes is None
        or
        len(result.boxes) == 0
    ):

        return {
            "pest": "Healthy",
            "confidence": 0.0,
            "severity": "Low",
            "description":
                PEST_DATABASE["healthy"]["description"],
            "recommended_action":
                PEST_DATABASE["healthy"]["action"],
            "detections": [],
            "model_status":
                "Real YOLO pest detection model"
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
                f"Unknown class {class_id}"
            )

            detections.append({

                "pest": str(
                    class_name
                ),

                "confidence": round(
                    confidence * 100,
                    2
                ),

                "class_id": class_id

            })

        except Exception as error:

            print(
                "Detection processing error:",
                error
            )

    # ========================================================
    # IF NOTHING COULD BE PROCESSED
    # ========================================================

    if not detections:

        return {
            "pest": "Healthy",
            "confidence": 0.0,
            "severity": "Low",
            "description":
                PEST_DATABASE["healthy"]["description"],
            "recommended_action":
                PEST_DATABASE["healthy"]["action"],
            "detections": [],
            "model_status":
                "Real YOLO pest detection model"
        }

    # ========================================================
    # SORT BY CONFIDENCE
    # ========================================================

    detections.sort(
        key=lambda item: item["confidence"],
        reverse=True
    )

    best_detection = detections[0]

    detected_pest = best_detection["pest"]

    confidence = best_detection["confidence"]

    information = get_pest_information(
        detected_pest
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    response = {

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

    print(
        "Detected pest:",
        detected_pest
    )

    print(
        "Confidence:",
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