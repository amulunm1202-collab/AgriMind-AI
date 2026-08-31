# ============================================================
# AGRIMIND AI - YOLO PEST DETECTION
# LAZY LOADING VERSION FOR RENDER
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
# IMPORTANT: DO NOT LOAD DURING APP STARTUP
# ============================================================

model = None


# ============================================================
# ALLOWED IMAGES
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
            "Small insects that feed on plant sap "
            "and may cause curling or yellowing of leaves.",

        "action":
            "Inspect the underside of leaves and "
            "follow appropriate integrated pest management."

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
            "Small insects that feed on plant tissue "
            "and may cause silvery patches or distortion.",

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
            "Larvae that create winding tunnels inside leaves.",

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
# LOAD YOLO ONLY WHEN NEEDED
# ============================================================

def get_model():

    global model

    if model is not None:

        return model


    if not os.path.isfile(MODEL_PATH):

        raise FileNotFoundError(

            "\n==============================================\n"
            "REAL PEST MODEL NOT FOUND\n"
            "==============================================\n"
            f"Expected:\n{MODEL_PATH}\n"

        )


    print("==============================================")
    print("Loading YOLO pest model...")
    print("==============================================")


    try:

        from ultralytics import YOLO

        model = YOLO(
            MODEL_PATH
        )

        print("✓ YOLO pest model loaded.")
        print("Classes:", model.names)

    except Exception as error:

        print("❌ YOLO model load error:")
        print(error)

        raise


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

        with Image.open(
            image_path
        ) as image:

            image.verify()

    except Exception as error:

        raise ValueError(
            f"Invalid image: {error}"
        )


# ============================================================
# PEST INFORMATION
# ============================================================

def get_pest_information(pest_name):

    pest_name_lower = str(
        pest_name
    ).lower()


    if pest_name_lower in PEST_DATABASE:

        return PEST_DATABASE[
            pest_name_lower
        ]


    for name, information in PEST_DATABASE.items():

        if name in pest_name_lower:

            return information


    if "aphid" in pest_name_lower:

        return PEST_DATABASE["aphids"]


    if "thrips" in pest_name_lower:

        return PEST_DATABASE["thrips"]


    if "caterpillar" in pest_name_lower:

        return PEST_DATABASE["caterpillar"]


    if "beetle" in pest_name_lower:

        return PEST_DATABASE["beetle"]


    if (
        "whitefly" in pest_name_lower
        or
        "white fly" in pest_name_lower
    ):

        return PEST_DATABASE["whiteflies"]


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
# PREDICT PEST
# ============================================================

def predict_pest(image_path):

    print("==============================================")
    print("YOLO pest prediction requested")
    print("Image:", image_path)
    print("==============================================")


    # --------------------------------------------------------
    # VALIDATE
    # --------------------------------------------------------

    validate_image(
        image_path
    )


    # --------------------------------------------------------
    # LOAD MODEL ONLY NOW
    # --------------------------------------------------------

    current_model = get_model()


    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    try:

        results = current_model.predict(

            source=image_path,

            conf=0.10,

            verbose=False,

            device="cpu"

        )

    except Exception as error:

        raise RuntimeError(
            f"YOLO prediction failed: {error}"
        )


    if not results:

        raise RuntimeError(
            "YOLO returned no result."
        )


    result = results[0]


    # --------------------------------------------------------
    # NO DETECTION
    # --------------------------------------------------------

    if (
        result.boxes is None
        or
        len(result.boxes) == 0
    ):

        return {

            "pest":
                "Healthy",

            "confidence":
                0.0,

            "severity":
                "Low",

            "description":
                PEST_DATABASE["healthy"][
                    "description"
                ],

            "recommended_action":
                PEST_DATABASE["healthy"][
                    "action"
                ],

            "detections":
                [],

            "model_status":
                "Real YOLO pest detection model"

        }


    # --------------------------------------------------------
    # PROCESS DETECTIONS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    detections.sort(

        key=lambda item:
            item["confidence"],

        reverse=True

    )


    best_detection = detections[0]


    detected_pest = best_detection[
        "pest"
    ]


    confidence = best_detection[
        "confidence"
    ]


    information = get_pest_information(
        detected_pest
    )


    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    return {

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


# ============================================================
# ALIAS
# ============================================================

def detect_pest(image_path):

    return predict_pest(
        image_path
    )