import os

# Render does not provide a GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


import os
import io
import json
import random
import sqlite3
import urllib.request
import urllib.parse

from datetime import datetime

import requests
import numpy as np
from PIL import Image

from dotenv import load_dotenv
from google import genai
# ============================================================
# GEMINI AI SETUP
# ============================================================

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("✅ Gemini AI configured.")
else:
    print("⚠️ Gemini AI is not configured. Continuing without Gemini.")
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    flash
)

from flask_cors import CORS

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)




# ============================================================
# DISEASE MODEL
# ============================================================

from backend.disease_model import predict_disease

# ============================================================
# AI FARMING ASSISTANT
# ============================================================

from backend.farming_assistant import get_farming_response

# ============================================================
# REAL PEST MODEL
# ============================================================

from backend.pest_model import predict_pest

# ============================================================
# REAL SOIL MODEL
# ============================================================

from backend.soil_model import predict_soil_fertility

from backend.crop_model import recommend_crop

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIR = os.path.join(
    BASE_DIR,
    "frontend",
    "templates"
)

STATIC_DIR = os.path.join(
    BASE_DIR,
    "frontend",
    "static"
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "agrimind.db"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# FLASK
# ============================================================

app = Flask(
    __name__,

    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

app.secret_key = "agrimind-ai-development-key"

CORS(app)


# ============================================================
# DATABASE
# ============================================================

def get_db():

    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_db()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            security_question TEXT,
            security_answer TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS soil_sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nitrogen REAL NOT NULL,
            phosphorus REAL NOT NULL,
            potassium REAL NOT NULL,
            ph REAL NOT NULL,
            moisture REAL NOT NULL,
            received_at TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()

    print("Database initialized.")


# ============================================================
# SECURITY QUESTIONS
# ============================================================

SECURITY_QUESTIONS = [

    "What is your mother's first name?",

    "What is the name of your first school?",

    "What is your favourite teacher's name?",

    "What is your favourite childhood place?",

    "What was the name of your first pet?"

]


# ============================================================
# CAPTCHA
# ============================================================

def create_captcha():

    number1 = random.randint(
        1,
        9
    )

    number2 = random.randint(
        1,
        9
    )

    operation = random.choice([
        "+",
        "-"
    ])

    if operation == "-":

        if number2 > number1:

            number1, number2 = (
                number2,
                number1
            )

        answer = number1 - number2

    else:

        answer = number1 + number2

    question = (
        f"{number1} "
        f"{operation} "
        f"{number2} = ?"
    )

    session["captcha_answer"] = str(
        answer
    )

    return question


def verify_captcha(answer):

    correct = session.get(
        "captcha_answer"
    )

    if correct is None:

        return False

    return (
        str(answer).strip()
        ==
        str(correct).strip()
    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    if session.get("user_id"):

        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("login")
    )


# ============================================================
# REGISTER
# ============================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "GET":

        captcha_question = create_captcha()

        return render_template(
            "register.html",
            security_questions=SECURITY_QUESTIONS,
            captcha_question=captcha_question
        )

    full_name = request.form.get(
        "full_name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    password = request.form.get(
        "password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )

    security_question = request.form.get(
        "security_question",
        ""
    ).strip()

    security_answer = request.form.get(
        "security_answer",
        ""
    ).strip()

    captcha = request.form.get(
        "captcha",
        ""
    ).strip()

    if not full_name:

        flash(
            "Please enter your full name.",
            "error"
        )

        return redirect(
            url_for("register")
        )

    if not email or "@" not in email:

        flash(
            "Please enter a valid email.",
            "error"
        )

        return redirect(
            url_for("register")
        )

    if len(password) < 8:

        flash(
            "Password must contain at least 8 characters.",
            "error"
        )

        return redirect(
            url_for("register")
        )

    if password != confirm_password:

        flash(
            "Passwords do not match.",
            "error"
        )

        return redirect(
            url_for("register")
        )

    if security_question not in SECURITY_QUESTIONS:

        flash(
            "Please select a security question.",
            "error"
        )

        return redirect(
            url_for("register")
        )

    if not security_answer:

        flash(
            "Please enter your security answer.",
            "error"
        )

        return redirect(
            url_for("register")
        )

    if not verify_captcha(captcha):

        flash(
            "Incorrect CAPTCHA.",
            "error"
        )

        return redirect(
            url_for("register")
        )

    connection = get_db()

    existing_user = connection.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    if existing_user:

        connection.close()

        flash(
            "Email is already registered.",
            "error"
        )

        return redirect(
            url_for("login")
        )

    hashed_password = generate_password_hash(
        password
    )

    hashed_answer = generate_password_hash(
        security_answer.lower()
    )

    connection.execute(
        """
        INSERT INTO users
        (
            full_name,
            email,
            password,
            security_question,
            security_answer,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            full_name,
            email,
            hashed_password,
            security_question,
            hashed_answer,
            datetime.now().isoformat()
        )
    )

    connection.commit()

    connection.close()

    session.pop(
        "captcha_answer",
        None
    )

    flash(
        "Account created successfully.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "GET":

        return render_template(
            "login.html"
        )

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    password = request.form.get(
        "password",
        ""
    )

    connection = get_db()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    if not user:

        flash(
            "Account not found.",
            "error"
        )

        return redirect(
            url_for("login")
        )

    if not check_password_hash(
        user["password"],
        password
    ):

        flash(
            "Incorrect password.",
            "error"
        )

        return redirect(
            url_for("login")
        )

    session["user_id"] = user["id"]

    session["user_name"] = (
        user["full_name"]
    )

    session["user_email"] = (
        user["email"]
    )

    return redirect(
        url_for("dashboard")
    )


# ============================================================
# FORGOT PASSWORD
# ============================================================

@app.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "GET":

        captcha_question = create_captcha()

        return render_template(
            "forgot_password.html",
            captcha_question=captcha_question
        )

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    security_answer = request.form.get(
        "security_answer",
        ""
    ).strip()

    captcha = request.form.get(
        "captcha",
        ""
    ).strip()

    if not verify_captcha(captcha):

        flash(
            "Incorrect CAPTCHA.",
            "error"
        )

        return redirect(
            url_for("forgot_password")
        )

    connection = get_db()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    if not user:

        flash(
            "Account not found.",
            "error"
        )

        return redirect(
            url_for("forgot_password")
        )

    if not check_password_hash(
        user["security_answer"],
        security_answer.lower()
    ):

        flash(
            "Incorrect security answer.",
            "error"
        )

        return redirect(
            url_for("forgot_password")
        )

    session["reset_email"] = email

    session["password_reset_verified"] = True

    return redirect(
        url_for("reset_password")
    )


# ============================================================
# RESET PASSWORD
# ============================================================

@app.route(
    "/reset-password",
    methods=["GET", "POST"]
)
def reset_password():

    if not session.get(
        "password_reset_verified"
    ):

        return redirect(
            url_for("forgot_password")
        )

    if request.method == "GET":

        return render_template(
            "reset_password.html"
        )

    email = session.get(
        "reset_email"
    )

    password = request.form.get(
        "password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )

    if len(password) < 8:

        flash(
            "Password must contain at least 8 characters.",
            "error"
        )

        return redirect(
            url_for("reset_password")
        )

    if password != confirm_password:

        flash(
            "Passwords do not match.",
            "error"
        )

        return redirect(
            url_for("reset_password")
        )

    hashed_password = generate_password_hash(
        password
    )

    connection = get_db()

    connection.execute(
        """
        UPDATE users
        SET password = ?
        WHERE email = ?
        """,
        (
            hashed_password,
            email
        )
    )

    connection.commit()

    connection.close()

    session.pop(
        "reset_email",
        None
    )

    session.pop(
        "password_reset_verified",
        None
    )

    flash(
        "Password changed successfully.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if not session.get("user_id"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard.html"
    )

# ============================================================
# SOIL SCAN PAGE
# ============================================================

@app.route("/soil-scan", methods=["GET"])
def soil_scan_page():

    if not session.get("user_id"):
        return redirect(url_for("login"))

    return render_template("soil_scan.html")


# ============================================================
# SOIL IMAGE ANALYSIS
# ============================================================

@app.route("/api/soil-scan-image", methods=["POST"])
def soil_scan_image_api():

    if not session.get("user_id"):

        return jsonify({
            "success": False,
            "error": "Please login first."
        }), 401

    try:

        if "soil_image" not in request.files:

            return jsonify({
                "success": False,
                "error": "Please upload a soil image."
            }), 400


        image_file = request.files["soil_image"]


        if image_file.filename == "":

            return jsonify({
                "success": False,
                "error": "No soil image selected."
            }), 400


        from PIL import Image
        import io
        import numpy as np


        image = Image.open(
            io.BytesIO(
                image_file.read()
            )
        ).convert("RGB")


        image.thumbnail(
            (500, 500)
        )


        image_array = np.array(
            image
        )


        # ====================================================
        # RGB
        # ====================================================

        average_rgb = (
            image_array
            .mean(axis=(0, 1))
        )


        r = float(
            average_rgb[0]
        )

        g = float(
            average_rgb[1]
        )

        b = float(
            average_rgb[2]
        )


        brightness = (
            r + g + b
        ) / 3


        # ====================================================
        # SOIL COLOR
        # ====================================================

        if brightness < 70:

            soil_color = "Very Dark Brown"

        elif brightness < 105:

            soil_color = "Dark Brown"

        elif brightness < 145:

            soil_color = "Brown"

        elif brightness < 185:

            soil_color = "Light Brown"

        else:

            soil_color = "Light / Pale Soil"


        # ====================================================
        # APPARENT MOISTURE
        # ====================================================

        if brightness < 85:

            moisture = "High"

        elif brightness < 135:

            moisture = "Moderate"

        else:

            moisture = "Low"


        # ====================================================
        # TEXTURE
        # ====================================================

        gray = (
            image_array
            .mean(axis=2)
        )


        texture_variation = float(
            gray.std()
        )


        if texture_variation < 25:

            texture = "Fine / Smooth"

        elif texture_variation < 50:

            texture = "Moderately Textured"

        else:

            texture = "Coarse / Rough"


        # ====================================================
        # CONDITION
        # ====================================================

        if moisture == "High":

            condition = "Moist-looking Soil"

        elif moisture == "Moderate":

            condition = "Moderately Moist Soil"

        else:

            condition = "Dry-looking Soil"


        # ====================================================
        # AUTOMATIC ESTIMATED SOIL VALUES
        #
        # IMPORTANT:
        # These are estimates, NOT real measurements.
        # ====================================================

        if brightness < 85:

            nitrogen = 85.0
            phosphorus = 42.0
            potassium = 55.0
            ph = 6.4

        elif brightness < 135:

            nitrogen = 65.0
            phosphorus = 35.0
            potassium = 45.0
            ph = 6.7

        elif brightness < 185:

            nitrogen = 45.0
            phosphorus = 28.0
            potassium = 35.0
            ph = 6.9

        else:

            nitrogen = 30.0
            phosphorus = 20.0
            potassium = 25.0
            ph = 7.1


        # ====================================================
        # SAVE AUTOMATIC SOIL VALUES
        #
        # This fixes your current:
        # "No soil scan found" 404 problem.
        # ====================================================

        connection = get_db()


        connection.execute("""
            INSERT INTO soil_sensor_data
            (
                nitrogen,
                phosphorus,
                potassium,
                ph,
                moisture,
                received_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (

            nitrogen,
            phosphorus,
            potassium,
            ph,

            brightness,

            datetime.now().isoformat()

        ))


        connection.commit()
        connection.close()


        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "success": True,

            "result": {

                "color":
                    soil_color,

                "texture":
                    texture,

                "moisture":
                    moisture,

                "condition":
                    condition,

                "brightness":
                    round(
                        brightness,
                        2
                    ),

                "texture_variation":
                    round(
                        texture_variation,
                        2
                    )

            },

            "soil_values": {

                "nitrogen":
                    nitrogen,

                "phosphorus":
                    phosphorus,

                "potassium":
                    potassium,

                "ph":
                    ph

            },

            "analysis_type":
                "Image-based soil analysis with automatic estimated nutrient values",

            "note":
                "N, P, K and pH are estimated for automatic demonstration. "
                "Actual measurements require a soil sensor or laboratory test."

        }), 200


    except Exception as error:

        print(
            "SOIL IMAGE ERROR:",
            repr(error)
        )


        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500
# ============================================================
# LATEST SOIL DATA API
# ============================================================

@app.route("/api/soil-data", methods=["GET"])
def api_soil_data():

    if not session.get("user_id"):
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    connection = None

    try:

        connection = get_db()

        row = connection.execute("""
            SELECT
                id,
                nitrogen,
                phosphorus,
                potassium,
                ph,
                moisture
            FROM soil_sensor_data
            ORDER BY id DESC
            LIMIT 1
        """).fetchone()

        if row is None:

            return jsonify({
                "success": False,
                "message": "No soil data found. Please analyze soil first."
            }), 404

        return jsonify({

            "success": True,

            "soil": {

                "nitrogen":
                    float(row["nitrogen"]),

                "phosphorus":
                    float(row["phosphorus"]),

                "potassium":
                    float(row["potassium"]),

                "ph":
                    float(row["ph"]),

                "moisture":
                    float(row["moisture"])
                    if row["moisture"] is not None
                    else None
            }
        })

    except Exception as error:

        print(
            "❌ /api/soil-data ERROR:",
            repr(error)
        )

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500

    finally:

        if connection:
            connection.close()
    
# ============================================================
# CROP RECOMMENDATION PAGE
# ============================================================

@app.route("/crop-recommendation-page", methods=["GET"])
def crop_recommendation_page():

    if not session.get("user_id"):
        return redirect(url_for("login"))

    return render_template(
        "crop_recommendation.html"
    )
# ============================================================
# CROP RECOMMENDATION API
# AUTOMATIC SOIL VALUES + WEATHER
# ============================================================

@app.route(
    "/api/crop-recommendation",
    methods=["POST"]
)
def crop_recommendation():

    if not session.get("user_id"):

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401


    try:

        data = (
            request.get_json(
                silent=True
            )
            or {}
        )


        # ====================================================
        # SOIL
        # ====================================================

        nitrogen = float(
            data["nitrogen"]
        )

        phosphorus = float(
            data["phosphorus"]
        )

        potassium = float(
            data["potassium"]
        )

        ph = float(
            data["ph"]
        )


        # ====================================================
        # WEATHER
        # ====================================================

        temperature = float(
            data["temperature"]
        )

        humidity = float(
            data["humidity"]
        )

        rainfall = float(
            data["rainfall"]
        )


        print()
        print(
            "=============================================="
        )

        print(
            "AUTOMATIC CROP RECOMMENDATION"
        )

        print(
            "N:",
            nitrogen
        )

        print(
            "P:",
            phosphorus
        )

        print(
            "K:",
            potassium
        )

        print(
            "pH:",
            ph
        )

        print(
            "Temperature:",
            temperature
        )

        print(
            "Humidity:",
            humidity
        )

        print(
            "Rainfall:",
            rainfall
        )

        print(
            "=============================================="
        )


        # ====================================================
        # REAL RANDOM FOREST MODEL
        # ====================================================

        ml_result = recommend_crop(

            nitrogen,

            phosphorus,

            potassium,

            temperature,

            humidity,

            ph,

            rainfall

        )


        return jsonify({

            "success": True,

            "soil": {

                "nitrogen":
                    nitrogen,

                "phosphorus":
                    phosphorus,

                "potassium":
                    potassium,

                "ph":
                    ph

            },

            "weather": {

                "temperature":
                    temperature,

                "humidity":
                    humidity,

                "rainfall":
                    rainfall

            },

            "result":
                ml_result

        }), 200


    except (
        TypeError,
        ValueError,
        KeyError
    ) as error:

        return jsonify({

            "success": False,

            "message":
                f"Invalid crop input: {error}"

        }), 400


    except Exception as error:

        print(
            "CROP RECOMMENDATION ERROR:",
            repr(error)
        )


        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500
# ============================================================
# AI FARMING ASSISTANT
# ============================================================

def get_farming_response(message):

    message = str(message).strip()

    if not message:

        return (
            "Please enter your farming question."
        )

    try:

        prompt = f"""
You are AgriMind AI, an intelligent farming assistant.

Answer the user's question clearly, naturally and helpfully.

You can help with:

- crops
- crop selection
- soil
- soil nutrients
- irrigation
- water requirements
- fertilizers
- seeds
- plant growth
- plant diseases
- pests
- weather
- farming techniques
- crop nutrition
- harvesting
- agricultural problems

Do NOT restrict yourself to fixed questions.

Answer any reasonable agriculture-related question.

Give practical, simple and easy-to-understand answers.

If the question is not related to agriculture or farming,
politely explain that AgriMind AI is mainly designed to
help with farming and agriculture.

User question:
{message}
"""

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt

        )

        return response.text

    except Exception as error:

        print(
            "GEMINI ERROR:",
            repr(error)
        )

        return (
            "Sorry, I couldn't process your question right now. "
            "Please try again."
        )

# ============================================================
# WEATHER CONDITION
# ============================================================

def weather_condition_from_code(code):

    weather_codes = {

        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Fog",

        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",

        56: "Freezing Drizzle",
        57: "Freezing Drizzle",

        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",

        66: "Freezing Rain",
        67: "Heavy Freezing Rain",

        71: "Slight Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",

        77: "Snow Grains",

        80: "Slight Rain Showers",
        81: "Moderate Rain Showers",
        82: "Heavy Rain Showers",

        85: "Slight Snow Showers",
        86: "Heavy Snow Showers",

        95: "Thunderstorm",
        96: "Thunderstorm with Hail",
        99: "Thunderstorm with Heavy Hail"

    }

    return weather_codes.get(
        code,
        "Unknown"
    )


# ============================================================
# WEATHER ICON
# ============================================================

def weather_icon_from_code(code):

    if code == 0:
        return "☀️"

    if code in [1, 2]:
        return "🌤️"

    if code == 3:
        return "☁️"

    if code in [45, 48]:
        return "🌫️"

    if code in [
        51, 53, 55,
        56, 57
    ]:
        return "🌦️"

    if code in [
        61, 63, 65,
        80, 81, 82
    ]:
        return "🌧️"

    if code in [
        71, 73, 75,
        77, 85, 86
    ]:
        return "❄️"

    if code in [
        95, 96, 99
    ]:
        return "⛈️"

    return "🌤️"


# ============================================================
# FARMING INSIGHT
# ============================================================

def create_farming_insight(
    temperature,
    humidity,
    rainfall,
    wind_speed,
    condition,
    rain_probability
):

    if rain_probability >= 70:

        return (
            "High rain probability is expected. "
            "Avoid unnecessary irrigation and "
            "monitor the field for excess water."
        )

    if rainfall >= 10:

        return (
            "Significant rainfall is occurring. "
            "Avoid additional irrigation and "
            "check the field for waterlogging."
        )

    if temperature >= 35:

        return (
            "High temperature detected. Crops may "
            "experience heat stress. Monitor soil "
            "moisture and provide irrigation when required."
        )

    if temperature <= 15:

        return (
            "Cool conditions are present. Monitor "
            "temperature-sensitive crops and avoid "
            "unnecessary irrigation."
        )

    if humidity >= 85:

        return (
            "Humidity is very high. Monitor crops "
            "carefully for fungal diseases and "
            "maintain good field ventilation."
        )

    if wind_speed >= 30:

        return (
            "Strong winds are present. Avoid spraying "
            "activities and check young plants for "
            "possible wind damage."
        )

    if condition in [
        "Clear Sky",
        "Mainly Clear"
    ]:

        return (
            "Weather conditions are generally favorable. "
            "Continue normal field monitoring and irrigate "
            "according to soil moisture and crop requirements."
        )

    if condition in [
        "Partly Cloudy",
        "Overcast"
    ]:

        return (
            "Cloudy conditions may reduce evaporation. "
            "Check soil moisture before deciding whether "
            "additional irrigation is needed."
        )

    return (
        "Monitor temperature, rainfall, humidity and "
        "soil moisture together before making irrigation "
        "or field-management decisions."
    )


# ============================================================
# IRRIGATION RECOMMENDATION
# ============================================================

def create_irrigation_recommendation(
    temperature,
    humidity,
    rainfall,
    rain_probability
):

    if rain_probability >= 70:

        return (
            "Irrigation is likely not required now. "
            "Rain may provide natural water to the field."
        )

    if rainfall >= 10:

        return (
            "Avoid irrigation for now because recent "
            "rainfall is already significant."
        )

    if humidity >= 80 and temperature < 30:

        return (
            "Irrigation can be delayed. High humidity "
            "and moderate temperature may reduce water loss."
        )

    if temperature >= 35:

        return (
            "Check soil moisture frequently. Irrigation "
            "may be needed during cooler parts of the day "
            "if the soil is dry."
        )

    if temperature >= 30:

        return (
            "Moderate irrigation may be required if the "
            "soil moisture is low. Prefer irrigation "
            "during cooler hours."
        )

    return (
        "Irrigate only when soil moisture is below "
        "the requirement of the crop."
    )


# ============================================================
# WEATHER ALERT
# ============================================================

def create_weather_alert(
    temperature,
    wind_speed,
    rain_probability,
    condition
):

    alerts = []

    if temperature >= 38:

        alerts.append(
            "High temperature alert"
        )

    if wind_speed >= 40:

        alerts.append(
            "Strong wind alert"
        )

    if rain_probability >= 80:

        alerts.append(
            "Heavy rain possibility"
        )

    if condition in [
        "Thunderstorm",
        "Thunderstorm with Hail",
        "Thunderstorm with Heavy Hail"
    ]:

        alerts.append(
            "Thunderstorm alert"
        )

    if not alerts:

        return (
            "No major weather alerts at the moment."
        )

    return " • ".join(alerts)


# ============================================================
# FETCH WEATHER
# ============================================================

def fetch_weather(
    latitude,
    longitude
):

    params = urllib.parse.urlencode({

        "latitude": latitude,

        "longitude": longitude,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "wind_speed_10m,"
            "weather_code"
        ),

        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation_probability,"
            "precipitation,"
            "weather_code"
        ),

        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_sum,"
            "precipitation_probability_max,"
            "weather_code"
        ),

        "forecast_days": 1,

        "timezone": "auto"

    })

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        + params
    )

    request_object = urllib.request.Request(

        url,

        headers={
            "User-Agent": "AgriMind-AI/1.0"
        }

    )

    with urllib.request.urlopen(
        request_object,
        timeout=10
    ) as response:

        return json.loads(
            response.read().decode(
                "utf-8"
            )
        )

# ============================================================
# WEATHER INSIGHTS PAGE
# ============================================================

@app.route("/weather-insights", methods=["GET"])
def weather_insights():

    if not session.get("user_id"):
        return redirect(url_for("login"))

    return render_template("weather.html")
# ============================================================
# WEATHER DATA API
# ============================================================

@app.route(
    "/weather-data",
    methods=["GET"]
)
@app.route(
    "/api/weather-data",
    methods=["GET"]
)

def weather_data():

    if not session.get("user_id"):

        return jsonify({

            "success": False,

            "message":
                "Please login first."

        }), 401

    try:

        latitude = request.args.get(
            "lat",
            type=float
        )

        longitude = request.args.get(
            "lon",
            type=float
        )

        # Default location
        if (
            latitude is None
            or longitude is None
        ):

            latitude = 13.55
            longitude = 75.99

        # Validate latitude
        if not (
            -90 <= latitude <= 90
        ):

            raise ValueError(
                "Invalid latitude."
            )

        # Validate longitude
        if not (
            -180 <= longitude <= 180
        ):

            raise ValueError(
                "Invalid longitude."
            )

        # ====================================================
        # FETCH WEATHER
        # ====================================================

        weather = fetch_weather(
            latitude,
            longitude
        )

        current = weather.get(
            "current",
            {}
        )

        hourly = weather.get(
            "hourly",
            {}
        )

        daily = weather.get(
            "daily",
            {}
        )

        # ====================================================
        # CURRENT VALUES
        # ====================================================

        temperature = float(
            current.get(
                "temperature_2m",
                0
            )
        )

        humidity = float(
            current.get(
                "relative_humidity_2m",
                0
            )
        )

        rainfall = float(
            current.get(
                "precipitation",
                0
            )
        )

        wind_speed = float(
            current.get(
                "wind_speed_10m",
                0
            )
        )

        weather_code = int(
            current.get(
                "weather_code",
                0
            )
        )

        # ====================================================
        # WEATHER DESCRIPTION
        # ====================================================

        condition = weather_condition_from_code(
            weather_code
        )

        weather_icon = weather_icon_from_code(
            weather_code
        )

        # ====================================================
        # RAIN PROBABILITY
        # ====================================================

        rain_probability = 0

        rain_probabilities = hourly.get(
            "precipitation_probability",
            []
        )

        hourly_times = hourly.get(
            "time",
            []
        )

        current_time = current.get(
            "time",
            ""
        )

        try:

            if current_time in hourly_times:

                index = hourly_times.index(
                    current_time
                )

                if index < len(
                    rain_probabilities
                ):

                    rain_probability = int(
                        rain_probabilities[index]
                    )

            elif rain_probabilities:

                rain_probability = int(
                    rain_probabilities[0]
                )

        except Exception:

            rain_probability = 0

        # ====================================================
        # TODAY DATA
        # ====================================================

        today_max = 0
        today_min = 0
        today_rain = 0
        today_rain_probability = 0

        today_code = weather_code

        try:

            today_max = float(
                daily["temperature_2m_max"][0]
            )

            today_min = float(
                daily["temperature_2m_min"][0]
            )

            today_rain = float(
                daily["precipitation_sum"][0]
            )

            today_rain_probability = int(
                daily[
                    "precipitation_probability_max"
                ][0]
            )

            today_code = int(
                daily["weather_code"][0]
            )

        except Exception:

            pass

        # ====================================================
        # TODAY CONDITION
        # ====================================================

        today_condition = (
            weather_condition_from_code(
                today_code
            )
        )

        today_icon = (
            weather_icon_from_code(
                today_code
            )
        )

        # ====================================================
        # FARMING INSIGHT
        # ====================================================

        insight = create_farming_insight(

            temperature,
            humidity,
            rainfall,
            wind_speed,
            condition,
            rain_probability

        )

        # ====================================================
        # IRRIGATION
        # ====================================================

        irrigation = create_irrigation_recommendation(

            temperature,
            humidity,
            rainfall,
            today_rain_probability

        )

        # ====================================================
        # WEATHER ALERT
        # ====================================================

        alert = create_weather_alert(

            temperature,
            wind_speed,
            today_rain_probability,
            condition

        )

        # ====================================================
        # RETURN WEATHER
        # ====================================================

        return jsonify({

            "success": True,

            "temperature": round(
                temperature,
                1
            ),

            "humidity": round(
                humidity,
                1
            ),

            "rainfall": round(
                rainfall,
                1
            ),

            "wind_speed": round(
                wind_speed,
                1
            ),

            "condition": condition,

            "weather_icon": weather_icon,

            "rain_probability":
                rain_probability,

            "today": {

                "max_temperature":
                    round(
                        today_max,
                        1
                    ),

                "min_temperature":
                    round(
                        today_min,
                        1
                    ),

                "rainfall":
                    round(
                        today_rain,
                        1
                    ),

                "rain_probability":
                    today_rain_probability,

                "condition":
                    today_condition,

                "icon":
                    today_icon

            },

            "insight":
                insight,

            "irrigation":
                irrigation,

            "alert":
                alert,

            "latitude":
                latitude,

            "longitude":
                longitude,

            "source":
                "Open-Meteo"

        })

    except Exception as error:

        print(
            "WEATHER ERROR:",
            repr(error)
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to fetch current weather. "
                "Please check your internet connection."

        }), 500




# ============================================================
# AI FARMING ASSISTANT PAGE
# ============================================================

@app.route("/farming-assistant")
def farming_assistant():

    if not session.get("user_id"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "farming_assistant.html"
    )



# ============================================================
# AI FARMING ASSISTANT API
# ============================================================

@app.route(
    "/api/farming-assistant",
    methods=["POST"]
)
def farming_assistant_api():

    if not session.get("user_id"):

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    try:

        data = request.get_json(
            silent=True
        ) or {}

        question = str(
            data.get("message", "")
        ).strip()

        if not question:

            return jsonify({
                "success": False,
                "message": "Please enter your question."
            }), 400

        # Send question to AI
        response = get_farming_response(
            question
     #============================================================  
    )

        return jsonify({

            "success": True,

            "response": str(
                response
            )

        }), 200

    except Exception as error:

        print(
            "FARMING ASSISTANT ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to process your question."

        }), 500

# ============================================================
# PLANT DISEASE DETECTION PAGE
# ============================================================

@app.route("/disease-detection")
def disease_detection():

    if not session.get("user_id"):
        return redirect(url_for("login"))

    return render_template("disease_detection.html")

# ============================================================
# PLANT DISEASE DETECTION API
# ============================================================

@app.route("/predict-disease", methods=["POST"])
def predict_disease_api():

    if not session.get("user_id"):
        return jsonify({
            "success": False,
            "error": "Please login first."
        }), 401

    try:

        if "image" not in request.files:
            return jsonify({
                "success": False,
                "error": "No image uploaded."
            }), 400

        image = request.files["image"]

        if image.filename == "":
            return jsonify({
                "success": False,
                "error": "Please select an image."
            }), 400

        upload_folder = os.path.join(
            BASE_DIR,
            "uploads"
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        filename = image.filename

        image_path = os.path.join(
            upload_folder,
            filename
        )

        image.save(image_path)

        result = predict_disease(
            image_path
        )

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as error:

        print("DISEASE DETECTION ERROR:")
        print(error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500
# ============================================================
# PEST DETECTION PAGE
# ============================================================

@app.route("/pest-detection", methods=["GET"])
def pest_detection_page():

    if not session.get("user_id"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "pest.html"
    )


# ============================================================
# REAL PEST DETECTION API
# ============================================================

@app.route("/predict-pest", methods=["POST"])
def predict_pest_api():

    print("\n==============================================")
    print("           REAL PEST API REQUEST")
    print("==============================================")


    # ========================================================
    # LOGIN CHECK
    # ========================================================

    if not session.get("user_id"):

        print("❌ User is not logged in.")

        return jsonify({

            "success": False,

            "error":
                "Please login before using Pest Detection."

        }), 401


    # ========================================================
    # CHECK IMAGE
    # ========================================================

    if "image" not in request.files:

        print("❌ No image field received.")

        return jsonify({

            "success": False,

            "error":
                "No image was uploaded."

        }), 400


    file = request.files["image"]


    if not file or file.filename == "":

        print("❌ Empty image.")

        return jsonify({

            "success": False,

            "error":
                "Please select an image."

        }), 400


    print(
        "Received image:",
        file.filename
    )


    # ========================================================
    # CREATE UPLOAD DIRECTORY
    # ========================================================

    upload_folder = os.path.join(

        os.path.dirname(
            os.path.abspath(__file__)
        ),

        "uploads",

        "pests"

    )


    os.makedirs(

        upload_folder,

        exist_ok=True

    )


    # ========================================================
    # SAFE FILENAME
    # ========================================================

    from werkzeug.utils import secure_filename


    original_filename = secure_filename(
        file.filename
    )


    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )


    filename = (
        timestamp
        + "_"
        + original_filename
    )


    image_path = os.path.join(

        upload_folder,

        filename

    )


    print(
        "Saving image:",
        image_path
    )


    # ========================================================
    # SAVE IMAGE
    # ========================================================

    try:

        file.save(
            image_path
        )

        print(
            "✓ Image saved successfully."
        )

    except Exception as error:

        print(
            "❌ IMAGE SAVE ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                f"Unable to save image: {error}"

        }), 500


    # ========================================================
    # CHECK FILE EXISTS
    # ========================================================

    if not os.path.isfile(image_path):

        return jsonify({

            "success": False,

            "error":
                "Uploaded image could not be found."

        }), 500


    # ========================================================
    # RUN REAL YOLO PEST MODEL
    # ========================================================

    try:

        print(
            "\nRunning REAL YOLO pest model..."
        )


        prediction = predict_pest(
            image_path
        )


        print(
            "\n✓ REAL PEST PREDICTION:"
        )

        print(
            prediction
        )


    except Exception as error:

        print(
            "\n❌ PEST MODEL ERROR:"
        )

        print(
            repr(error)
        )


        return jsonify({

            "success": False,

            "error":
                f"Pest model prediction failed: {error}"

        }), 500


    # ========================================================
    # RETURN REAL RESULT
    # ========================================================

    return jsonify({

        "success":
            True,

        "result":
            prediction

    }), 200
# =========================================================
# SMART IRRIGATION - LIVE WEATHER ASSESSMENT
# =========================================================

@app.route("/assess-irrigation", methods=["POST"])
def assess_irrigation():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400

        crop = str(data.get("crop", "")).strip()

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # -------------------------------------------------
        # VALIDATE CROP
        # -------------------------------------------------

        if not crop:
            return jsonify({
                "success": False,
                "error": "Please enter or select a crop."
            }), 400

        # -------------------------------------------------
        # VALIDATE LOCATION
        # -------------------------------------------------

        if latitude is None or longitude is None:
            return jsonify({
                "success": False,
                "error": "Location is required for live weather analysis."
            }), 400

        try:

            latitude = float(latitude)
            longitude = float(longitude)

        except (TypeError, ValueError):

            return jsonify({
                "success": False,
                "error": "Invalid location coordinates."
            }), 400

        # -------------------------------------------------
        # CHECK COORDINATE RANGE
        # -------------------------------------------------

        if not (-90 <= latitude <= 90):

            return jsonify({
                "success": False,
                "error": "Invalid latitude."
            }), 400

        if not (-180 <= longitude <= 180):

            return jsonify({
                "success": False,
                "error": "Invalid longitude."
            }), 400

        # =================================================
        # LIVE WEATHER FROM OPEN-METEO
        # =================================================

        weather_url = "https://api.open-meteo.com/v1/forecast"

        params = {

            "latitude": latitude,

            "longitude": longitude,

            "current": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "rain"
            ]),

            "hourly": ",".join([
                "precipitation_probability",
                "precipitation",
                "rain",
                "et0_fao_evapotranspiration",
                "soil_moisture_0_to_1cm"
            ]),

            "forecast_days": 2,

            "timezone": "auto"

        }

        response = requests.get(

            weather_url,

            params=params,

            timeout=15

        )

        response.raise_for_status()

        weather = response.json()

        # =================================================
        # CURRENT WEATHER
        # =================================================

        current = weather.get(
            "current",
            {}
        )

        temperature = current.get(
            "temperature_2m"
        )

        humidity = current.get(
            "relative_humidity_2m"
        )

        current_precipitation = current.get(
            "precipitation",
            0
        )

        current_rain = current.get(
            "rain",
            0
        )

        # =================================================
        # HOURLY WEATHER
        # =================================================

        hourly = weather.get(
            "hourly",
            {}
        )

        precipitation_probability = hourly.get(
            "precipitation_probability",
            []
        )

        precipitation = hourly.get(
            "precipitation",
            []
        )

        rain_values = hourly.get(
            "rain",
            []
        )

        evapotranspiration_values = hourly.get(
            "et0_fao_evapotranspiration",
            []
        )

        soil_moisture_values = hourly.get(
            "soil_moisture_0_to_1cm",
            []
        )

        # =================================================
        # NEXT 24 HOURS
        # =================================================

        next_24_probability = (
            precipitation_probability[:24]
        )

        next_24_precipitation = (
            precipitation[:24]
        )

        next_24_rain = (
            rain_values[:24]
        )

        next_24_evapotranspiration = (
            evapotranspiration_values[:24]
        )

        # =================================================
        # EXPECTED RAIN
        # =================================================

        expected_rain = round(

            sum(

                value or 0

                for value in next_24_precipitation

            ),

            1

        )

        # =================================================
        # RAIN PROBABILITY
        # =================================================

        if next_24_probability:

            rain_probability = max(

                value or 0

                for value in next_24_probability

            )

        else:

            rain_probability = 0

        # =================================================
        # CURRENT RAIN
        # =================================================

        current_rain = round(

            current_rain or 0,

            1

        )

        current_precipitation = round(

            current_precipitation or 0,

            1

        )

        # =================================================
        # SOIL MOISTURE
        # =================================================

        soil_moisture = None

        valid_moisture = [

            value

            for value in soil_moisture_values[:24]

            if value is not None

        ]

        if valid_moisture:

            soil_moisture = round(

                sum(valid_moisture)

                /

                len(valid_moisture),

                3

            )

        # =================================================
        # EVAPOTRANSPIRATION
        # =================================================

        evapotranspiration = round(

            sum(

                value or 0

                for value in next_24_evapotranspiration

            ),

            2

        )

        # =================================================
        # CROP WATER REQUIREMENT
        # =================================================

        crop_profiles = {

            # High water requirement
            "rice": "high",
            "paddy": "high",
            "sugarcane": "high",
            "banana": "high",

            # Medium water requirement
            "wheat": "medium",
            "maize": "medium",
            "corn": "medium",
            "cotton": "medium",
            "groundnut": "medium",
            "peanut": "medium",
            "soybean": "medium",
            "tomato": "medium",
            "potato": "medium",
            "onion": "medium",
            "chilli": "medium",
            "capsicum": "medium",
            "cabbage": "medium",
            "cauliflower": "medium",
            "barley": "medium",

            # Lower water requirement
            "ragi": "low",
            "millet": "low",
            "sorghum": "low",
            "chickpea": "low",
            "lentil": "low"

        }

        crop_key = crop.lower().strip()

        requirement = crop_profiles.get(
            crop_key,
            "medium"
        )

        # =================================================
        # IRRIGATION DECISION
        # =================================================

        reasons = []

        # -------------------------------------------------
        # RAIN EXPECTED
        # -------------------------------------------------

        if expected_rain >= 10:

            status = (
                "Irrigation May Not Be Needed"
            )

            recommendation = (
                "WAIT FOR RAIN"
            )

            message = (

                f"Live weather data indicates approximately "
                f"{expected_rain} mm of precipitation may occur "
                f"during the next 24 hours. For {crop}, "
                f"irrigation can be postponed while monitoring "
                f"field conditions."

            )

            reasons.append(
                "Rain is expected soon."
            )

            tip = (

                "Monitor rainfall and soil moisture before "
                "adding irrigation."

            )

        # -------------------------------------------------
        # HIGH TEMPERATURE
        # -------------------------------------------------

        elif (

            temperature is not None

            and temperature >= 35

            and expected_rain < 5

        ):

            status = (
                "Irrigation Recommended"
            )

            recommendation = (
                "IRRIGATE SOON"
            )

            message = (

                f"The current temperature is {temperature}°C "
                f"and approximately {expected_rain} mm of rain "
                f"is forecast during the next 24 hours. "
                f"Water demand may be elevated for {crop}."

            )

            reasons.append(
                "High temperature with limited forecast rain."
            )

            tip = (

                "Check soil moisture and crop condition "
                "before irrigation."

            )

        # -------------------------------------------------
        # LOW SOIL MOISTURE
        # -------------------------------------------------

        elif (

            soil_moisture is not None

            and soil_moisture < 0.20

            and expected_rain < 5

        ):

            status = (
                "Low Soil Moisture Detected"
            )

            recommendation = (
                "CHECK IRRIGATION"
            )

            message = (

                f"Forecast rainfall is low and modeled "
                f"near-surface soil moisture is "
                f"{soil_moisture:.2f}. Check the {crop} "
                f"field before irrigation."

            )

            reasons.append(
                "Low modeled near-surface soil moisture."
            )

            tip = (

                "Verify field soil moisture before "
                "applying irrigation."

            )

        # -------------------------------------------------
        # HIGH WATER CROP
        # -------------------------------------------------

        elif (

            requirement == "high"

            and expected_rain < 5

        ):

            status = (
                "Monitor Irrigation Closely"
            )

            recommendation = (
                "IRRIGATION MAY BE NEEDED"
            )

            message = (

                f"{crop.title()} generally has a relatively "
                f"high water requirement. Little rainfall "
                f"is currently forecast during the next "
                f"24 hours."

            )

            reasons.append(
                "Crop has relatively high water demand."
            )

            tip = (

                "Monitor soil moisture and crop condition."

            )

        # -------------------------------------------------
        # NORMAL CONDITIONS
        # -------------------------------------------------

        else:

            status = (
                "Irrigation Can Be Monitored"
            )

            recommendation = (
                "MONITOR FIELD"
            )

            message = (

                f"Current live weather conditions appear "
                f"moderate for {crop.title()}. Continue "
                f"monitoring rainfall and field moisture."

            )

            reasons.append(
                "Current weather conditions are moderate."
            )

            tip = (

                "Continue monitoring rainfall, temperature "
                "and field moisture."

            )

        # =================================================
        # RETURN IRRIGATION RESULT
        # =================================================

        return jsonify({

            "success": True,

            "crop": crop,

            "temperature": temperature,

            "humidity": humidity,

            "current_rain": current_rain,

            "current_precipitation":
                current_precipitation,

            "expected_rain":
                expected_rain,

            "rain_probability":
                rain_probability,

            "soil_moisture":
                soil_moisture,

            "evapotranspiration":
                evapotranspiration,

            "crop_requirement":
                requirement,

            "status":
                status,

            "message":
                message,

            "recommendation":
                recommendation,

            "tip":
                tip,

            "latitude":
                latitude,

            "longitude":
                longitude,

            "weather_source":
                "Open-Meteo",

            "analysis":
                reasons

        })

    # =====================================================
    # WEATHER API ERROR
    # =====================================================

    except requests.exceptions.RequestException as error:

        print(
            "WEATHER API ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                "Live weather service could not be reached. "
                "Please try again."

        }), 503

    # =====================================================
    # GENERAL ERROR
    # =====================================================

    except Exception as error:

        print(
            "IRRIGATION ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# =========================================================
# IRRIGATION ASSESSMENT PAGE
# =========================================================

@app.route("/irrigation-assessment", methods=["GET"])
def irrigation_assessment_page():

    return render_template(
        "irrigation.html"
    )


# ============================================================
# DROUGHT RISK PAGE
# ============================================================

@app.route("/drought-risk", methods=["GET"])
@app.route("/drought-risk-page", methods=["GET"])
def drought_risk_page():
    return render_template("drought.html")


# ============================================================
# DROUGHT RISK API
# LIVE WEATHER + DROUGHT ANALYSIS
# ============================================================

@app.route("/assess-drought", methods=["POST"])
def assess_drought():

    try:

        # ----------------------------------------------------
        # RECEIVE DATA
        # ----------------------------------------------------

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400

        # ----------------------------------------------------
        # CROP
        # ----------------------------------------------------

        crop = str(data.get("crop", "")).strip()

        if not crop:
            return jsonify({
                "success": False,
                "error": "Please enter or select a crop."
            }), 400

        # ----------------------------------------------------
        # LOCATION
        # ----------------------------------------------------

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if latitude is None or longitude is None:
            return jsonify({
                "success": False,
                "error": "Farm location is required."
            }), 400

        try:
            latitude = float(latitude)
            longitude = float(longitude)

        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "error": "Invalid latitude or longitude."
            }), 400

        if not -90 <= latitude <= 90:
            return jsonify({
                "success": False,
                "error": "Invalid latitude."
            }), 400

        if not -180 <= longitude <= 180:
            return jsonify({
                "success": False,
                "error": "Invalid longitude."
            }), 400

        # ====================================================
        # OPEN-METEO
        # ====================================================

        weather_url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,

            "current": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "rain"
            ]),

            "hourly": ",".join([
                "temperature_2m",
                "precipitation",
                "rain",
                "relative_humidity_2m",
                "et0_fao_evapotranspiration",
                "soil_moisture_0_to_1cm"
            ]),

            "past_days": 30,
            "forecast_days": 1,
            "timezone": "auto"
        }

        response = requests.get(
            weather_url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        weather = response.json()

        if "hourly" not in weather:
            return jsonify({
                "success": False,
                "error": "Weather service returned incomplete data."
            }), 503

        # ====================================================
        # CURRENT WEATHER
        # ====================================================

        current = weather.get("current", {})

        temperature = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        current_rain = current.get("rain", 0)
        current_precipitation = current.get("precipitation", 0)

        # ====================================================
        # HOURLY DATA
        # ====================================================

        hourly = weather.get("hourly", {})

        temperatures = hourly.get(
            "temperature_2m", []
        )

        rainfall_values = hourly.get(
            "precipitation", []
        )

        et0_values = hourly.get(
            "et0_fao_evapotranspiration", []
        )

        soil_values = hourly.get(
            "soil_moisture_0_to_1cm", []
        )

        # ====================================================
        # USE LAST 30 DAYS
        # ====================================================

        total_hours = len(rainfall_values)

        if total_hours == 0:
            return jsonify({
                "success": False,
                "error": "No rainfall data available."
            }), 503

        past_hours = min(
            30 * 24,
            total_hours
        )

        recent_rainfall = rainfall_values[:past_hours]

        recent_temperatures = temperatures[:past_hours]

        recent_et0 = et0_values[:past_hours]

        recent_soil = soil_values[:past_hours]

        # ====================================================
        # 7 DAY RAINFALL
        # ====================================================

        last_7_hours = min(
            7 * 24,
            len(recent_rainfall)
        )

        rainfall_7_days = round(
            sum(
                value or 0
                for value in recent_rainfall[
                    past_hours - last_7_hours:
                ]
            ),
            1
        )

        # ====================================================
        # 30 DAY RAINFALL
        # ====================================================

        rainfall_30_days = round(
            sum(
                value or 0
                for value in recent_rainfall
            ),
            1
        )

        # ====================================================
        # TEMPERATURE
        # ====================================================

        valid_temperatures = [
            value
            for value in recent_temperatures
            if value is not None
        ]

        if valid_temperatures:

            average_temperature = round(
                sum(valid_temperatures)
                / len(valid_temperatures),
                1
            )

            maximum_temperature = round(
                max(valid_temperatures),
                1
            )

        else:

            average_temperature = None
            maximum_temperature = None

        # ====================================================
        # SOIL MOISTURE
        # ====================================================

        valid_soil = [
            value
            for value in recent_soil
            if value is not None
        ]

        if valid_soil:

            soil_moisture = round(
                sum(valid_soil)
                / len(valid_soil),
                3
            )

        else:

            soil_moisture = None

        # ====================================================
        # EVAPOTRANSPIRATION
        # ====================================================

        valid_et0 = [
            value
            for value in recent_et0
            if value is not None
        ]

        if valid_et0:

            et0_30_days = round(
                sum(valid_et0),
                1
            )

            average_daily_et0 = round(
                et0_30_days / 30,
                2
            )

        else:

            et0_30_days = None
            average_daily_et0 = None

        # ====================================================
        # CROP WATER REQUIREMENT
        # ====================================================

        high_water_crops = {
            "rice",
            "paddy",
            "sugarcane",
            "banana"
        }

        low_water_crops = {
            "ragi",
            "millet",
            "sorghum",
            "chickpea",
            "lentil"
        }

        crop_key = crop.lower().strip()

        if crop_key in high_water_crops:

            crop_requirement = "High"

        elif crop_key in low_water_crops:

            crop_requirement = "Low"

        else:

            crop_requirement = "Medium"

        # ====================================================
        # DROUGHT SCORE
        # ====================================================

        score = 0

        analysis = []

        # ----------------------------------------------------
        # RAINFALL
        # ----------------------------------------------------

        if rainfall_7_days < 10:

            score += 40

            analysis.append(
                "Very low rainfall was recorded during the "
                "recent 7-day period."
            )

        elif rainfall_7_days < 25:

            score += 30

            analysis.append(
                "Recent 7-day rainfall is relatively low."
            )

        elif rainfall_7_days < 50:

            score += 18

            analysis.append(
                "Recent rainfall is below a moderate level."
            )

        elif rainfall_7_days < 75:

            score += 8

            analysis.append(
                "Recent rainfall is moderate."
            )

        else:

            analysis.append(
                "Recent 7-day rainfall is relatively adequate."
            )

        # ----------------------------------------------------
        # 30 DAY RAINFALL
        # ----------------------------------------------------

        if rainfall_30_days < 50:

            analysis.append(
                "The recent 30-day rainfall total is also low."
            )

        elif rainfall_30_days < 100:

            analysis.append(
                "The recent 30-day rainfall total is moderate."
            )

        else:

            analysis.append(
                "The recent 30-day rainfall total is relatively adequate."
            )

        # ----------------------------------------------------
        # SOIL MOISTURE
        # ----------------------------------------------------

        if soil_moisture is not None:

            if soil_moisture < 0.10:

                score += 30

                analysis.append(
                    "Modeled near-surface soil moisture is very low."
                )

            elif soil_moisture < 0.20:

                score += 24

                analysis.append(
                    "Modeled near-surface soil moisture is low."
                )

            elif soil_moisture < 0.30:

                score += 15

                analysis.append(
                    "Soil moisture is below a moderate level."
                )

            elif soil_moisture < 0.40:

                score += 7

                analysis.append(
                    "Soil moisture is moderately low."
                )

            else:

                analysis.append(
                    "Modeled near-surface soil moisture is relatively adequate."
                )

        else:

            analysis.append(
                "Soil moisture data was unavailable."
            )

        # ----------------------------------------------------
        # TEMPERATURE
        # ----------------------------------------------------

        if maximum_temperature is not None:

            if maximum_temperature >= 40:

                score += 20

                analysis.append(
                    "Very high temperatures may increase crop water stress."
                )

            elif maximum_temperature >= 35:

                score += 15

                analysis.append(
                    "High temperatures may increase crop water demand."
                )

            elif maximum_temperature >= 30:

                score += 8

                analysis.append(
                    "Warm temperatures may increase water demand."
                )

            else:

                analysis.append(
                    "Recent temperatures are not in the highest drought-risk range."
                )

        # ----------------------------------------------------
        # ET0
        # ----------------------------------------------------

        if average_daily_et0 is not None:

            if average_daily_et0 >= 7:

                score += 10

                analysis.append(
                    "Atmospheric evaporative demand is relatively high."
                )

            elif average_daily_et0 >= 5:

                score += 6

                analysis.append(
                    "Atmospheric evaporative demand is moderate-high."
                )

            elif average_daily_et0 >= 3:

                score += 3

                analysis.append(
                    "Atmospheric evaporative demand is moderate."
                )

        # ----------------------------------------------------
        # CROP
        # ----------------------------------------------------

        if crop_requirement == "High":

            analysis.append(
                f"{crop.title()} generally has relatively high water requirements."
            )

        elif crop_requirement == "Low":

            analysis.append(
                f"{crop.title()} generally has relatively lower water requirements."
            )

        else:

            analysis.append(
                f"{crop.title()} generally has moderate water requirements."
            )

        # ====================================================
        # FINAL SCORE
        # ====================================================

        score = min(
            max(
                round(score),
                0
            ),
            100
        )

        # ====================================================
        # RISK LEVEL
        # ====================================================

        if score >= 75:

            risk = "Severe"

            status = "Severe Drought Risk"

            message = (
                f"Live weather and modeled field indicators "
                f"show a severe drought-risk signal for "
                f"{crop.title()}."
            )

        elif score >= 50:

            risk = "High"

            status = "High Drought Risk"

            message = (
                f"Live weather conditions indicate a high "
                f"drought-risk signal for {crop.title()}."
            )

        elif score >= 25:

            risk = "Moderate"

            status = "Moderate Drought Risk"

            message = (
                f"Live weather conditions indicate a moderate "
                f"drought-risk signal for {crop.title()}."
            )

        else:

            risk = "Low"

            status = "Low Drought Risk"

            message = (
                f"Live weather conditions indicate a relatively "
                f"low drought-risk signal for {crop.title()}."
            )

        # ====================================================
        # RESULT
        # ====================================================

        result = {

            "risk": risk,

            "status": status,

            "message": message,

            "score": score,

            "crop": crop,

            "rainfall_7_days": rainfall_7_days,

            "rainfall_30_days": rainfall_30_days,

            "average_temperature": average_temperature,

            "maximum_temperature": maximum_temperature,

            "temperature": temperature,

            "humidity": humidity,

            "current_rain": round(
                current_rain or 0,
                1
            ),

            "current_precipitation": round(
                current_precipitation or 0,
                1
            ),

            "soil_moisture": soil_moisture,

            "et0_30_days": et0_30_days,

            "average_daily_et0": average_daily_et0,

            "crop_requirement": crop_requirement,

            "latitude": latitude,

            "longitude": longitude,

            "weather_source": "Open-Meteo",

            "analysis": analysis
        }

        return jsonify({
            "success": True,
            "result": result
        })

    # ========================================================
    # WEATHER ERROR
    # ========================================================

    except requests.exceptions.RequestException as error:

        print(
            "DROUGHT WEATHER API ERROR:",
            error
        )

        return jsonify({
            "success": False,
            "error":
                "Live weather service could not be reached. "
                "Please check your internet connection."
        }), 503

     # ========================================================
    # GENERAL ERROR
    # ========================================================

    except Exception as error:

        print(
            "DROUGHT RISK ERROR:",
            error
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500   

# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    init_database()

    print()
    print("==================================================")
    print("              🌱 AGRIMIND AI")
    print("==================================================")
    print("Flask server starting...")
    print("Open: http://127.0.0.1:5000")
    print()
    print("Disease Detection: /disease-detection")
    print("Pest Detection: /pest-detection")
    print("Pest API: /predict-pest")
    print("Irrigation: /irrigation-assessment")
    print("Irrigation API: /assess-irrigation")
    print("Drought API: /assess-drought")
    print("==================================================")
    print()

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )
