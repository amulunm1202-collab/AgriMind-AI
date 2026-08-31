// ============================================================
// AGRIMIND AI - REAL PEST DETECTION
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("pestForm");
    const fileInput = document.getElementById("imageInput");
    const analyzeButton = document.getElementById("analyzeButton");

    const loading = document.getElementById("loading");
    const errorBox = document.getElementById("error");
    const result = document.getElementById("result");

    const pestName = document.getElementById("pestName");
    const confidence = document.getElementById("confidence");
    const severity = document.getElementById("severity");
    const description = document.getElementById("description");
    const recommendedAction =
        document.getElementById("recommendedAction");


    // ========================================================
    // ERROR
    // ========================================================

    function showError(message) {

        if (errorBox) {

            errorBox.textContent = message;
            errorBox.style.display = "block";

        }

    }


    function clearError() {

        if (errorBox) {

            errorBox.textContent = "";
            errorBox.style.display = "none";

        }

    }


    // ========================================================
    // CHECK FORM
    // ========================================================

    if (!form) {

        console.error("pestForm not found.");
        return;

    }


    // ========================================================
    // FORM SUBMIT
    // ========================================================

    form.addEventListener("submit", async function (event) {

        event.preventDefault();

        clearError();


        // ====================================================
        // CHECK IMAGE
        // ====================================================

        if (
            !fileInput ||
            !fileInput.files ||
            fileInput.files.length === 0
        ) {

            showError(
                "Please select a crop image first."
            );

            return;

        }


        const file = fileInput.files[0];


        // ====================================================
        // CHECK FILE TYPE
        // ====================================================

        const allowedTypes = [
            "image/jpeg",
            "image/jpg",
            "image/png",
            "image/webp"
        ];


        if (!allowedTypes.includes(file.type)) {

            showError(
                "Please upload JPG, JPEG, PNG or WEBP."
            );

            return;

        }


        // ====================================================
        // LOADING
        // ====================================================

        if (analyzeButton) {

            analyzeButton.disabled = true;
            analyzeButton.textContent = "Analyzing...";

        }


        if (loading) {

            loading.style.display = "block";

        }


        if (result) {

            result.style.display = "none";

        }


        // ====================================================
        // FORM DATA
        // ====================================================

        const formData = new FormData();

        formData.append(
            "image",
            file
        );


        // ====================================================
        // SEND TO FLASK
        // ====================================================

        try {

            console.log(
                "Sending image to real pest model..."
            );


            const response = await fetch(
                "/predict-pest",
                {
                    method: "POST",
                    body: formData
                }
            );


            console.log(
                "Pest API status:",
                response.status
            );


            // =================================================
            // CHECK RESPONSE TYPE
            // =================================================

            const contentType =
                response.headers.get(
                    "content-type"
                ) || "";


            if (
                !contentType.includes(
                    "application/json"
                )
            ) {

                const text =
                    await response.text();

                console.error(
                    "Server returned non-JSON:",
                    text
                );

                throw new Error(
                    "Server returned an invalid response. Check the Flask /predict-pest route."
                );

            }


            // =================================================
            // JSON
            // =================================================

            const data =
                await response.json();


            console.log(
                "Pest API response:",
                data
            );


            // =================================================
            // API ERROR
            // =================================================

            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Pest detection failed."
                );

            }


            if (!data.success) {

                throw new Error(
                    data.error ||
                    "Pest detection failed."
                );

            }


            // =================================================
            // RESULT
            // =================================================

            const prediction =
                data.result;


            if (!prediction) {

                throw new Error(
                    "The pest model returned no prediction."
                );

            }


            console.log(
                "REAL PEST RESULT:",
                prediction
            );


            // =================================================
            // PEST NAME
            // =================================================

            if (pestName) {

                pestName.textContent =
                    prediction.pest || "--";

            }


            // =================================================
            // CONFIDENCE
            // =================================================

            if (confidence) {

                const confidenceValue =
                    Number(
                        prediction.confidence
                    );


                if (Number.isFinite(confidenceValue)) {

                    confidence.textContent =
                        confidenceValue.toFixed(1) + "%";

                } else {

                    confidence.textContent = "--";

                }

            }


            // =================================================
            // SEVERITY
            // =================================================

            if (severity) {

                severity.textContent =
                    prediction.severity || "--";

            }


            // =================================================
            // DESCRIPTION
            // =================================================

            if (description) {

                description.textContent =
                    prediction.description || "--";

            }


            // =================================================
            // ACTION
            // =================================================

            if (recommendedAction) {

                recommendedAction.textContent =
                    prediction.recommended_action || "--";

            }


            // =================================================
            // SHOW RESULT
            // =================================================

            if (result) {

                result.style.display = "block";

            }


        }

        catch (error) {

            console.error(
                "REAL PEST DETECTION ERROR:",
                error
            );


            showError(
                error.message ||
                "Unable to analyze the image."
            );

        }


        finally {

            if (loading) {

                loading.style.display = "none";

            }


            if (analyzeButton) {

                analyzeButton.disabled = false;
                analyzeButton.textContent =
                    "Analyze Pest →";

            }

        }

    });

});