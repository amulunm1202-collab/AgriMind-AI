# ============================================================
# AGRIMIND AI - PLANT DISEASE DETECTION
# TensorFlow Lazy Loading / Render Friendly
# ============================================================

import os

import numpy as np
from PIL import Image


# ============================================================
# TENSORFLOW ENVIRONMENT SETTINGS
# ============================================================

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("TF_NUM_INTRAOP_THREADS", "1")
os.environ.setdefault("TF_NUM_INTEROP_THREADS", "1")


# ============================================================
# PATHS
# ============================================================

# disease_model.py is inside:
# project/
# ├── app.py
# ├── backend/
# │   └── disease_model.py
# └── models/
#     └── plant_disease_model.keras

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "plant_disease_model.keras"
)


# ============================================================
# IMAGE SIZE
# ============================================================

IMAGE_SIZE = (128, 128)


# ============================================================
# MODEL
# ============================================================

model = None


# ============================================================
# PLANTVILLAGE 38 CLASSES
# ============================================================

CLASS_NAMES = [

    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",

    "Blueberry___healthy",

    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",

    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",

    "Orange___Haunglongbing_(Citrus_greening)",

    "Peach___Bacterial_spot",
    "Peach___healthy",

    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",

    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",

    "Raspberry___healthy",
    "Soybean___healthy",

    "Squash___Powdery_mildew",

    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",

    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]


# ============================================================
# CHECK MODEL
# ============================================================

def get_model():

    global model

    # Already loaded
    if model is not None:
        return model

    # Check file
    if not os.path.isfile(MODEL_PATH):

        raise FileNotFoundError(
            "Plant disease model not found.\n"
            f"Expected location:\n{MODEL_PATH}"
        )

    print("==============================================")
    print("Loading PlantVillage disease model...")
    print("==============================================")

    try:

        # TensorFlow is imported ONLY when prediction
        # is actually requested.
        import tensorflow as tf

        # CPU only
        try:

            tf.config.set_visible_devices(
                [],
                "GPU"
            )

        except Exception:
            pass

        # Limit CPU threads
        try:

            tf.config.threading.set_intra_op_parallelism_threads(
                1
            )

            tf.config.threading.set_inter_op_parallelism_threads(
                1
            )

        except Exception:
            pass

        from tensorflow.keras.models import load_model

        model = load_model(
            MODEL_PATH,
            compile=False
        )

        print("✓ Disease model loaded successfully.")
        print(
            "Input shape:",
            model.input_shape
        )

        print(
            "Output shape:",
            model.output_shape
        )

        # Verify output classes
        output_shape = model.output_shape

        if isinstance(output_shape, list):

            output_count = output_shape[0][-1]

        else:

            output_count = output_shape[-1]

        if output_count != len(CLASS_NAMES):

            raise RuntimeError(
                "Disease model output mismatch.\n"
                f"Model outputs: {output_count}\n"
                f"Configured classes: {len(CLASS_NAMES)}"
            )

        return model

    except Exception as error:

        print("❌ Disease model loading failed:")
        print(error)

        raise RuntimeError(
            f"Unable to load disease model: {error}"
        )


# ============================================================
# CLEAN DISEASE NAME
# ============================================================

def clean_disease_name(name):

    return (
        str(name)
        .replace(
            "___",
            " - "
        )
        .replace(
            "_",
            " "
        )
    )


# ============================================================
# PREPARE IMAGE
# ============================================================

def prepare_image(image_path):

    if not image_path:

        raise ValueError(
            "No image path provided."
        )

    if not os.path.isfile(image_path):

        raise FileNotFoundError(
            f"Image not found:\n{image_path}"
        )

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

    except Exception as error:

        raise ValueError(
            f"Unable to open image: {error}"
        )

    # Resize
    image = image.resize(
        IMAGE_SIZE,
        Image.Resampling.LANCZOS
    )

    # Convert to numpy
    image_array = np.asarray(
        image,
        dtype=np.float32
    )

    # Normalize
    image_array /= 255.0

    # Add batch dimension
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    return image_array


# ============================================================
# CONVERT OUTPUT TO PROBABILITIES
# ============================================================

def get_probabilities(predictions):

    predictions = np.asarray(
        predictions,
        dtype=np.float32
    )

    # Expected:
    # (1, 38)
    if predictions.ndim == 2:

        probabilities = predictions[0]

    elif predictions.ndim == 1:

        probabilities = predictions

    else:

        raise RuntimeError(
            "Unexpected model prediction shape: "
            f"{predictions.shape}"
        )

    # Check class count
    if len(probabilities) != len(CLASS_NAMES):

        raise RuntimeError(
            "Model output does not match "
            "PlantVillage classes.\n"
            f"Model output: {len(probabilities)}\n"
            f"Expected: {len(CLASS_NAMES)}"
        )

    # Make a copy
    probabilities = np.asarray(
        probabilities,
        dtype=np.float32
    )

    # --------------------------------------------------------
    # If output is already probabilities
    # --------------------------------------------------------

    total = float(
        np.sum(probabilities)
    )

    valid_probability_output = (

        np.all(probabilities >= 0)

        and

        np.all(probabilities <= 1)

        and

        abs(total - 1.0) < 0.05

    )

    if valid_probability_output:

        return probabilities

    # --------------------------------------------------------
    # Otherwise treat output as logits
    # --------------------------------------------------------

    shifted = (
        probabilities
        -
        np.max(probabilities)
    )

    exp_values = np.exp(
        shifted
    )

    denominator = float(
        np.sum(exp_values)
    )

    if denominator <= 0:

        raise RuntimeError(
            "Unable to calculate prediction probabilities."
        )

    probabilities = (
        exp_values /
        denominator
    )

    return probabilities


# ============================================================
# PREDICT DISEASE
# ============================================================

def predict_disease(image_path):

    print("==============================================")
    print("Disease prediction requested")
    print("Image:", image_path)
    print("==============================================")

    # --------------------------------------------------------
    # Prepare image
    # --------------------------------------------------------

    image_array = prepare_image(
        image_path
    )

    # --------------------------------------------------------
    # Load model only now
    # --------------------------------------------------------

    current_model = get_model()

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    try:

        predictions = current_model.predict(
            image_array,
            verbose=0
        )

    except Exception as error:

        print("❌ Disease prediction error:")
        print(error)

        raise RuntimeError(
            f"Disease prediction failed: {error}"
        )

    # --------------------------------------------------------
    # Probabilities
    # --------------------------------------------------------

    probabilities = get_probabilities(
        predictions
    )

    # --------------------------------------------------------
    # Best class
    # --------------------------------------------------------

    predicted_index = int(
        np.argmax(
            probabilities
        )
    )

    confidence = float(
        probabilities[
            predicted_index
        ]
    )

    disease = CLASS_NAMES[
        predicted_index
    ]

    disease_display = clean_disease_name(
        disease
    )

    # --------------------------------------------------------
    # Top 3 predictions
    # --------------------------------------------------------

    top_indices = np.argsort(
        probabilities
    )[::-1][:3]

    top_predictions = []

    for index in top_indices:

        index = int(index)

        top_predictions.append({

            "disease":
                clean_disease_name(
                    CLASS_NAMES[index]
                ),

            "confidence":
                round(
                    float(
                        probabilities[index]
                    ) * 100,
                    2
                )

        })

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    result = {

        "disease":
            disease_display,

        "confidence":
            round(
                confidence * 100,
                2
            ),

        "class_index":
            predicted_index,

        "top_predictions":
            top_predictions,

        "model_status":
            "Real PlantVillage disease model"

    }

    print(
        "Disease:",
        disease_display
    )

    print(
        "Confidence:",
        result["confidence"],
        "%"
    )

    return result


# ============================================================
# ALIAS
# ============================================================

def detect_disease(image_path):

    return predict_disease(
        image_path
    )