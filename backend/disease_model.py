import os
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "plant_disease_model.keras"
)


# ============================================================
# CHECK MODEL FILE
# ============================================================

if not os.path.isfile(MODEL_PATH):
    raise FileNotFoundError(
        "\n\nPlant disease model not found!\n"
        "Expected location:\n"
        f"{MODEL_PATH}\n\n"
        "Put plant_disease_model.keras inside:\n"
        "AgriMind AI/backend/models/\n"
    )


# ============================================================
# LOAD MODEL
# ============================================================

print("\n==============================================")
print("       LOADING PLANT DISEASE MODEL")
print("==============================================")

try:
    model = load_model(
        MODEL_PATH,
        compile=False
    )

    print("✓ Disease model loaded successfully.")
    print("Model input shape:", model.input_shape)
    print("Model output shape:", model.output_shape)

except Exception as error:
    print("❌ MODEL LOAD ERROR:")
    print(error)
    raise


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
# CHECK MODEL CLASS COUNT
# ============================================================

try:

    MODEL_CLASSES = int(
        model.output_shape[-1]
    )

except Exception:

    MODEL_CLASSES = None


print("Model classes:", MODEL_CLASSES)
print("Class names:", len(CLASS_NAMES))


if MODEL_CLASSES is not None:

    if MODEL_CLASSES != len(CLASS_NAMES):

        raise ValueError(
            "\n\nMODEL / CLASS COUNT MISMATCH!\n"
            f"Model predicts {MODEL_CLASSES} classes.\n"
            f"CLASS_NAMES contains {len(CLASS_NAMES)} classes.\n"
        )


print("✓ Model and class names match.")


# ============================================================
# IMAGE SIZE
# ============================================================

# PlantVillage model normally uses 224 x 224.
IMAGE_SIZE = (128, 128)


# ============================================================
# CLEAN CLASS NAME
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
# PREDICT DISEASE
# ============================================================

def predict_disease(image_path):

    print("\n==============================================")
    print("        DISEASE MODEL PREDICTION")
    print("==============================================")

    print("Image path:")
    print(image_path)


    # ========================================================
    # CHECK IMAGE PATH
    # ========================================================

    if not image_path:

        raise ValueError(
            "Image path is empty."
        )


    if not os.path.isfile(image_path):

        raise FileNotFoundError(
            f"Image not found:\n{image_path}"
        )


    # ========================================================
    # OPEN IMAGE
    # ========================================================

    try:

        image = Image.open(
            image_path
        )

        image = image.convert(
            "RGB"
        )

        print(
            "Original image size:",
            image.size
        )

    except Exception as error:

        raise ValueError(
            f"Unable to open uploaded image: {error}"
        )


    # ========================================================
    # RESIZE IMAGE
    # ========================================================

    image = image.resize(
        IMAGE_SIZE,
        Image.Resampling.LANCZOS
    )

    print(
        "Resized image:",
        image.size
    )


    # ========================================================
    # NUMPY ARRAY
    # ========================================================

    image_array = np.asarray(
        image,
        dtype=np.float32
    )


    # ========================================================
    # NORMALIZATION
    # ========================================================

    image_array = (
        image_array / 255.0
    )


    # ========================================================
    # BATCH DIMENSION
    # ========================================================

    image_array = np.expand_dims(
        image_array,
        axis=0
    )


    print(
        "Final image shape:",
        image_array.shape
    )

    print(
        "Model expected input:",
        model.input_shape
    )


    # ========================================================
    # MODEL PREDICTION
    # ========================================================

    try:

        predictions = model.predict(
            image_array,
            verbose=0
        )

    except Exception as error:

        raise RuntimeError(
            f"Model prediction failed: {error}"
        )


    # ========================================================
    # CHECK PREDICTION
    # ========================================================

    if predictions is None:

        raise RuntimeError(
            "Model returned no prediction."
        )


    predictions = np.asarray(
        predictions
    )


    print(
        "Prediction shape:",
        predictions.shape
    )


    # ========================================================
    # HANDLE OUTPUT
    # ========================================================

    if predictions.ndim == 2:

        probabilities = predictions[0]

    elif predictions.ndim == 1:

        probabilities = predictions

    else:

        raise RuntimeError(
            "Unexpected model output shape: "
            f"{predictions.shape}"
        )


    # ========================================================
    # CHECK OUTPUT COUNT
    # ========================================================

    if len(probabilities) != len(CLASS_NAMES):

        raise RuntimeError(
            "Prediction output does not match "
            "the 38 disease classes."
        )


    # ========================================================
    # HANDLE MODELS THAT RETURN LOGITS
    # ========================================================

    total_probability = float(
        np.sum(probabilities)
    )


    if (
        np.any(probabilities < 0)
        or
        np.any(probabilities > 1)
        or
        abs(total_probability - 1.0) > 0.05
    ):

        # Convert logits to probabilities.
        exp_values = np.exp(
            probabilities
            -
            np.max(probabilities)
        )

        probabilities = (
            exp_values
            /
            np.sum(exp_values)
        )


    # ========================================================
    # PREDICTED INDEX
    # ========================================================

    predicted_index = int(
        np.argmax(
            probabilities
        )
    )


    # ========================================================
    # CONFIDENCE
    # ========================================================

    confidence = float(
        probabilities[
            predicted_index
        ]
    )


    # ========================================================
    # DISEASE NAME
    # ========================================================

    disease = CLASS_NAMES[
        predicted_index
    ]


    disease_display = clean_disease_name(
        disease
    )


    # ========================================================
    # TOP 3
    # ========================================================

    top_indices = np.argsort(
        probabilities
    )[::-1][:3]


    top_predictions = []


    for index in top_indices:

        index = int(index)

        prediction_name = clean_disease_name(
            CLASS_NAMES[index]
        )

        prediction_confidence = float(
            probabilities[index]
        ) * 100.0


        top_predictions.append({

            "disease":
                prediction_name,

            "confidence":
                round(
                    prediction_confidence,
                    2
                )

        })


    # ========================================================
    # RESULT
    # ========================================================

    result = {

        "disease":
            disease_display,

        "confidence":
            round(
                confidence * 100.0,
                2
            ),

        "class_index":
            predicted_index,

        "top_predictions":
            top_predictions

    }


    # ========================================================
    # PRINT RESULT
    # ========================================================

    print("\nPredicted disease:")
    print(
        disease_display
    )

    print(
        "Confidence:",
        round(
            confidence * 100,
            2
        ),
        "%"
    )

    print(
        "Class index:",
        predicted_index
    )

    print(
        "Top predictions:"
    )

    for prediction in top_predictions:

        print(
            " -",
            prediction["disease"],
            ":",
            prediction["confidence"],
            "%"
        )


    print(
        "=============================================="
    )


    return result