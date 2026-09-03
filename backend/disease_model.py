# ============================================================
# AGRIMIND AI - PLANT DISEASE DETECTION
# ============================================================

import os
import numpy as np
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
    "plant_disease_model.keras"
)

IMAGE_SIZE = (128, 128)


# ============================================================
# MODEL
# ============================================================

model = None


# ============================================================
# PLANTVILLAGE CLASSES
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
# LOAD MODEL
# ============================================================

def get_model():

    global model

    if model is not None:
        return model

    if not os.path.isfile(MODEL_PATH):
        raise FileNotFoundError(
            f"Disease model not found:\n{MODEL_PATH}"
        )

    print("==============================================")
    print("Loading PlantVillage disease model...")
    print("==============================================")

    try:
        # TensorFlow is imported ONLY when prediction is needed.
        import tensorflow as tf

        # CPU only
        try:
            tf.config.set_visible_devices([], "GPU")
        except Exception:
            pass

        # Reduce CPU usage
        try:
            tf.config.threading.set_intra_op_parallelism_threads(1)
            tf.config.threading.set_inter_op_parallelism_threads(1)
        except Exception:
            pass

        # Keras 3 is a standalone package that TensorFlow depends on;
        # import it directly so Pylance can resolve its source (the
        # `tensorflow.keras` lazy-loader module has no resolvable source).
        import keras

        model = keras.models.load_model(
            MODEL_PATH,
            compile=False
        )

        print("✓ Disease model loaded")
        print("Input shape:", model.input_shape)
        print("Output shape:", model.output_shape)

        return model

    except ImportError as error:

        raise RuntimeError(
            "TensorFlow is not installed. "
            "Install TensorFlow in the active environment."
        ) from error

    except Exception as error:

        print("❌ Disease model loading failed:")
        print(error)

        raise RuntimeError(
            f"Unable to load disease model: {error}"
        ) from error


# ============================================================
# CLEAN NAME
# ============================================================

def clean_disease_name(name):

    return (
        str(name)
        .replace("___", " - ")
        .replace("_", " ")
    )


# ============================================================
# VALIDATE IMAGE
# ============================================================

def validate_image(image_path):

    if not image_path:
        raise ValueError(
            "No image path provided."
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
        ) from error


# ============================================================
# PREPARE IMAGE
# ============================================================

def prepare_image(image_path):

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

    except Exception as error:

        raise ValueError(
            f"Unable to open image: {error}"
        ) from error

    image = image.resize(
        IMAGE_SIZE,
        Image.Resampling.LANCZOS
    )

    image_array = np.asarray(
        image,
        dtype=np.float32
    )

    image_array /= 255.0

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    return image_array


# ============================================================
# PREDICTION PROBABILITIES
# ============================================================

def get_probabilities(predictions):

    predictions = np.asarray(
        predictions,
        dtype=np.float32
    )

    if predictions.ndim == 2:
        probabilities = predictions[0]

    elif predictions.ndim == 1:
        probabilities = predictions

    else:
        raise RuntimeError(
            f"Unexpected model output shape: "
            f"{predictions.shape}"
        )

    if len(probabilities) != len(CLASS_NAMES):

        raise RuntimeError(
            f"Model returned {len(probabilities)} classes, "
            f"but {len(CLASS_NAMES)} class names are configured."
        )

    # If already probabilities, use them.
    total = float(
        np.sum(probabilities)
    )

    if (
        np.all(probabilities >= 0)
        and
        np.all(probabilities <= 1)
        and
        abs(total - 1.0) < 0.05
    ):
        return probabilities

    # Otherwise apply softmax.
    shifted = (
        probabilities
        -
        np.max(probabilities)
    )

    exp_values = np.exp(
        shifted
    )

    return (
        exp_values
        /
        np.sum(exp_values)
    )


# ============================================================
# PREDICT DISEASE
# ============================================================

def predict_disease(image_path):

    print("==============================================")
    print("Disease prediction requested")
    print("Image:", image_path)
    print("==============================================")

    # Validate
    validate_image(
        image_path
    )

    # Prepare image
    image_array = prepare_image(
        image_path
    )

    # Load model only now
    current_model = get_model()

    try:

        predictions = current_model.predict(
            image_array,
            verbose=0
        )

    except Exception as error:

        print("❌ Disease prediction failed:")
        print(error)

        raise RuntimeError(
            f"Disease prediction failed: {error}"
        ) from error

    # Convert output to probabilities
    probabilities = get_probabilities(
        predictions
    )

    # Best class
    predicted_index = int(
        np.argmax(probabilities)
    )

    confidence = float(
        probabilities[predicted_index]
    )

    disease = CLASS_NAMES[
        predicted_index
    ]

    # ========================================================
    # TOP 3
    # ========================================================

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

    # ========================================================
    # RESULT
    # ========================================================

    result = {

        "disease":
            clean_disease_name(
                disease
            ),

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
            "PlantVillage disease model"
    }

    print("✓ Disease:", result["disease"])
    print(
        "✓ Confidence:",
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