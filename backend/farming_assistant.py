# ============================================================
# AGRIMIND AI - FARMING ASSISTANT
# ============================================================


def get_farming_response(message):

    message = str(message).lower().strip()

    # --------------------------------------------------------
    # EMPTY QUESTION
    # --------------------------------------------------------

    if not message:

        return (
            "Please enter your farming question."
        )


    # --------------------------------------------------------
    # WATER REQUIREMENT
    # --------------------------------------------------------

    if (
        "how much water" in message
        or "water should" in message
        or "water requirement" in message
        or "how often water" in message
        or "how much irrigation" in message
    ):

        return (
            "🌱 Water requirements depend on the crop, soil type, "
            "temperature, rainfall and growth stage. As a general "
            "guide, avoid fixed watering schedules. Check the soil "
            "moisture first and irrigate when the root zone begins "
            "to dry. Water slowly and deeply rather than giving "
            "small amounts too frequently. During hot weather, "
            "plants may need more frequent irrigation, while "
            "rainy or highly humid conditions may require less."
        )


    # --------------------------------------------------------
    # IRRIGATION
    # --------------------------------------------------------

    if (
        "irrigation" in message
        or "irrigate" in message
        or "watering" in message
        or "water" in message
    ):

        return (
            "💧 Irrigation should be based on soil moisture, "
            "rainfall, temperature and the crop's water requirement. "
            "Check the soil before watering. Avoid irrigation when "
            "the soil is already sufficiently moist or significant "
            "rain is expected. Prefer watering during cooler parts "
            "of the day to reduce water loss."
        )


    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    if (
        "weather" in message
        or "rain" in message
        or "rainfall" in message
        or "temperature" in message
        or "humidity" in message
    ):

        return (
            "🌦️ Weather plays an important role in farming. "
            "Temperature, rainfall, humidity and wind can affect "
            "irrigation, crop growth and disease risk. Check the "
            "Weather Insights section in AgriMind AI for the latest "
            "weather conditions before making field-management "
            "decisions."
        )


    # --------------------------------------------------------
    # SOIL
    # --------------------------------------------------------

    if (
        "soil" in message
        or "ph" in message
        or "nitrogen" in message
        or "phosphorus" in message
        or "potassium" in message
        or "nutrient" in message
    ):

        return (
            "🌱 Soil health depends on nutrients, pH, moisture "
            "and soil characteristics. You can use the Soil Scan "
            "feature in AgriMind AI to analyze your soil. The "
            "results can help you understand the soil profile and "
            "identify crops that may be suitable for it."
        )


    # --------------------------------------------------------
    # CROP RECOMMENDATION
    # --------------------------------------------------------

    if (
        "crop" in message
        or "which crop" in message
        or "best crop" in message
        or "suitable crop" in message
        or "grow" in message
    ):

        return (
            "🌾 The best crop depends on your soil nutrients, pH, "
            "moisture, climate and available water. AgriMind AI "
            "can use your latest soil readings to recommend crops "
            "that match your field conditions. First scan your "
            "soil and then open Crop Recommendation."
        )


    # --------------------------------------------------------
    # DISEASE
    # --------------------------------------------------------

    if (
        "disease" in message
        or "leaf" in message
        or "plant disease" in message
        or "spots" in message
        or "yellow leaf" in message
        or "yellow leaves" in message
    ):

        return (
            "🍃 Plant diseases can cause symptoms such as leaf "
            "spots, yellowing, wilting or unusual growth. Use "
            "AgriMind AI's Disease Detection feature and upload "
            "a clear image of the affected leaf. The AI model can "
            "analyze the image and provide a possible disease "
            "prediction."
        )


    # --------------------------------------------------------
    # FERTILIZER
    # --------------------------------------------------------

    if (
        "fertilizer" in message
        or "fertiliser" in message
        or "manure" in message
        or "fertilize" in message
    ):

        return (
            "🧪 Fertilizer requirements depend on the crop and "
            "soil nutrient levels. Avoid applying fertilizer "
            "without understanding the soil condition. Check "
            "nitrogen, phosphorus, potassium and pH first, then "
            "choose a fertilizer plan appropriate for the crop."
        )


    # --------------------------------------------------------
    # NITROGEN
    # --------------------------------------------------------

    if "nitrogen" in message:

        return (
            "🌿 Nitrogen is an important nutrient for healthy "
            "vegetative growth and leaf development. Both "
            "deficiency and excessive nitrogen can affect crops. "
            "Use your soil readings to determine whether nitrogen "
            "levels are appropriate for the selected crop."
        )


    # --------------------------------------------------------
    # PHOSPHORUS
    # --------------------------------------------------------

    if "phosphorus" in message:

        return (
            "🧪 Phosphorus supports important processes such as "
            "root development and plant growth. The required level "
            "depends on the crop and soil condition. Soil testing "
            "is useful before applying additional phosphorus."
        )


    # --------------------------------------------------------
    # POTASSIUM
    # --------------------------------------------------------

    if "potassium" in message:

        return (
            "⚡ Potassium helps plants with several important "
            "functions, including water regulation and overall "
            "plant health. The appropriate level depends on the "
            "crop and existing soil nutrients."
        )


    # --------------------------------------------------------
    # SOIL MOISTURE
    # --------------------------------------------------------

    if (
        "moisture" in message
        or "dry soil" in message
        or "wet soil" in message
    ):

        return (
            "💧 Soil moisture is important for plant growth. "
            "Very dry soil can cause water stress, while "
            "excessively wet soil can reduce root aeration and "
            "increase the risk of some problems. Check your "
            "soil-moisture reading before irrigation."
        )


    # --------------------------------------------------------
    # PESTS
    # --------------------------------------------------------

    if (
        "pest" in message
        or "insect" in message
        or "insects" in message
        or "pesticide" in message
    ):

        return (
            "🐛 Monitor crops regularly for insects and visible "
            "damage. Identify the pest before choosing a control "
            "method. Integrated pest management can combine "
            "monitoring, prevention and appropriate control "
            "measures."
        )


    # --------------------------------------------------------
    # FARMING HELP
    # --------------------------------------------------------

    if (
        "help" in message
        or "what can you do" in message
        or "what can i ask" in message
    ):

        return (
            "🤖 I can help you with:\n\n"
            "🌾 Crop recommendations\n"
            "🌱 Soil management\n"
            "💧 Irrigation and water management\n"
            "🌦️ Weather-related farming decisions\n"
            "🍃 Plant disease information\n"
            "🧪 Soil nutrients and fertilizers\n"
            "🐛 Pest management\n\n"
            "Ask me any farming-related question."
        )


    # --------------------------------------------------------
    # DEFAULT RESPONSE
    # --------------------------------------------------------

    return (
        "🤖 I can help you with crops, soil, irrigation, "
        "weather, plant diseases, fertilizers, nutrients and "
        "general farm management. Please ask a specific farming "
        "question and I will try to guide you."
    )