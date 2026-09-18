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
        "description":
            "Aphids are small insects that feed on plant sap.",
        "action":
            "Inspect leaves and monitor the affected crop regularly."
    },

    "aphids": {
        "severity": "Medium",
        "description":
            "Aphids are small insects that feed on plant sap.",
        "action":
            "Inspect leaves and monitor the affected crop regularly."
    },

    "whitefly": {
        "severity": "Medium",
        "description":
            "Whiteflies are small insects that feed on plant sap.",
        "action":
            "Inspect the underside of leaves and monitor the crop."
    },

    "whiteflies": {
        "severity": "Medium",
        "description":
            "Whiteflies are small insects that feed on plant sap.",
        "action":
            "Inspect the underside of leaves and monitor the crop."
    },

    "thrips": {
        "severity": "Medium",
        "description":
            "Thrips can damage young leaves and flowers.",
        "action":
            "Inspect young leaves and flowers regularly."
    },

    "caterpillar": {
        "severity": "High",
        "description":
            "Caterpillars can eat leaves and damage crop growth.",
        "action":
            "Inspect leaves for caterpillars and crop damage."
    },

    "beetle": {
        "severity": "Medium",
        "description":
            "Beetles may feed on leaves and cause visible damage.",
        "action":
            "Inspect leaves and monitor the crop regularly."
    },

    "leaf miner": {
        "severity": "Medium",
        "description":
            "Leaf miners create tunnels inside leaves.",
        "action":
            "Remove severely affected leaves and monitor new growth."
    },

    "healthy": {
        "severity": "Low",
        "description":
            "The model classified the submitted image as healthy.",
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

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            f"Pest model not found:\n{MODEL_PATH}"
        )

    print()
    print("==============================================")
    print("Loading YOLO pest model...")
    print("==============================================")

    try:

        from ultralytics import YOLO

        model = YOLO(
            MODEL_PATH
        )

        print("✓ Pest model loaded")

        print(
            "Task:",
            getattr(
                model,
                "task",
                "Unknown"
            )
        )

        print(
            "Classes:",
            model.names
        )

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

    # Special cases
    if "aphid" in name:

        return PEST_DATABASE["aphids"]

    if "whitefly" in name or "white fly" in name:

        return PEST_DATABASE["whiteflies"]

    if "thrip" in name:

        return PEST_DATABASE["thrips"]

    if "caterpillar" in name:

        return PEST_DATABASE["caterpillar"]

    if "beetle" in name:

        return PEST_DATABASE["beetle"]

    if "leaf miner" in name:

        return PEST_DATABASE["leaf miner"]

    return {

        "severity":
            "Medium",

        "description":
            "The model identified an agricultural pest.",

        "action":
            "Inspect the affected crop and monitor it regularly."
    }


# ============================================================
# CLASS NAME HELPER
# ============================================================

def get_class_name(
    names,
    class_id
):

    try:

        if isinstance(
            names,
            dict
        ):

            return str(
                names.get(
                    class_id,
                    f"Class {class_id}"
                )
            )

        if isinstance(
            names,
            list
        ):

            if (
                0 <= class_id < len(names)
            ):

                return str(
                    names[class_id]
                )

    except Exception:
        pass

    return f"Class {class_id}"


# ============================================================
# PREDICT PEST
# ============================================================

def predict_pest(image_path):

    print()
    print("==============================================")
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
    # LOAD MODEL
    # ========================================================

    current_model = get_model()

    print(
        "Running model..."
    )

    # ========================================================
    # RUN MODEL
    # ========================================================

    try:

        results = current_model.predict(

            source=image_path,

            device="cpu",

            imgsz=640,

            conf=0.10,

            augment=False,

            verbose=False,

            max_det=10
        )

    except Exception as error:

        raise RuntimeError(
            f"Pest prediction failed: {error}"
        )

    # ========================================================
    # NO RESULT
    # ========================================================

    if not results:

        return {

            "pest":
                "No confident prediction",

            "confidence":
                0,

            "severity":
                "Unknown",

            "description":
                "The model did not return a usable prediction.",

            "recommended_action":
                "Try uploading a clearer image.",

            "detections":
                [],

            "model_status":
                "YOLO pest detection model"
        }

    result = results[0]

    print()
    print("==============================================")
    print("           MODEL RESULT")
    print("==============================================")

    print(
        "Task:",
        getattr(
            current_model,
            "task",
            "Unknown"
        )
    )

    print(
        "Classes:",
        result.names
    )

    # ========================================================
    # DETECTION MODEL
    # ========================================================

    if (
        result.boxes is not None
        and
        len(result.boxes) > 0
    ):

        detections = []

        for box in result.boxes:

            try:

                class_id = int(
                    box.cls[0].item()
                )

                confidence = float(
                    box.conf[0].item()
                )

                class_name = get_class_name(
                    result.names,
                    class_id
                )

                confidence_percent = round(
                    confidence * 100,
                    2
                )

                print(
                    "Detected:",
                    class_name,
                    "| Confidence:",
                    confidence_percent,
                    "%"
                )

                detections.append({

                    "pest":
                        class_name,

                    "confidence":
                        confidence_percent,

                    "class_id":
                        class_id
                })

            except Exception as error:

                print(
                    "Detection processing error:",
                    error
                )

        # ----------------------------------------------------
        # VALID DETECTION
        # ----------------------------------------------------

        if detections:

            detections.sort(

                key=lambda item:
                    item["confidence"],

                reverse=True
            )

            best = detections[0]

            pest_name = best["pest"]

            confidence = best["confidence"]

            information = get_pest_information(
                pest_name
            )

            print()
            print(
                "✓ FINAL PEST:",
                pest_name
            )

            print(
                "✓ CONFIDENCE:",
                confidence,
                "%"
            )

            return {

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
                    "YOLO object detection model"
            }

    # ========================================================
    # CLASSIFICATION MODEL
    # ========================================================

    if (
        getattr(
            result,
            "probs",
            None
        ) is not None
    ):

        try:

            class_id = int(
                result.probs.top1
            )

            confidence = float(
                result.probs.top1conf.item()
            )

            class_name = get_class_name(
                result.names,
                class_id
            )

            confidence_percent = round(
                confidence * 100,
                2
            )

            print(
                "Classification:",
                class_name,
                "| Confidence:",
                confidence_percent,
                "%"
            )

            # ------------------------------------------------
            # HEALTHY CLASS
            # ------------------------------------------------

            if class_name.lower() in {

                "healthy",
                "normal",
                "no pest",
                "no_pest",
                "healthy leaf"

            }:

                information = get_pest_information(
                    "healthy"
                )

                return {

                    "pest":
                        "Healthy",

                    "confidence":
                        confidence_percent,

                    "severity":
                        "Low",

                    "description":
                        information["description"],

                    "recommended_action":
                        information["action"],

                    "detections":
                        [],

                    "model_status":
                        "YOLO classification model"
                }

            # ------------------------------------------------
            # PEST CLASS
            # ------------------------------------------------

            information = get_pest_information(
                class_name
            )

            return {

                "pest":
                    class_name,

                "confidence":
                    confidence_percent,

                "severity":
                    information["severity"],

                "description":
                    information["description"],

                "recommended_action":
                    information["action"],

                "detections":
                    [
                        {
                            "pest":
                                class_name,

                            "confidence":
                                confidence_percent,

                            "class_id":
                                class_id
                        }
                    ],

                "model_status":
                    "YOLO classification model"
            }

        except Exception as error:

            print(
                "Classification processing error:",
                error
            )

    # ========================================================
    # NO CONFIDENT DETECTION
    # ========================================================

    print()
    print(
        "⚠ No pest was confidently detected."
    )

    return {

        "pest":
            "No pest confidently detected",

        "confidence":
            0,

        "severity":
            "Unknown",

        "description":
            "The model did not confidently identify a pest in this image.",

        "recommended_action":
            "Upload a clearer image with the pest clearly visible.",

        "detections":
            [],

        "model_status":
            "YOLO pest detection model"
    }


# ============================================================
# ALIAS
# ============================================================

def detect_pest(image_path):

    return predict_pest(
        image_path
    )