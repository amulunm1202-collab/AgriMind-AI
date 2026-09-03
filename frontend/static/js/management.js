/* =========================================================
   AGRIMIND AI - CROP HEALTH MANAGEMENT
   =========================================================
   Reads the detection result (crop, problem, confidence,
   severity, weather) from the query string, calls the real
   management / prevention API and renders the result page.
   ========================================================= */

(function () {

    "use strict";

    /* -----------------------------------------------------
       DOM references
    ----------------------------------------------------- */
    var loadingState = document.getElementById("loadingState");
    var errorState = document.getElementById("errorState");
    var errorTitle = document.getElementById("errorTitle");
    var errorMessage = document.getElementById("errorMessage");
    var content = document.getElementById("content");

    var summaryCard = document.getElementById("summaryCard");
    var earlyBanner = document.getElementById("earlyBanner");
    var riskBanner = document.getElementById("riskBanner");

    var symptomsCard = document.getElementById("symptomsCard");
    var symptomsIcon = document.getElementById("symptomsIcon");
    var symptomsTitle = document.getElementById("symptomsTitle");
    var symptomsList = document.getElementById("symptomsList");

    var warningCard = document.getElementById("warningCard");
    var warningList = document.getElementById("warningList");

    var preventionCard = document.getElementById("preventionCard");
    var preventionList = document.getElementById("preventionList");

    var managementCard = document.getElementById("managementCard");
    var managementList = document.getElementById("managementList");

    var controlCard = document.getElementById("controlCard");
    var controlBody = document.getElementById("controlBody");

    var chemicalCard = document.getElementById("chemicalCard");
    var chemicalBody = document.getElementById("chemicalBody");

    var weatherCard = document.getElementById("weatherCard");
    var weatherBody = document.getElementById("weatherBody");

    var monitoringCard = document.getElementById("monitoringCard");
    var monitoringList = document.getElementById("monitoringList");

    var safetyCard = document.getElementById("safetyCard");
    var safetyList = document.getElementById("safetyList");

    var sourceCard = document.getElementById("sourceCard");
    var sourceList = document.getElementById("sourceList");


    /* -----------------------------------------------------
       Helpers
    ----------------------------------------------------- */

    function params() {
        return new URLSearchParams(window.location.search);
    }

    function showError(title, message) {
        loadingState.classList.add("hidden");
        content.classList.add("hidden");
        errorState.classList.remove("hidden");
        errorTitle.textContent = title || "Something went wrong";
        errorMessage.textContent = message || "";
    }

    function clearList(el) {
        while (el.firstChild) {
            el.removeChild(el.firstChild);
        }
    }

    function addListItem(el, text) {
        var li = document.createElement("li");
        li.textContent = text;
        el.appendChild(li);
    }

    function addBulletList(el, items) {
        clearList(el);
        (items || []).forEach(function (item) {
            if (item) {
                addListItem(el, item);
            }
        });
    }

    function addBodyList(container, items) {
        var ul = document.createElement("ul");
        ul.className = "section-list";
        (items || []).forEach(function (item) {
            if (item) {
                addListItem(ul, item);
            }
        });
        container.appendChild(ul);
    }

    function subsection(container, label, items) {
        var wrap = document.createElement("div");
        var title = document.createElement("div");
        title.className = "subsection-label";
        title.textContent = label;
        wrap.appendChild(title);
        addBodyList(wrap, items);
        container.appendChild(wrap);
    }

    function summaryItem(label, value) {
        var div = document.createElement("div");
        div.className = "summary-item";
        var l = document.createElement("span");
        l.className = "label";
        l.textContent = label;
        var v = document.createElement("div");
        v.className = "value";
        v.textContent = value;
        div.appendChild(l);
        div.appendChild(v);
        return div;
    }

    function show(element) {
        element.classList.remove("hidden");
    }

    function hide(element) {
        element.classList.add("hidden");
    }


    /* -----------------------------------------------------
       Read detection inputs
    ----------------------------------------------------- */
    var q = params();

    var crop = q.get("crop") || "";
    // 'problem' carries the disease OR pest name
    var problem = q.get("problem") || q.get("disease") || q.get("pest") || "";
    var type = (q.get("type") || "disease").toLowerCase();

    var confidence = q.get("confidence");      // keep as-is (backend handles %)
    var severity = q.get("severity") || "";
    var temperature = q.get("temperature") || q.get("temp") || null;
    var humidity = q.get("humidity") || null;
    var rainfall = q.get("rainfall") || null;
    var location = q.get("location") || "";


    /* -----------------------------------------------------
       Validate inputs
    ----------------------------------------------------- */
    if (!problem) {
        showError(
            "Missing detection details",
            "No disease or pest was provided. Please return to the "
            + "detection page and try again."
        );
        return;
    }


    /* -----------------------------------------------------
       Call the management API
    ----------------------------------------------------- */
    var endpoint = (type === "pest")
        ? "/api/pest-management"
        : "/api/disease-management";

    var payload = {
        crop: crop,
        problem: problem,
        confidence: confidence,
        severity: severity,
        temperature: temperature,
        humidity: humidity,
        rainfall: rainfall,
        location: location
    };

    if (type === "pest") {
        payload.pest = problem;
        delete payload.problem;
    } else {
        payload.disease = problem;
        delete payload.problem;
    }

    var isPest = (type === "pest");

    fetch(endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
        .then(function (response) {
            return response.json()
                .then(function (data) {
                    return { ok: response.ok, data: data };
                });
        })
        .then(function (res) {
            if (!res.ok || !res.data.success) {
                throw new Error(
                    res.data.error || "Unable to load management guidance."
                );
            }
            render(res.data);
        })
        .catch(function (err) {
            showError("Unable to load guidance", err.message);
        });


    /* -----------------------------------------------------
       Render
    ----------------------------------------------------- */
    function render(d) {

        loadingState.classList.add("hidden");
        show(content);

        var confidenceLabel = (d.confidence && d.confidence.percent !== null)
            ? (d.confidence.percent + "%  ·  " + d.confidence.label)
            : (d.confidence ? d.confidence.label : "—");
        var severityLabel = (d.severity && d.severity.label)
            ? d.severity.label
            : "Could not be determined";
        var riskLabel = d.risk_level || "—";

        /* ---------- summary card ---------- */
        clearList(summaryCard);
        summaryCard.appendChild(summaryItem("Crop", d.crop || crop || "General"));
        summaryCard.appendChild(summaryItem(
            isPest ? "Pest" : "Problem",
            d.problem || problem
        ));
        summaryCard.appendChild(summaryItem("Confidence", confidenceLabel));
        summaryCard.appendChild(summaryItem("Severity", severityLabel));
        summaryCard.appendChild(summaryItem("Risk", riskLabel));

        /* ---------- risk banner ---------- */
        hide(riskBanner);
        var riskText = {
            HIGH: "High risk - immediate field inspection and appropriate management are recommended.",
            MEDIUM: "Medium risk - continue monitoring and follow the recommended preventive measures.",
            LOW: "Low risk - maintain routine monitoring."
        }[riskLabel];

        if (riskText) {
            riskBanner.className = "banner banner-risk-" + riskLabel.toLowerCase();
            riskBanner.innerHTML = "";
            var icon = document.createElement("div");
            icon.className = "banner-icon";
            icon.textContent = riskLabel === "HIGH" ? "🔴" : (riskLabel === "MEDIUM" ? "🟠" : "🟢");
            var txt = document.createElement("div");
            txt.textContent = riskText;
            riskBanner.appendChild(icon);
            riskBanner.appendChild(txt);
            show(riskBanner);
        }

        /* ---------- early stage banner ---------- */
        hide(earlyBanner);
        if (d.in_knowledge_base && d.early_stage) {
            earlyBanner.innerHTML = "";
            var eIcon = document.createElement("div");
            eIcon.className = "banner-icon";
            eIcon.textContent = "🟢";
            var eTxt = document.createElement("div");
            eTxt.textContent = "EARLY STAGE DETECTED - Early management may "
                + "help reduce further spread. Inspect nearby plants and "
                + "begin the recommended preventive measures.";
            earlyBanner.appendChild(eIcon);
            earlyBanner.appendChild(eTxt);
            show(earlyBanner);
        }

        /* ---------- not in knowledge base ---------- */
        if (!d.in_knowledge_base) {
            earlyBanner.innerHTML = "";
            var nIcon = document.createElement("div");
            nIcon.className = "banner-icon";
            nIcon.textContent = "ℹ️";
            var nTxt = document.createElement("div");
            nTxt.textContent = d.message;
            earlyBanner.appendChild(nIcon);
            earlyBanner.appendChild(nTxt);
            show(earlyBanner);
            hide(symptomsCard);
            hide(warningCard);
            hide(preventionCard);
            hide(managementCard);
            hide(controlCard);
            hide(chemicalCard);
            hide(monitoringCard);
            hide(safetyCard);
            hide(sourceCard);
            renderWeather(d, false);
            return;
        }

        /* ---------- symptoms / identification ---------- */
        if (isPest) {
            symptomsIcon.textContent = "🐛";
            symptomsTitle.textContent = "Identification";
            var ident = (d.identification || []).slice();

            if (d.damage_signs && d.damage_signs.length) {
                ident.push("Damage / Feeding signs:");
                d.damage_signs.forEach(function (x) { ident.push("  • " + x); });
            }
            addBulletList(symptomsList, ident);
            if (!ident.length) { hide(symptomsCard); }
        } else {
            symptomsIcon.textContent = "🔍";
            symptomsTitle.textContent = "Symptoms";
            var syms = (d.symptoms || []).slice();
            if (d.pathogen) {
                syms.unshift("Causal organism where known: " + d.pathogen);
            }
            addBulletList(symptomsList, syms);
            if (!syms.length) { hide(symptomsCard); }
        }

        /* ---------- early warning ---------- */
        if (d.early_warning && d.early_warning.length) {
            addBulletList(warningList, d.early_warning);
            show(warningCard);
        } else {
            hide(warningCard);
        }

        /* ---------- prevention ---------- */
        if (d.prevention && d.prevention.length) {
            addBulletList(preventionList, d.prevention);
            show(preventionCard);
        } else {
            hide(preventionCard);
        }

        /* ---------- what to do now ---------- */
        if (d.management && d.management.length) {
            addBulletList(managementList, d.management);
            show(managementCard);
        } else {
            hide(managementCard);
        }

        /* ---------- cultural / mechanical / biological ---------- */
        var hasControls = (d.cultural_control && d.cultural_control.length)
            || (d.mechanical_control && d.mechanical_control.length)
            || (d.biological_control && d.biological_control.length);
        if (hasControls) {
            controlBody.innerHTML = "";
            if (d.cultural_control && d.cultural_control.length) {
                subsection(controlBody, "Cultural", d.cultural_control);
            }
            if (d.mechanical_control && d.mechanical_control.length) {
                subsection(controlBody, "Mechanical", d.mechanical_control);
            }
            if (d.biological_control && d.biological_control.length) {
                subsection(controlBody, "Biological", d.biological_control);
            }
            show(controlCard);
        } else {
            hide(controlCard);
        }

        /* ---------- chemical / control options ---------- */
        chemicalBody.innerHTML = "";
        if (d.chemical_explanation) {
            var note = document.createElement("p");
            note.className = "section-note";
            note.textContent = "⚠️ " + d.chemical_explanation;
            chemicalBody.appendChild(note);
        }
        if (d.chemical_control && d.chemical_control.length) {
            addBodyList(chemicalBody, d.chemical_control);
        }
        if (d.chemical_control && d.chemical_control.length
            && d.chemical_explanation) {
            /* both shown; fine */
        }
        show(chemicalCard);

        /* ---------- weather ---------- */
        renderWeather(d, true);

        /* ---------- monitoring ---------- */
        if (d.monitoring && d.monitoring.length) {
            addBulletList(monitoringList, d.monitoring);
            show(monitoringCard);
        } else {
            hide(monitoringCard);
        }

        /* ---------- safety ---------- */
        if (d.safety_notes && d.safety_notes.length) {
            addBulletList(safetyList, d.safety_notes);
            show(safetyCard);
        } else {
            hide(safetyCard);
        }

        /* ---------- sources ---------- */
        clearList(sourceList);
        (d.sources || []).forEach(function (src) {
            if (src && src.title) {
                var li = document.createElement("li");
                li.textContent = "Source: " + src.title;
                sourceList.appendChild(li);
            }
        });
        if (sourceList.children.length) {
            show(sourceCard);
        } else {
            hide(sourceCard);
        }

        content.scrollIntoView({ behavior: "smooth", block: "start" });

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }


    function renderWeather(d, showCard) {
        if (!showCard) {
            hide(weatherCard);
            return;
        }
        weatherBody.innerHTML = "";

        var table = document.createElement("div");
        table.className = "summary-grid";

        if (temperature) {
            table.appendChild(summaryItem("Temperature", temperature + " °C"));
        }
        if (humidity) {
            table.appendChild(summaryItem("Humidity", humidity + " %"));
        }
        if (rainfall) {
            table.appendChild(summaryItem("Rainfall", rainfall + " mm"));
        }
        if (!table.children.length) {
            table.appendChild(summaryItem("Weather", "Not provided"));
        }

        if (d.weather_risk) {
            table.appendChild(
                summaryItem("Weather risk", d.weather_risk.level || "—")
            );
        }

        weatherBody.appendChild(table);

        if (d.weather_risk && d.weather_risk.explanation) {
            var exp = document.createElement("p");
            exp.style.cssText =
                "margin:16px 0 0;color:#40584a;font-size:13px;line-height:1.7;";
            exp.textContent = d.weather_risk.explanation;
            weatherBody.appendChild(exp);
        }

        if (d.weather_risk && d.weather_risk.factors
            && d.weather_risk.factors.length) {
            addBodyList(weatherBody, d.weather_risk.factors);
        }

        if (d.weather_risk && d.weather_risk.note) {
            var wnote = document.createElement("p");
            wnote.className = "section-note";
            wnote.textContent = d.weather_risk.note;
            weatherBody.appendChild(wnote);
        }

        show(weatherCard);
    }

})();
