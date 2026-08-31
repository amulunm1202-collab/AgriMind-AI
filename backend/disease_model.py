# ============================================================
# AGRIMIND AI - PLANT DISEASE DETECTION
# LAZY LOADING VERSION FOR RENDER
# ============================================================

import os

# Reduce TensorFlow startup logging
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("TF_NUM_INTRAOP_THREADS", "1")
os.environ.setdefault("TF_NUM_INTEROP_THREADS", "1")

import numpy as np
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

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "plant_disease_model.keras"
)


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
# IMAGE SIZE
# ============================================================

IMAGE_SIZE = (128, 128)


# ============================================================
# GLOBAL MODEL
# IMPORTANT: DO NOT LOAD AT STARTUP
# ============================================================

model = None


# ============================================================
# LOAD MODEL ONLY WHEN NEEDED
# ============================================================

def get_model():

    global model

    if model is not None:
        return model

    if not os.path.isfile(MODEL_PATH):

        raise FileNotFoundError(
            "\nPlant disease model not found.\n"
            f"Expected location:\n{MODEL_PATH}\n"
        )

    print("==============================================")
    print("Loading plant disease model...")
    print("==============================================")

    try:

        from tensorflow.keras.models import load_model

        model = load_model(
            MODEL_PATH,
            compile=False
        )

        print("✓ Disease model loaded.")
        print("Input:", model.input_shape)
        print("Output:", model.output_shape)

    except Exception as error:

        print("❌ Disease model load error:")
        print(error)

        raise

    return model


# ============================================================
# CLEAN DISEASE NAME
# ============================================================

def clean_disease_name(name):

    return str(name).replace(
        "___",
        " - "
    ).replace(
        "_",
        " "
    )


# ============================================================
# DISEASE PREDICTION
# ============================================================

def predict_disease(image_path):

    print("==============================================")
    print("Disease prediction requested")
    print("Image:", image_path)
    print("==============================================")


    # --------------------------------------------------------
    # CHECK IMAGE
    # --------------------------------------------------------

    if not image_path:

        raise ValueError(
            "Image path is empty."
        )


    if not os.path.isfile(image_path):

        raise FileNotFoundError(
            f"Image not found:\n{image_path}"
        )


    # --------------------------------------------------------
    # LOAD MODEL ONLY NOW
    # --------------------------------------------------------

    current_model = get_model()


    # --------------------------------------------------------
    # OPEN IMAGE
    # --------------------------------------------------------

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

    except Exception as error:

        raise ValueError(
            f"Unable to open image: {error}"
        )


    # --------------------------------------------------------
    # RESIZE
    # --------------------------------------------------------

    image = image.resize(
        IMAGE_SIZE,
        Image.Resampling.LANCZOS
    )


    # --------------------------------------------------------
    # ARRAY
    # --------------------------------------------------------

    image_array = np.asarray(
        image,
        dtype=np.float32
    )


    # --------------------------------------------------------
    # NORMALIZE
    # --------------------------------------------------------

    image_array = image_array / 255.0


    # --------------------------------------------------------
    # BATCH
    # --------------------------------------------------------

    image_array = np.expand_dims(
        image_array,
        axis=0
    )


    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    try:

        predictions = current_model.predict(
            image_array,
            verbose=0
        )

    except Exception as error:

        raise RuntimeError(
            f"Disease prediction failed: {error}"
        )


    predictions = np.asarray(
        predictions
    )


    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    if predictions.ndim == 2:

        probabilities = predictions[0]

    elif predictions.ndim == 1:

        probabilities = predictions

    else:

        raise RuntimeError(
            f"Unexpected prediction shape: {predictions.shape}"
        )


    if len(probabilities) != len(CLASS_NAMES):

        raise RuntimeError(
            "Model output does not contain "
            f"{len(CLASS_NAMES)} classes."
        )


    # --------------------------------------------------------
    # HANDLE LOGITS
    # --------------------------------------------------------

    total = float(
        np.sum(probabilities)
    )


    if (
        np.any(probabilities < 0)
        or
        np.any(probabilities > 1)
        or
        abs(total - 1.0) > 0.05
    ):

        exp_values = np.exp(
            probabilities -
            np.max(probabilities)
        )

        probabilities = (
            exp_values /
            np.sum(exp_values)
        )


    # --------------------------------------------------------
    # BEST CLASS
    # --------------------------------------------------------

    predicted_index = int(
        np.argmax(probabilities)
    )


    confidence = float(
        probabilities[predicted_index]
    )


    disease = CLASS_NAMES[
        predicted_index
    ]


    disease_display = clean_disease_name(
        disease
    )


    # --------------------------------------------------------
    # TOP 3
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
    # RESULT
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


    print("Disease:", disease_display)
    print(
        "Confidence:",
        result["confidence"],
        "%"
    )

    return result