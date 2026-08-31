/* =========================================================
   AGRIMIND AI
   SMART IRRIGATION JAVASCRIPT
========================================================= */


/* =========================================================
   VARIABLES
========================================================= */

let latitude = null;
let longitude = null;

let locationReady = false;


/* =========================================================
   ELEMENTS
========================================================= */

const cropInput =
    document.getElementById("cropInput");

const assessBtn =
    document.getElementById("assessBtn");

const locationStatus =
    document.getElementById("locationStatus");

const locationDot =
    document.getElementById("locationDot");

const errorMessage =
    document.getElementById("errorMessage");

const resultCard =
    document.getElementById("resultCard");

const emptyState =
    document.getElementById("emptyState");


/* =========================================================
   CROP SUGGESTIONS
========================================================= */

document
    .querySelectorAll(".suggestions button")
    .forEach(button => {

        button.addEventListener("click", () => {

            cropInput.value =
                button.dataset.crop;

            cropInput.focus();

        });

    });


/* =========================================================
   LOCATION
========================================================= */

function detectLocation() {

    if (!navigator.geolocation) {

        locationStatus.textContent =
            "Geolocation is not supported";

        return;

    }


    locationStatus.textContent =
        "Requesting location permission...";


    navigator.geolocation.getCurrentPosition(

        position => {

            latitude =
                position.coords.latitude;

            longitude =
                position.coords.longitude;

            locationReady = true;


            locationStatus.textContent =
                "Location detected ✓";

            locationDot.classList.add("active");


            console.log(
                "Latitude:",
                latitude
            );

            console.log(
                "Longitude:",
                longitude
            );

        },

        error => {

            console.error(
                "Location error:",
                error
            );

            locationReady = false;

            locationDot.classList.remove(
                "active"
            );


            if (
                error.code ===
                error.PERMISSION_DENIED
            ) {

                locationStatus.textContent =
                    "Location permission denied";

            } else {

                locationStatus.textContent =
                    "Unable to detect location";

            }

        },

        {
            enableHighAccuracy: true,

            timeout: 15000,

            maximumAge: 300000

        }

    );

}


/* =========================================================
   START LOCATION DETECTION
========================================================= */

detectLocation();


/* =========================================================
   ERROR
========================================================= */

function showError(message) {

    errorMessage.textContent =
        message;

}


/* =========================================================
   CLEAR ERROR
========================================================= */

function clearError() {

    errorMessage.textContent =
        "";

}


/* =========================================================
   FORMAT NUMBER
========================================================= */

function formatNumber(
    value,
    decimals = 1
) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return "--";

    }


    const number =
        Number(value);


    if (Number.isNaN(number)) {

        return "--";

    }


    return number.toFixed(
        decimals
    );

}


/* =========================================================
   WEATHER DISPLAY
========================================================= */

function updateWeather(data) {

    document.getElementById(
        "temperature"
    ).textContent =
        data.temperature !== null
            ? `${formatNumber(data.temperature)}°C`
            : "--";


    document.getElementById(
        "humidity"
    ).textContent =
        data.humidity !== null
            ? `${formatNumber(data.humidity, 0)}%`
            : "--";


    document.getElementById(
        "currentRain"
    ).textContent =
        `${formatNumber(data.current_rain)} mm`;


    document.getElementById(
        "expectedRain"
    ).textContent =
        `${formatNumber(data.expected_rain)} mm`;


    document.getElementById(
        "rainProbability"
    ).textContent =
        `${formatNumber(data.rain_probability, 0)}%`;

}


/* =========================================================
   RESULT DISPLAY
========================================================= */

function displayResult(result) {

    resultCard.classList.remove(
        "hidden"
    );

    emptyState.style.display =
        "none";


    /* -----------------------------------------
       STATUS
    ----------------------------------------- */

    document.getElementById(
        "resultStatus"
    ).textContent =
        result.status || "Assessment complete";


    document.getElementById(
        "resultBadge"
    ).textContent =
        result.recommendation ||
        "MONITOR FIELD";


    /* -----------------------------------------
       MESSAGE
    ----------------------------------------- */

    document.getElementById(
        "resultMessage"
    ).textContent =
        result.message || "--";


    /* -----------------------------------------
       METRICS
    ----------------------------------------- */

    document.getElementById(
        "resultRain"
    ).textContent =
        `${formatNumber(result.expected_rain)} mm`;


    if (
        result.soil_moisture !== null &&
        result.soil_moisture !== undefined
    ) {

        document.getElementById(
            "resultSoil"
        ).textContent =
            `${formatNumber(
                result.soil_moisture * 100,
                0
            )}%`;

    } else {

        document.getElementById(
            "resultSoil"
        ).textContent =
            "Unavailable";

    }


    document.getElementById(
        "resultET"
    ).textContent =
        `${formatNumber(
            result.evapotranspiration,
            1
        )} mm`;


    document.getElementById(
        "resultRequirement"
    ).textContent =
        result.crop_requirement
            ? result.crop_requirement
                .charAt(0)
                .toUpperCase()
                +
                result.crop_requirement
                    .slice(1)
            : "--";


    /* -----------------------------------------
       ANALYSIS
    ----------------------------------------- */

    const analysisList =
        document.getElementById(
            "analysisList"
        );


    analysisList.innerHTML =
        "";


    if (
        Array.isArray(result.analysis)
    ) {

        result.analysis.forEach(
            reason => {

                const item =
                    document.createElement(
                        "div"
                    );

                item.className =
                    "analysis-item";


                item.innerHTML = `
                    <span>✓</span>
                    <div>${escapeHtml(reason)}</div>
                `;


                analysisList.appendChild(
                    item
                );

            }
        );

    }


    /* -----------------------------------------
       TIP
    ----------------------------------------- */

    document.getElementById(
        "resultTip"
    ).textContent =
        result.tip || "--";


    /* -----------------------------------------
       SCROLL
    ----------------------------------------- */

    setTimeout(() => {

        resultCard.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }, 100);

}


/* =========================================================
   HTML ESCAPE
========================================================= */

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        text;

    return div.innerHTML;

}


/* =========================================================
   ASSESS IRRIGATION
========================================================= */

async function assessIrrigation() {

    clearError();


    /* -----------------------------------------
       CROP VALIDATION
    ----------------------------------------- */

    const crop =
        cropInput.value.trim();


    if (!crop) {

        showError(
            "Please enter or select a crop."
        );

        cropInput.focus();

        return;

    }


    /* -----------------------------------------
       LOCATION VALIDATION
    ----------------------------------------- */

    if (
        !locationReady ||
        latitude === null ||
        longitude === null
    ) {

        showError(
            "Live location is required. Please allow location access and try again."
        );

        detectLocation();

        return;

    }


    /* -----------------------------------------
       LOADING
    ----------------------------------------- */

    assessBtn.disabled = true;


    assessBtn.innerHTML = `
        <span>⏳</span>
        <span>Analyzing live conditions...</span>
    `;


    try {

        /* -----------------------------------------
           API REQUEST
        ----------------------------------------- */

        const response =
            await fetch(
                "/assess-irrigation",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        crop: crop,

                        latitude:
                            latitude,

                        longitude:
                            longitude

                    })

                }
            );


        const data =
            await response.json();


        /* -----------------------------------------
           API ERROR
        ----------------------------------------- */

        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.error ||
                "Unable to complete irrigation assessment."
            );

        }


        /* -----------------------------------------
           UPDATE WEATHER
        ----------------------------------------- */

        updateWeather(data);


        /* -----------------------------------------
           DISPLAY RESULT
        ----------------------------------------- */

        displayResult(data);


    }

    catch (error) {

        console.error(
            "IRRIGATION ERROR:",
            error
        );


        showError(
            error.message ||
            "Something went wrong. Please try again."
        );

    }

    finally {

        assessBtn.disabled = false;


        assessBtn.innerHTML = `
            <span>💧</span>
            <span>Assess Irrigation</span>
            <span>→</span>
        `;

    }

}


/* =========================================================
   BUTTON
========================================================= */

assessBtn.addEventListener(
    "click",
    assessIrrigation
);


/* =========================================================
   ENTER KEY
========================================================= */

cropInput.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Enter"
        ) {

            assessIrrigation();

        }

    }
);