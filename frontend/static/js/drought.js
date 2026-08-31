// ============================================================
// AGRIMIND AI - DROUGHT RISK
// Live Location + Open-Meteo Analysis
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("droughtForm");
    const cropInput = document.getElementById("crop");

    const locationStatus =
        document.getElementById("locationStatus");

    const analyzeButton =
        document.getElementById("analyzeButton");

    const loading =
        document.getElementById("loading");

    const errorBox =
        document.getElementById("error");

    let latitude = null;
    let longitude = null;


    // ========================================================
    // INITIAL STATE
    // ========================================================

    if (loading) {
        loading.style.display = "none";
    }

    if (errorBox) {
        errorBox.style.display = "none";
    }


    // ========================================================
    // GET USER LOCATION
    // ========================================================

    function getLocation() {

        if (!navigator.geolocation) {

            locationStatus.textContent =
                "Geolocation is not supported by this browser.";

            return;
        }

        locationStatus.textContent =
            "Requesting location permission...";


        navigator.geolocation.getCurrentPosition(

            (position) => {

                latitude =
                    position.coords.latitude;

                longitude =
                    position.coords.longitude;


                locationStatus.textContent =
                    "Location detected ✓";


                locationStatus.style.color =
                    "#198754";

                console.log(
                    "LOCATION:",
                    latitude,
                    longitude
                );

            },

            (error) => {

                console.error(
                    "LOCATION ERROR:",
                    error
                );

                locationStatus.textContent =
                    "Unable to detect location. Allow location access.";

                locationStatus.style.color =
                    "#dc3545";
            },

            {
                enableHighAccuracy: true,
                timeout: 15000,
                maximumAge: 0
            }
        );
    }


    // ========================================================
    // REQUEST LOCATION
    // ========================================================

    getLocation();


    // ========================================================
    // FORM SUBMIT
    // ========================================================

    form.addEventListener("submit", async (event) => {

        event.preventDefault();


        // ----------------------------------------------------
        // CLEAR OLD ERROR
        // ----------------------------------------------------

        if (errorBox) {

            errorBox.textContent = "";

            errorBox.style.display = "none";
        }


        // ----------------------------------------------------
        // GET CROP
        // ----------------------------------------------------

        const crop =
            cropInput.value.trim();


        if (!crop) {

            showError(
                "Please enter a crop name."
            );

            cropInput.focus();

            return;
        }


        // ----------------------------------------------------
        // CHECK LOCATION
        // ----------------------------------------------------

        if (
            latitude === null ||
            longitude === null
        ) {

            showError(
                "Location is not available. Please allow location access and try again."
            );

            getLocation();

            return;
        }


        // ----------------------------------------------------
        // LOADING
        // ----------------------------------------------------

        analyzeButton.disabled = true;

        analyzeButton.textContent =
            "Analyzing...";


        if (loading) {
            loading.style.display = "flex";
        }


        try {

            console.log(
                "Sending drought request..."
            );

            console.log({
                crop: crop,
                latitude: latitude,
                longitude: longitude
            });


            // =================================================
            // CALL FLASK API
            // =================================================

            const response = await fetch(
                "/assess-drought",
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


            // =================================================
            // READ RESPONSE
            // =================================================

            const data =
                await response.json();


            console.log(
                "DROUGHT API RESPONSE:",
                data
            );


            // =================================================
            // API ERROR
            // =================================================

            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Drought analysis failed."
                );
            }


            if (!data.success) {

                throw new Error(
                    data.error ||
                    "Drought analysis failed."
                );
            }


            // =================================================
            // RESULT
            // =================================================

            displayResult(
                data.result
            );


        } catch (error) {

            console.error(
                "DROUGHT ANALYSIS ERROR:",
                error
            );


            showError(
                error.message ||
                "Unable to analyze drought risk."
            );


        } finally {

            analyzeButton.disabled = false;

            analyzeButton.textContent =
                "Analyze Drought Risk →";


            if (loading) {
                loading.style.display = "none";
            }
        }

    });


    // ========================================================
    // DISPLAY RESULT
    // ========================================================

    function displayResult(result) {

        if (!result) {

            showError(
                "The server returned an empty result."
            );

            return;
        }


        // ----------------------------------------------------
        // WEATHER
        // ----------------------------------------------------

        setText(
            "temperature",
            result.temperature !== null &&
            result.temperature !== undefined
                ? `${result.temperature}°C`
                : "--"
        );


        setText(
            "humidity",
            result.humidity !== null &&
            result.humidity !== undefined
                ? `${result.humidity}%`
                : "--"
        );


        setText(
            "currentRain",
            result.current_rain !== null &&
            result.current_rain !== undefined
                ? `${result.current_rain} mm`
                : "0 mm"
        );


        setText(
            "selectedCrop",
            result.crop || "--"
        );


        // ----------------------------------------------------
        // DROUGHT SCORE
        // ----------------------------------------------------

        setText(
            "score",
            result.score !== undefined
                ? result.score
                : "--"
        );


        setText(
            "riskName",
            result.risk || "--"
        );


        setText(
            "message",
            result.message || "--"
        );


        // ----------------------------------------------------
        // METRICS
        // ----------------------------------------------------

        setText(
            "rainfall7",
            result.rainfall_7_days !== undefined &&
            result.rainfall_7_days !== null
                ? `${result.rainfall_7_days} mm`
                : "--"
        );


        setText(
            "rainfall30",
            result.rainfall_30_days !== undefined &&
            result.rainfall_30_days !== null
                ? `${result.rainfall_30_days} mm`
                : "--"
        );


        setText(
            "soilMoisture",
            result.soil_moisture !== undefined &&
            result.soil_moisture !== null
                ? result.soil_moisture
                : "--"
        );


        setText(
            "maxTemperature",
            result.maximum_temperature !== undefined &&
            result.maximum_temperature !== null
                ? `${result.maximum_temperature}°C`
                : "--"
        );


        // ----------------------------------------------------
        // ANALYSIS LIST
        // ----------------------------------------------------

        const analysisList =
            document.getElementById(
                "analysisList"
            );


        if (analysisList) {

            analysisList.innerHTML = "";


            if (
                Array.isArray(result.analysis) &&
                result.analysis.length > 0
            ) {

                result.analysis.forEach(
                    (item) => {

                        const li =
                            document.createElement(
                                "li"
                            );

                        li.textContent =
                            item;

                        analysisList.appendChild(
                            li
                        );
                    }
                );

            } else {

                const li =
                    document.createElement(
                        "li"
                    );

                li.textContent =
                    "No additional analysis available.";

                analysisList.appendChild(
                    li
                );
            }
        }


        // ----------------------------------------------------
        // SHOW RESULT
        // ----------------------------------------------------

        const resultSection =
            document.getElementById(
                "result"
            );


        if (resultSection) {

            resultSection.style.display =
                "block";


            setTimeout(() => {

                resultSection.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }, 100);
        }

    }


    // ========================================================
    // HELPER - SET TEXT
    // ========================================================

    function setText(id, value) {

        const element =
            document.getElementById(id);


        if (element) {
            element.textContent = value;
        }
    }


    // ========================================================
    // SHOW ERROR
    // ========================================================

    function showError(message) {

        if (!errorBox) {

            alert(message);

            return;
        }


        errorBox.textContent =
            message;

        errorBox.style.display =
            "block";
    }

});