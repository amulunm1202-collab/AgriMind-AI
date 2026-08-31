/* ============================================================
   AGRIMIND AI — CROP RECOMMENDATION
   Soil Scan → Weather → AI Crop Recommendation
============================================================ */


/* ============================================================
   GLOBAL DATA
============================================================ */

let soilData = null;
let weatherData = null;


/* ============================================================
   DOM READY
============================================================ */

document.addEventListener("DOMContentLoaded", async function () {

    console.log("🌱 AgriMind AI Crop Recommendation started");

    await loadSoilData();
    await loadWeather();

});


/* ============================================================
   LOAD LATEST SOIL SCAN
============================================================ */

async function loadSoilData() {

    try {

        console.log("🧪 Loading latest soil scan...");

        const response = await fetch(
            "/api/soil-data",
            {
                method: "GET",

                headers: {
                    "Accept": "application/json"
                },

                cache: "no-store"
            }
        );


        /* ----------------------------------------------------
           CHECK HTTP STATUS
        ---------------------------------------------------- */

        if (!response.ok) {

            let errorMessage =
                "Soil scan data could not be loaded.";

            try {

                const errorData =
                    await response.json();

                errorMessage =
                    errorData.error ||
                    errorData.message ||
                    errorMessage;

            }
            catch (_) {
                // Ignore JSON parsing error
            }

            throw new Error(errorMessage);

        }


        /* ----------------------------------------------------
           READ JSON
        ---------------------------------------------------- */

        const data =
            await response.json();

        console.log(
            "🧪 Soil API response:",
            data
        );


        /* ----------------------------------------------------
           BACKEND ERROR
        ---------------------------------------------------- */

        if (data.success === false) {

            throw new Error(
                data.error ||
                data.message ||
                "No soil scan available."
            );

        }


        /* ----------------------------------------------------
           SUPPORT DIFFERENT RESPONSE STRUCTURES
        ---------------------------------------------------- */

        soilData =
            data.soil ||
            data.result ||
            data.data ||
            data;


        if (!soilData) {

            throw new Error(
                "Latest soil scan is empty."
            );

        }


        /* ----------------------------------------------------
           EXTRACT NITROGEN
        ---------------------------------------------------- */

        const nitrogen =
            getNumber(
                soilData.nitrogen ??
                soilData.N ??
                soilData.n
            );


        /* ----------------------------------------------------
           EXTRACT PHOSPHORUS
        ---------------------------------------------------- */

        const phosphorus =
            getNumber(
                soilData.phosphorus ??
                soilData.P ??
                soilData.p
            );


        /* ----------------------------------------------------
           EXTRACT POTASSIUM
        ---------------------------------------------------- */

        const potassium =
            getNumber(
                soilData.potassium ??
                soilData.K ??
                soilData.k
            );


        /* ----------------------------------------------------
           EXTRACT PH
        ---------------------------------------------------- */

        const ph =
            getNumber(
                soilData.ph ??
                soilData.pH ??
                soilData.PH
            );


        /* ----------------------------------------------------
           EXTRACT MOISTURE
        ---------------------------------------------------- */

        const moisture =
            getNumber(
                soilData.moisture ??
                soilData.soil_moisture ??
                soilData.moisture_percent
            );


        /* ----------------------------------------------------
           VALIDATE SOIL
        ---------------------------------------------------- */

        if (
            nitrogen === null ||
            phosphorus === null ||
            potassium === null ||
            ph === null
        ) {

            throw new Error(
                "The latest soil scan does not contain complete NPK and pH values."
            );

        }


        /* ----------------------------------------------------
           STORE CLEAN SOIL DATA
        ---------------------------------------------------- */

        soilData = {

            nitrogen: nitrogen,

            phosphorus: phosphorus,

            potassium: potassium,

            ph: ph,

            moisture: moisture

        };


        /* ----------------------------------------------------
           DISPLAY SOIL
        ---------------------------------------------------- */

        setText(
            "nitrogen",
            formatValue(nitrogen)
        );


        setText(
            "phosphorus",
            formatValue(phosphorus)
        );


        setText(
            "potassium",
            formatValue(potassium)
        );


        setText(
            "ph",
            formatValue(ph)
        );


        setText(
            "moisture",
            formatValue(moisture)
        );


        console.log(
            "✅ Latest soil scan loaded:",
            soilData
        );

    }


    catch (error) {

        console.error(
            "❌ SOIL ERROR:",
            error
        );

        soilData = null;

        showError(
            error.message ||
            "Please scan your soil first."
        );

    }

}


/* ============================================================
   LOAD CURRENT WEATHER
============================================================ */

async function loadWeather() {

    try {

        console.log(
            "🌤️ Loading current weather..."
        );


        const response =
            await fetch(
                "/weather-data",
                {
                    method: "GET",

                    headers: {
                        "Accept": "application/json"
                    },

                    cache: "no-store"
                }
            );


        /* ----------------------------------------------------
           CHECK HTTP STATUS
        ---------------------------------------------------- */

        if (!response.ok) {

            let errorMessage =
                "Weather data could not be loaded.";

            try {

                const errorData =
                    await response.json();

                errorMessage =
                    errorData.error ||
                    errorData.message ||
                    errorMessage;

            }
            catch (_) {
                // Ignore JSON parsing error
            }

            throw new Error(
                errorMessage
            );

        }


        /* ----------------------------------------------------
           READ JSON
        ---------------------------------------------------- */

        const data =
            await response.json();

        console.log(
            "🌤️ Weather API response:",
            data
        );


        /* ----------------------------------------------------
           BACKEND ERROR
        ---------------------------------------------------- */

        if (data.success === false) {

            throw new Error(
                data.error ||
                data.message ||
                "Weather unavailable."
            );

        }


        /* ----------------------------------------------------
           EXTRACT WEATHER
        ---------------------------------------------------- */

        const temperature =
            getNumber(
                data.temperature
            );


        const humidity =
            getNumber(
                data.humidity
            );


        const rainfall =
            getNumber(
                data.rainfall
            );


        /* ----------------------------------------------------
           VALIDATE WEATHER
        ---------------------------------------------------- */

        if (
            temperature === null ||
            humidity === null ||
            rainfall === null
        ) {

            throw new Error(
                "Complete weather information is unavailable."
            );

        }


        /* ----------------------------------------------------
           STORE WEATHER
        ---------------------------------------------------- */

        weatherData = {

            temperature: temperature,

            humidity: humidity,

            rainfall: rainfall,

            condition:
                data.condition ||
                "Current weather",

            weather_icon:
                data.weather_icon ||
                "🌤️"

        };


        /* ----------------------------------------------------
           DISPLAY WEATHER
        ---------------------------------------------------- */

        setText(
            "temperature",
            `${temperature.toFixed(1)} °C`
        );


        setText(
            "humidity",
            `${humidity.toFixed(1)} %`
        );


        setText(
            "rainfall",
            `${rainfall.toFixed(1)} mm`
        );


        setText(
            "condition",
            `${weatherData.weather_icon} ${weatherData.condition}`
        );


        console.log(
            "✅ Weather loaded:",
            weatherData
        );

    }


    catch (error) {

        console.error(
            "❌ WEATHER ERROR:",
            error
        );


        weatherData = null;


        setText(
            "temperature",
            "—"
        );


        setText(
            "humidity",
            "—"
        );


        setText(
            "rainfall",
            "—"
        );


        setText(
            "condition",
            "Unavailable"
        );


        showError(
            error.message ||
            "Current weather could not be loaded."
        );

    }

}


/* ============================================================
   GET CROP RECOMMENDATION
============================================================ */

async function getRecommendation() {

    hideError();


    /* --------------------------------------------------------
       CHECK SOIL
    -------------------------------------------------------- */

    if (!soilData) {

        showError(
            "No soil scan is available. Please scan your soil first."
        );

        return;

    }


    /* --------------------------------------------------------
       CHECK WEATHER
    -------------------------------------------------------- */

    if (!weatherData) {

        showError(
            "Weather data is unavailable. Please try again."
        );

        return;

    }


    /* --------------------------------------------------------
       EXTRACT SOIL
    -------------------------------------------------------- */

    const nitrogen =
        getNumber(
            soilData.nitrogen
        );


    const phosphorus =
        getNumber(
            soilData.phosphorus
        );


    const potassium =
        getNumber(
            soilData.potassium
        );


    const ph =
        getNumber(
            soilData.ph
        );


    /* --------------------------------------------------------
       EXTRACT WEATHER
    -------------------------------------------------------- */

    const temperature =
        getNumber(
            weatherData.temperature
        );


    const humidity =
        getNumber(
            weatherData.humidity
        );


    const rainfall =
        getNumber(
            weatherData.rainfall
        );


    /* --------------------------------------------------------
       VALIDATE SOIL
    -------------------------------------------------------- */

    if (
        nitrogen === null ||
        phosphorus === null ||
        potassium === null ||
        ph === null
    ) {

        showError(
            "The latest soil scan does not contain complete NPK and pH values."
        );

        return;

    }


    /* --------------------------------------------------------
       VALIDATE WEATHER
    -------------------------------------------------------- */

    if (
        temperature === null ||
        humidity === null ||
        rainfall === null
    ) {

        showError(
            "Complete weather information is required."
        );

        return;

    }


    /* --------------------------------------------------------
       BUTTON
    -------------------------------------------------------- */

    const button =
        document.getElementById(
            "recommendBtn"
        );


    const loading =
        document.getElementById(
            "loading"
        );


    if (button) {

        button.disabled = true;

    }


    if (loading) {

        loading.style.display =
            "block";

    }


    /* ========================================================
       FINAL INPUT TO ML MODEL
    ======================================================== */

    const payload = {

        nitrogen:
            nitrogen,

        phosphorus:
            phosphorus,

        potassium:
            potassium,

        ph:
            ph,

        temperature:
            temperature,

        humidity:
            humidity,

        rainfall:
            rainfall

    };


    console.log(
        "🌱 FINAL CROP INPUT:",
        payload
    );


    try {


        /* ====================================================
           IMPORTANT FIX
           
           YOUR FLASK ROUTE IS:

           @app.route("/crop-recommendation", methods=["POST"])

           Therefore the URL MUST BE:

           /crop-recommendation

           NOT:

           /api/crop-recommendation
        ==================================================== */


        const response =
            await fetch(
                "/crop-recommendation",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"

                    },

                    body:
                        JSON.stringify(
                            payload
                        )

                }
            );


        /* ====================================================
           READ RESPONSE SAFELY
        ==================================================== */

        let data = null;


        const contentType =
            response.headers.get(
                "content-type"
            ) || "";


        if (
            contentType.includes(
                "application/json"
            )
        ) {

            data =
                await response.json();

        }

        else {

            const text =
                await response.text();

            console.error(
                "❌ Server returned non-JSON:",
                text
            );


            throw new Error(
                `Server returned ${response.status} ${response.statusText}.`
            );

        }


        console.log(
            "🌾 Crop recommendation response:",
            data
        );


        /* ====================================================
           CHECK HTTP ERROR
        ==================================================== */

        if (!response.ok) {

            throw new Error(

                data.error ||
                data.message ||
                "Crop recommendation failed."

            );

        }


        /* ====================================================
           CHECK BACKEND SUCCESS
        ==================================================== */

        if (
            data.success === false
        ) {

            throw new Error(

                data.error ||
                data.message ||
                "Crop recommendation failed."

            );

        }


        /* ====================================================
           GET RESULT
        ==================================================== */

        const result =
            data.result ||
            data;


        if (!result) {

            throw new Error(
                "No recommendation result received."
            );

        }


        /* ====================================================
           DISPLAY RESULT
        ==================================================== */

        displayResult(
            result
        );

    }


    catch (error) {

        console.error(
            "❌ CROP RECOMMENDATION ERROR:",
            error
        );


        showError(
            error.message ||
            "Unable to generate crop recommendation."
        );

    }


    finally {

        if (button) {

            button.disabled = false;

        }


        if (loading) {

            loading.style.display =
                "none";

        }

    }

}


/* ============================================================
   DISPLAY RESULT
============================================================ */

function displayResult(result) {

    if (!result) {

        showError(
            "No crop recommendation was received."
        );

        return;

    }


    const section =
        document.getElementById(
            "resultSection"
        );


    if (section) {

        section.style.display =
            "block";

    }


    /* ========================================================
       CROP
    ======================================================== */

    const crop =
        result.crop ||
        result.recommended_crop ||
        result.recommendedCrop ||
        "Unknown";


    setText(
        "recommendedCrop",
        formatCropName(crop)
    );


    /* ========================================================
       CONFIDENCE
    ======================================================== */

    let confidence =
        result.confidence ??
        result.score ??
        0;


    confidence =
        Number(
            confidence
        );


    if (
        !Number.isFinite(
            confidence
        )
    ) {

        confidence = 0;

    }


    confidence =
        Math.max(
            0,
            Math.min(
                100,
                confidence
            )
        );


    setText(
        "confidence",
        `Confidence: ${confidence.toFixed(1)}%`
    );


    /* ========================================================
       MODEL
    ======================================================== */

    setText(
        "model",
        result.model ||
        "Random Forest Classifier"
    );


    /* ========================================================
       MODEL ACCURACY
    ======================================================== */

    const accuracy =
        result.model_accuracy ??
        result.accuracy ??
        null;


    if (
        accuracy !== null &&
        Number.isFinite(
            Number(accuracy)
        )
    ) {

        setText(
            "accuracy",
            `${Number(accuracy).toFixed(2)}%`
        );

    }

    else {

        setText(
            "accuracy",
            "—"
        );

    }


    /* ========================================================
       WATER REQUIREMENT
    ======================================================== */

    setText(
        "water",
        result.water_requirement ||
        result.water ||
        "Moderate"
    );


    /* ========================================================
       TOP CROPS
    ======================================================== */

    const cropList =
        document.getElementById(
            "cropList"
        );


    if (!cropList) {

        console.warn(
            "cropList element not found."
        );

        return;

    }


    cropList.innerHTML = "";


    let crops =
        result.ranked_crops ||
        result.top_crops ||
        result.recommendations ||
        [];


    if (!Array.isArray(crops)) {

        crops = [];

    }


    /* ========================================================
       CREATE TOP 5 CROPS
    ======================================================== */

    crops
        .slice(0, 5)
        .forEach(
            function (item, index) {


                let name =
                    "Crop";


                let score =
                    "";


                /* ------------------------------------------------
                   STRING
                ------------------------------------------------ */

                if (
                    typeof item ===
                    "string"
                ) {

                    name =
                        item;

                }


                /* ------------------------------------------------
                   OBJECT
                ------------------------------------------------ */

                else if (
                    item &&
                    typeof item ===
                    "object"
                ) {

                    name =
                        item.crop ||
                        item.name ||
                        item.recommended_crop ||
                        "Crop";


                    score =
                        item.confidence ??
                        item.score ??
                        item.probability ??
                        "";

                }


                /* ------------------------------------------------
                   CREATE ROW
                ------------------------------------------------ */

                const div =
                    document.createElement(
                        "div"
                    );


                div.className =
                    "crop-item";


                const nameElement =
                    document.createElement(
                        "span"
                    );


                nameElement.className =
                    "crop-name";


                nameElement.textContent =
                    `${index + 1}. ${formatCropName(name)}`;


                const scoreElement =
                    document.createElement(
                        "span"
                    );


                scoreElement.className =
                    "crop-score";


                if (
                    score !== "" &&
                    Number.isFinite(
                        Number(score)
                    )
                ) {

                    scoreElement.textContent =
                        `${Number(score).toFixed(1)}%`;

                }

                else {

                    scoreElement.textContent =
                        "Recommended";

                }


                div.appendChild(
                    nameElement
                );


                div.appendChild(
                    scoreElement
                );


                cropList.appendChild(
                    div
                );

            }
        );


    /* ========================================================
       FALLBACK
    ======================================================== */

    if (
        cropList.children.length ===
        0
    ) {

        const div =
            document.createElement(
                "div"
            );


        div.className =
            "crop-item";


        const nameElement =
            document.createElement(
                "span"
            );


        nameElement.className =
            "crop-name";


        nameElement.textContent =
            `1. ${formatCropName(crop)}`;


        const scoreElement =
            document.createElement(
                "span"
            );


        scoreElement.className =
            "crop-score";


        scoreElement.textContent =
            `${confidence.toFixed(1)}%`;


        div.appendChild(
            nameElement
        );


        div.appendChild(
            scoreElement
        );


        cropList.appendChild(
            div
        );

    }


    /* ========================================================
       MESSAGE
    ======================================================== */

    const message =
        result.message ||
        result.reason ||
        result.description ||
        `Based on the latest soil scan and current environmental conditions, ${formatCropName(crop)} is the top AI recommendation.`;


    setText(
        "message",
        message
    );


    /* ========================================================
       SCROLL TO RESULT
    ======================================================== */

    if (section) {

        section.scrollIntoView({

            behavior: "smooth",

            block: "start"

        });

    }


    /* ========================================================
       DEBUG
    ======================================================== */

    console.log(
        "✅ FINAL RECOMMENDATION:",
        {
            crop: crop,

            confidence:
                confidence,

            soil:
                soilData,

            weather:
                weatherData,

            result:
                result
        }
    );

}


/* ============================================================
   NUMBER CONVERSION
============================================================ */

function getNumber(value) {

    if (
        value === undefined ||
        value === null ||
        value === ""
    ) {

        return null;

    }


    const number =
        Number(
            value
        );


    if (
        !Number.isFinite(
            number
        )
    ) {

        return null;

    }


    return number;

}


/* ============================================================
   FORMAT VALUE
============================================================ */

function formatValue(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "—";

    }


    const number =
        Number(
            value
        );


    if (
        Number.isFinite(
            number
        )
    ) {

        if (
            Number.isInteger(
                number
            )
        ) {

            return String(
                number
            );

        }


        return number.toFixed(2);

    }


    return String(
        value
    );

}


/* ============================================================
   FORMAT CROP NAME
============================================================ */

function formatCropName(name) {

    if (
        name === null ||
        name === undefined
    ) {

        return "Unknown";

    }


    return String(name)
        .trim()
        .replace(
            /\b\w/g,
            function (letter) {
                return letter.toUpperCase();
            }
        );

}


/* ============================================================
   SET TEXT SAFELY
============================================================ */

function setText(
    elementId,
    value
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {

        console.warn(
            `Element #${elementId} not found.`
        );

        return;

    }


    element.textContent =
        value;

}


/* ============================================================
   SHOW ERROR
============================================================ */

function showError(message) {

    const error =
        document.getElementById(
            "error"
        );


    if (!error) {

        console.error(
            "ERROR:",
            message
        );

        return;

    }


    error.textContent =
        "❌ " +
        (
            message ||
            "Something went wrong."
        );


    error.style.display =
        "block";

}


/* ============================================================
   HIDE ERROR
============================================================ */

function hideError() {

    const error =
        document.getElementById(
            "error"
        );


    if (error) {

        error.style.display =
            "none";

    }

}
// ============================================================
// SHOW CROP RECOMMENDATION SECTION
// ============================================================

const cropSection =
    document.getElementById(
        "cropSection"
    );


// ============================================================
// SHOW AFTER SOIL ANALYSIS
// ============================================================

// Add this inside your successful soil analysis section
// after:
//
// result.style.display = "block";

cropSection.style.display =
    "block";


// ============================================================
// CROP RECOMMENDATION BUTTON
// ============================================================

const recommendCropBtn =
    document.getElementById(
        "recommendCropBtn"
    );


recommendCropBtn.addEventListener(
    "click",
    async function () {

        const nitrogen =
            document.getElementById(
                "nitrogen"
            ).value;

        const phosphorus =
            document.getElementById(
                "phosphorus"
            ).value;

        const potassium =
            document.getElementById(
                "potassium"
            ).value;

        const ph =
            document.getElementById(
                "ph"
            ).value;

        const temperature =
            document.getElementById(
                "temperature"
            ).value;

        const humidity =
            document.getElementById(
                "humidity"
            ).value;

        const rainfall =
            document.getElementById(
                "rainfall"
            ).value;


        // ----------------------------------------------------
        // VALIDATION
        // ----------------------------------------------------

        if (
            nitrogen === "" ||
            phosphorus === "" ||
            potassium === "" ||
            ph === ""
        ) {

            showMessage(
                "Please enter N, P, K and pH values.",
                "error"
            );

            return;
        }


        recommendCropBtn.disabled =
            true;

        recommendCropBtn.textContent =
            "🔄 Calculating recommendation...";


        try {

            const response =
                await fetch(
                    "/api/crop-recommendation",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            nitrogen:
                                parseFloat(
                                    nitrogen
                                ),

                            phosphorus:
                                parseFloat(
                                    phosphorus
                                ),

                            potassium:
                                parseFloat(
                                    potassium
                                ),

                            ph:
                                parseFloat(
                                    ph
                                ),

                            temperature:
                                parseFloat(
                                    temperature
                                ),

                            humidity:
                                parseFloat(
                                    humidity
                                ),

                            rainfall:
                                parseFloat(
                                    rainfall
                                )
                        })
                    }
                );


            const data =
                await response.json();


            if (
                !response.ok ||
                !data.success
            ) {

                throw new Error(
                    data.message ||
                    data.error ||
                    "Crop recommendation failed."
                );
            }


            // ------------------------------------------------
            // DISPLAY BEST CROP
            // ------------------------------------------------

            const recommendation =
                data.recommendation;


            document.getElementById(
                "recommendedCrop"
            ).textContent =
                recommendation
                    .recommended_crop
                    .replace(
                        /\b\w/g,
                        c => c.toUpperCase()
                    );


            // ------------------------------------------------
            // CONFIDENCE
            // ------------------------------------------------

            document.getElementById(
                "cropConfidence"
            ).textContent =
                recommendation.confidence +
                "%";


            // ------------------------------------------------
            // MODEL ACCURACY
            // ------------------------------------------------

            document.getElementById(
                "modelAccuracy"
            ).textContent =
                recommendation.model_accuracy +
                "%";


            // ------------------------------------------------
            // TOP CROPS
            // ------------------------------------------------

            const topCrops =
                document.getElementById(
                    "topCrops"
                );


            topCrops.innerHTML = "";


            recommendation.ranked_crops
                .forEach(
                    function (item, index) {

                        const row =
                            document.createElement(
                                "div"
                            );

                        row.style.padding =
                            "10px 0";

                        row.style.borderBottom =
                            "1px solid #dcebe0";

                        row.innerHTML =
                            `
                            <strong>
                                ${index + 1}.
                                ${item.crop}
                            </strong>

                            <span
                                style="
                                    float:right;
                                    color:#168547;
                                    font-weight:bold;
                                "
                            >
                                ${item.confidence}%
                            </span>
                            `;

                        topCrops.appendChild(
                            row
                        );

                    }
                );


            // ------------------------------------------------
            // SHOW RESULT
            // ------------------------------------------------

            document.getElementById(
                "cropResult"
            ).style.display =
                "block";


            showMessage(
                "Real ML crop recommendation generated successfully.",
                "success"
            );


        } catch (error) {

            console.error(
                "Crop recommendation error:",
                error
            );

            showMessage(
                error.message ||
                "Unable to generate crop recommendation.",
                "error"
            );

        } finally {

            recommendCropBtn.disabled =
                false;

            recommendCropBtn.textContent =
                "🌾 Recommend Best Crop";
        }

    }
);