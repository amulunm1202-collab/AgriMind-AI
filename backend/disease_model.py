import os
import numpy as np
from PIL import Image

# Reduce TensorFlow memory/thread usage
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("TF_NUM_INTRAOP_THREADS", "1")
os.environ.setdefault("TF_NUM_INTEROP_THREADS", "1")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "plant_disease_model.keras"
)

IMAGE_SIZE = (128, 128)

model = None

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


def get_model():

    global model

    if model is not None:
        return model

    if not os.path.isfile(MODEL_PATH):
        raise FileNotFoundError(
            f"Disease model not found at: {MODEL_PATH}"
        )

    print("==============================================")
    print("Loading disease model...")
    print("==============================================")

    try:

        import tensorflow as tf

        # Keep TensorFlow CPU usage small on Render
        try:
            tf.config.threading.set_intra_op_parallelism_threads(1)
            tf.config.threading.set_inter_op_parallelism_threads(1)
        except Exception:
            pass

        from tensorflow.keras.models import load_model

        model = load_model(
            MODEL_PATH,
            compile=False
        )

        print("✓ Disease model loaded")
        print("Input shape:", model.input_shape)
        print("Output shape:", model.output_shape)

        return model

    except Exception as error:

        print("❌ Disease model loading failed")
        print(error)

        raise


def clean_disease_name(name):

    return (
        str(name)
        .replace("___", " - ")
        .replace("_", " ")
    )


def predict_disease(image_path):

    if not image_path:
        raise ValueError("No image path provided.")

    if not os.path.isfile(image_path):
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    # Load TensorFlow model only when disease detection
    # is actually requested.
    current_model = get_model()

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

    except Exception as error:

        raise ValueError(
            f"Unable to open image: {error}"
        )

    image = image.resize(
        IMAGE_SIZE,
        Image.Resampling.LANCZOS
    )

    image_array = np.asarray(
        image,
        dtype=np.float32
    )

    image_array = image_array / 255.0

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    try:

        predictions = current_model.predict(
            image_array,
            verbose=0
        )

    except Exception as error:

        raise RuntimeError(
            f"Disease prediction failed: {error}"
        )

    predictions = np.asarray(predictions)

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
            f"Model has {len(probabilities)} outputs, "
            f"but {len(CLASS_NAMES)} classes are configured."
        )

    # Make sure probabilities are valid
    total = float(np.sum(probabilities))

    if (
        np.any(probabilities < 0)
        or np.any(probabilities > 1)
        or abs(total - 1.0) > 0.05
    ):

        shifted = (
            probabilities -
            np.max(probabilities)
        )

        exp_values = np.exp(shifted)

        probabilities = (
            exp_values /
            np.sum(exp_values)
        )

    predicted_index = int(
        np.argmax(probabilities)
    )

    confidence = float(
        probabilities[predicted_index]
    )

    disease = CLASS_NAMES[
        predicted_index
    ]

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

    return {

        "disease":
            clean_disease_name(disease),

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


def detect_disease(image_path):

    return predict_disease(image_path)