import sys
import requests
import random
import time

# Make console output UTF-8 safe (Windows cp1252 cannot encode emoji).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# Flask API address
URL = "http://127.0.0.1:5000/api/sensor-data"


def generate_soil_readings():

    # Simulated soil sensor values
    soil = {
        "nitrogen": round(random.uniform(40, 90), 2),
        "phosphorus": round(random.uniform(20, 60), 2),
        "potassium": round(random.uniform(30, 80), 2),
        "ph": round(random.uniform(5.5, 7.5), 2),
        "moisture": round(random.uniform(40, 80), 2)
    }

    return soil


print()
print("========================================")
print("        AGRIMIND AI SOIL SENSOR")
print("             SIMULATOR")
print("========================================")
print()

print("Checking AgriMind AI server...")


# Check Flask server
try:

    response = requests.get(
        "http://127.0.0.1:5000/",
        timeout=5
    )

    if response.status_code in [200, 302]:

        print("✓ AgriMind AI server connected")

    else:

        print(
            "Server response:",
            response.status_code
        )

except Exception as error:

    print()
    print("❌ Cannot connect to Flask.")
    print()
    print("First start Flask using:")
    print()
    print("python app.py")
    print()
    print("Error:")
    print(error)
    print()

    exit()


print()
print("Starting automatic soil scan...")
print()


# Simulate scanning
for i in range(5):

    print(
        f"Scanning soil sensor... {i + 1}/5"
    )

    time.sleep(1)


# Generate readings
soil = generate_soil_readings()


print()
print("========================================")
print("        SOIL SENSOR READINGS")
print("========================================")
print()

print(
    f"Nitrogen   : {soil['nitrogen']} mg/kg"
)

print(
    f"Phosphorus : {soil['phosphorus']} mg/kg"
)

print(
    f"Potassium  : {soil['potassium']} mg/kg"
)

print(
    f"Soil pH    : {soil['ph']} "
)

print(
    f"Moisture   : {soil['moisture']} %"
)

print()

print("Sending readings to AgriMind AI...")
print()


# Send readings to Flask
try:

    response = requests.post(
        URL,
        json=soil,
        timeout=10
    )

    print(
        "HTTP status:",
        response.status_code
    )

    result = response.json()

    print()

    if result.get("success"):

        print(
            "========================================"
        )

        print(
            "✓ SOIL DATA SENT SUCCESSFULLY"
        )

        print(
            "========================================"
        )

        print()

        print(
            "AgriMind AI received:"
        )

        print(
            "Nitrogen:",
            soil["nitrogen"]
        )

        print(
            "Phosphorus:",
            soil["phosphorus"]
        )

        print(
            "Potassium:",
            soil["potassium"]
        )

        print(
            "pH:",
            soil["ph"]
        )

        print(
            "Moisture:",
            soil["moisture"]
        )

        print()

        print(
            "✓ Values are now available"
        )

        print(
            "  for Crop Recommendation."
        )

    else:

        print(
            "❌ Server rejected the data."
        )

        print(
            result
        )


except Exception as error:

    print()
    print(
        "❌ ERROR sending sensor data:"
    )

    print(error)


print()
print("========================================")
print("             SCAN COMPLETE")
print("========================================")
print()