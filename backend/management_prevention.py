# ============================================================
# AGRIMIND AI
# REAL PEST & DISEASE MANAGEMENT / PREVENTION
# ============================================================
#
# This module is a DATA-DRIVEN decision-support knowledge base.
# It is NOT a replacement for a qualified agricultural expert.
#
# KEY RULES FOLLOWED HERE:
#   - Recommendations are retrieved from a structured store by
#     matching crop + disease (or crop + pest). They are never
#     generated from the problem name with random AI text.
#   - Chemical control information is NEVER invented. Where
#     verified chemical guidance is not available, the module
#     returns an official safety message and points the farmer
#     to a local agronomist / product label.
#   - Confidence, severity and weather are treated as risk
#     indicators, NOT proof that a disease/pest is present.
#   - Unknown crop/problem combinations return an honest
#     "not available in the knowledge base" result.
#
# ============================================================

import re


# ------------------------------------------------------------------
# SAFETY / STANDARD MESSAGES
# ------------------------------------------------------------------

CHEMICAL_FALLBACK = (
    "Specific chemical control information is unavailable. "
    "Please consult your local agriculture officer/agronomist "
    "and follow the product label."
)

REGIONAL_NOTE = (
    "Regional approval could not be verified. "
    "Use only products registered for the identified crop and "
    "problem in your region and follow the product label."
)

GENERAL_SAFETY = [
    "This is an agricultural decision-support tool, not a substitute "
    "for a qualified agricultural expert.",
    "Follow official product labels and local agricultural "
    "recommendations.",
    "Wear appropriate protective equipment when handling any "
    "agricultural input.",
    "Observe the recommended pre-harvest interval for any product used.",
]

NO_RECORD_MESSAGE = (
    "Specific management information is not available for this "
    "crop/problem in the current knowledge base. "
    "Please confirm the identification with a qualified agricultural "
    "expert or local extension service before taking action."
)

SEVERITY_UNKNOWN = (
    "Severity could not be reliably determined from the image."
)


# ============================================================
# DISEASE KNOWLEDGE BASE
# ============================================================
#
# Key format: "<crop> - <disease>" (lowercase, normalized).
# chemical_control is intentionally left EMPTY so we never invent
# pesticide products, active ingredients or application doses.

DISEASE_DB = {

    # --------------------------------------------------------
    # TOMATO - EARLY BLIGHT
    # --------------------------------------------------------
    "tomato - early blight": {
        "type": "disease",
        "crop": "Tomato",
        "disease": "Early blight",
        "pathogen": "Alternaria solani (fungus)",
        "symptoms": [
            "Dark brown to black lesions on older leaves, often starting "
            "on the lower canopy.",
            "Lesions frequently show a distinctive target-like pattern of "
            "concentric rings.",
            "Yellowing (chlorosis) develops around the lesions.",
            "Older/lower leaves are typically affected first.",
        ],
        "early_warning": [
            "Small dark spots appear on lower/older leaves.",
            "A few lesions start with a slight yellow halo.",
            "Gradual yellowing of the lower foliage.",
        ],
        "severity_indicators": [
            "Lesions spreading up the plant toward newer growth.",
            "Many lesions merging and large areas of leaf tissue turning brown.",
            "Defoliation of lower leaves.",
        ],
        "favorable_conditions": [
            "Warm, humid weather with wet foliage.",
            "Alternating wet and dry periods.",
            "Frequent rain, dew or overhead irrigation that keeps leaves wet.",
        ],
        "prevention": [
            "Use healthy, certified seed and transplants.",
            "Maintain appropriate plant spacing to improve air circulation.",
            "Avoid prolonged leaf wetness; water at the base of the plant.",
            "Remove and dispose of infected plant debris.",
            "Practice suitable crop rotation.",
            "Mulch to reduce soil splash that can carry spores to leaves.",
        ],
        "cultural_control": [
            "Rotate away from tomato, potato and related solanaceous crops.",
            "Improve airflow through spacing and pruning.",
            "Irrigate at the base and early in the day so foliage dries.",
            "Maintain balanced plant nutrition for plant vigour.",
        ],
        "mechanical_control": [
            "Remove severely infected lower leaves where practical.",
            "Remove and destroy infected plant debris.",
            "Avoid working among plants while foliage is wet.",
        ],
        "biological_control": [
            "Conserve beneficial organisms that help suppress fungal "
            "disease pressure.",
            "Some bio-fungicide products for fungal leaf blights are "
            "registered in some regions; verify local approval and label.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout lower/older leaves at least weekly.",
            "Inspect after rain or periods of high humidity.",
            "Check nearby tomato and potato plants for spread.",
            "Record first appearance to guide timing of any action.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Confirm the problem before applying any treatment.",
        ],
        "source": "University of Minnesota Extension; Penn State Extension",
    },

    # --------------------------------------------------------
    # TOMATO - LATE BLIGHT
    # --------------------------------------------------------
    "tomato - late blight": {
        "type": "disease",
        "crop": "Tomato",
        "disease": "Late blight",
        "pathogen": "Phytophthora infestans (oomycete)",
        "symptoms": [
            "Large, water-soaked, grey-green to brown lesions on leaves.",
            "Lesions on stems and can lead to rapid browning and collapse.",
            "White mould-like growth may appear on the underside of infected "
            "leaves in humid conditions.",
            "Greasy brown lesions on green fruit.",
        ],
        "early_warning": [
            "Water-soaked leaf spots that enlarge quickly.",
            "Dark discoloration on lower leaves and stems, often in cool, wet "
            "weather.",
            "Rapidly spreading blight during extended cool, wet periods.",
        ],
        "severity_indicators": [
            "Rapid spread through the planting during wet weather.",
            "Extensive defoliation and stem collapse.",
            "Fruit infection and darkening.",
        ],
        "favorable_conditions": [
            "Cool, wet weather.",
            "High humidity and long periods of leaf wetness.",
            "Standing water and poor airflow.",
        ],
        "prevention": [
            "Use certified disease-free transplants and seed.",
            "Avoid overhead irrigation; water at the base.",
            "Provide adequate spacing and prune for airflow.",
            "Avoid planting in poorly drained or low-ventilation beds.",
            "Remove and destroy infected plants/piles of cull tubers.",
        ],
        "cultural_control": [
            "Rotate crops and remove volunteer tomato/potato plants.",
            "Plant in well-drained soil with good air movement.",
            "Keep foliage dry through base watering and morning irrigation.",
        ],
        "mechanical_control": [
            "Remove and destroy infected leaves or whole plants where "
            "practical.",
            "Manage potato cull piles and volunteer plants.",
            "Disinfect tools used on infected plants.",
        ],
        "biological_control": [
            "Late blight is hard to control biologically once established; "
            "some registered bio-products exist in certain regions. "
            "Verify local registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout frequently during cool, wet weather.",
            "Inspect undersides of leaves for white mould.",
            "Check plants near field edges and low spots.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Late blight spreads very quickly; act early and do not "
            "delay expert advice.",
        ],
        "source": "University of Minnesota Extension; Penn State Extension",
    },

    # --------------------------------------------------------
    # TOMATO - BACTERIAL SPOT
    # --------------------------------------------------------
    "tomato - bacterial spot": {
        "type": "disease",
        "crop": "Tomato",
        "disease": "Bacterial spot",
        "pathogen": "Xanthomonas spp. (bacteria)",
        "symptoms": [
            "Small, dark, water-soaked spots on leaves.",
            "Spotty yellowing around leaf lesions.",
            "Raised, scabby spots on fruit.",
            "Spots on stems and petioles in severe cases.",
        ],
        "early_warning": [
            "Small water-soaked specks on young leaves.",
            "Faint yellow halos around dark spots.",
        ],
        "severity_indicators": [
            "Spots merging and defoliation of lower leaves.",
            "Lesions developing on fruit.",
        ],
        "favorable_conditions": [
            "Warm, wet weather; spread by rain splash.",
            "Working among plants while foliage is wet.",
        ],
        "prevention": [
            "Use disease-free seed and transplants.",
            "Inspect transplants before planting.",
            "Maintain adequate spacing for airflow.",
            "Water at the base of plants.",
            "Avoid working among wet plants.",
            "Practice crop rotation.",
            "Use drip irrigation where practical.",
        ],
        "cultural_control": [
            "Rotate away from tomato and pepper.",
            "Water at base only; avoid overhead irrigation.",
            "Control volunteer solanaceous plants.",
        ],
        "mechanical_control": [
            "Remove symptomatic leaves where practical.",
            "Disinfect pruning/training tools.",
            "Remove crop debris after harvest.",
        ],
        "biological_control": [
            "Copper-based products can suppress bacterial spot in some "
            "regions; copper is a natural mineral, but verify local "
            "registration and label before use.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect leaves and fruit regularly.",
            "Check transplants and seedlings before planting.",
            "Monitor after heavy rain.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Use drip irrigation and avoid wet foliage when possible.",
        ],
        "source": "University of Minnesota Extension",
    },

    # --------------------------------------------------------
    # TOMATO - LEAF MOLD
    # --------------------------------------------------------
    "tomato - leaf mold": {
        "type": "disease",
        "crop": "Tomato",
        "disease": "Leaf mold",
        "pathogen": "Passalora fulva (fungus)",
        "symptoms": [
            "Pale yellow spots on the upper leaf surface.",
            "Olive-green to brown velvety mould on the underside of leaves.",
            "Infected leaves may turn yellow and drop.",
        ],
        "early_warning": [
            "Faint yellow patches on upper leaves.",
            "Slight fuzzy growth on leaf undersides.",
        ],
        "severity_indicators": [
            "Defoliation moving up the plant.",
            "Heavy sporulation (mouldy growth) on undersides.",
        ],
        "favorable_conditions": [
            "High humidity and low air movement, especially in greenhouses.",
            "Warm, moist conditions.",
        ],
        "prevention": [
            "Provide good air circulation and ventilation.",
            "Reduce humidity around foliage.",
            "Avoid overhead watering that keeps leaves wet.",
            "Use resistant varieties where available.",
        ],
        "cultural_control": [
            "Increase spacing and prune to open the canopy.",
            "Improve ventilation in greenhouses or tunnels.",
            "Avoid excessive nitrogen which promotes lush growth.",
        ],
        "mechanical_control": [
            "Remove severely affected lower leaves.",
            "Remove and destroy infected debris.",
        ],
        "biological_control": [
            "Some registered biofungicides for foliar disease exist; "
            "verify local registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Check undersides of leaves, especially in humid conditions.",
            "Inspect plants close together or in low-ventilation areas.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Agricultural IPM practice; Penn State Extension",
    },

    # --------------------------------------------------------
    # TOMATO - SEPTORIA LEAF SPOT
    # --------------------------------------------------------
    "tomato - septoria leaf spot": {
        "type": "disease",
        "crop": "Tomato",
        "disease": "Septoria leaf spot",
        "pathogen": "Septoria lycopersici (fungus)",
        "symptoms": [
            "Many small dark spots with lighter grey/tan centres on leaves.",
            "Spots may have dark, narrow margins.",
            "Infected lower leaves yellow and drop.",
        ],
        "early_warning": [
            "Small dark spots on lower/older leaves.",
            "Starts near the base of the plant.",
        ],
        "severity_indicators": [
            "Many spots covering the leaf surface.",
            "Progressive defoliation from the bottom up.",
        ],
        "favorable_conditions": [
            "Warm, wet weather; spread by rain splash.",
            "Poor air circulation and wet foliage.",
        ],
        "prevention": [
            "Practice crop rotation.",
            "Water at the base; keep foliage dry.",
            "Maintain adequate spacing.",
            "Remove and destroy infected debris.",
            "Remove lower leaves that touch the soil.",
        ],
        "cultural_control": [
            "Rotate crops.",
            "Mulch to reduce soil splash.",
            "Maintain plant nutrition and spacing.",
        ],
        "mechanical_control": [
            "Remove infected lower leaves and debris.",
            "Avoid working among wet plants.",
        ],
        "biological_control": [
            "Some biofungicides are registered for leaf spots in some "
            "regions; verify local registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout lower leaves weekly.",
            "Inspect after rain or heavy dew.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Agricultural IPM practice",
    },

    # --------------------------------------------------------
    # POTATO - EARLY BLIGHT
    # --------------------------------------------------------
    "potato - early blight": {
        "type": "disease",
        "crop": "Potato",
        "disease": "Early blight",
        "pathogen": "Alternaria solani (fungus)",
        "symptoms": [
            "Dark brown leaf spots with concentric target-like rings.",
            "Yellowing around the spots.",
            "Older/lower leaves affected first.",
        ],
        "early_warning": [
            "Small dark spots on lower leaves.",
            "Scattered lesions with faint yellow halos.",
        ],
        "severity_indicators": [
            "Lesions spreading to upper leaves.",
            "Defoliation beginning on lower parts of the plant.",
        ],
        "favorable_conditions": [
            "Warm, humid conditions with wet foliage.",
            "Alternating wet and dry periods.",
        ],
        "prevention": [
            "Practice crop rotation.",
            "Use healthy, certified seed potatoes.",
            "Manage crop residue.",
            "Maintain balanced nutrition and plant vigour.",
            "Water at the base and keep foliage dry where possible.",
        ],
        "cultural_control": [
            "Rotate away from potato, tomato and related crops.",
            "Maintain good plant spacing for airflow.",
            "Water to keep foliage dry.",
        ],
        "mechanical_control": [
            "Remove and destroy severely affected foliage where practical.",
            "Manage crop debris after harvest.",
        ],
        "biological_control": [
            "Some registered biofungicides for foliar blights exist in "
            "certain regions; verify local registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout lower leaves weekly.",
            "Inspect after warm, wet periods.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University of Minnesota Extension",
    },

    # --------------------------------------------------------
    # POTATO - LATE BLIGHT
    # --------------------------------------------------------
    "potato - late blight": {
        "type": "disease",
        "crop": "Potato",
        "disease": "Late blight",
        "pathogen": "Phytophthora infestans (oomycete)",
        "symptoms": [
            "Water-soaked dark lesions on leaves and stems.",
            "Rapid collapse and death of foliage during cool, wet weather.",
            "White mould on the underside of leaves in humid conditions.",
            "Brown, firm rot of tubers.",
        ],
        "early_warning": [
            "Water-soaked spots appearing quickly on lower leaves.",
            "Rapidly enlarging blotches during cool, wet weather.",
        ],
        "severity_indicators": [
            "Rapid spread through the field.",
            "Extensive defoliation and stem blackening.",
            "Tuber rot.",
        ],
        "favorable_conditions": [
            "Cool, wet weather and high humidity.",
            "Frequent rain and dew.",
        ],
        "prevention": [
            "Use certified disease-free seed potatoes.",
            "Avoid overhead irrigation; water at the base.",
            "Provide adequate spacing and good airflow.",
            "Scout regularly during cool, wet weather.",
            "Manage cull piles and volunteer plants.",
        ],
        "cultural_control": [
            "Rotate crops and remove volunteer plants.",
            "Plant in well-drained, open fields.",
            "Keep foliage as dry as possible.",
        ],
        "mechanical_control": [
            "Remove and destroy infected plants where practical.",
            "Manage potato cull piles.",
        ],
        "biological_control": [
            "Late blight is hard to control biologically once established; "
            "some registered bio-products exist in some regions. Verify "
            "local registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout frequently during cool, wet spells.",
            "Check low-lying and dense parts of the field first.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Late blight spreads quickly; act early and seek expert advice.",
        ],
        "source": "University of Minnesota Extension; Penn State Extension",
    },

    # --------------------------------------------------------
    # SQUASH - POWDERY MILDEW
    # --------------------------------------------------------
    "squash - powdery mildew": {
        "type": "disease",
        "crop": "Squash",
        "disease": "Powdery mildew",
        "pathogen": "Erysiphaceae spp. (fungus)",
        "symptoms": [
            "White, powdery fungal growth on the upper surface of leaves.",
            "Leaves may turn yellow, brown and die.",
            "Reduced plant vigour and yield.",
        ],
        "early_warning": [
            "Small white powdery patches on leaves.",
            "White speckling on the top of leaves.",
        ],
        "severity_indicators": [
            "Powdery growth covering large areas of the leaf.",
            "Leaves drying and curling.",
        ],
        "favorable_conditions": [
            "Warm days and cool nights.",
            "High humidity with dry leaf surfaces.",
            "Dense, shaded canopies.",
        ],
        "prevention": [
            "Use resistant varieties where available.",
            "Provide adequate spacing and airflow.",
            "Avoid excessively humid plant canopies.",
            "Use drip irrigation; keep foliage dry.",
        ],
        "cultural_control": [
            "Increase spacing for better air movement.",
            "Avoid overhead irrigation.",
            "Plant in full sun.",
        ],
        "mechanical_control": [
            "Remove and destroy severely infected leaves.",
            "Do not compost infected debris next to the crop.",
        ],
        "biological_control": [
            "Some registered biofungicides and horticultural products "
            "suppress powdery mildew in some regions; verify local "
            "registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect leaves regularly, especially in warm, humid weather.",
            "Check the underside and shaded parts of the canopy.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Agricultural IPM practice; Penn State Extension",
    },

    # --------------------------------------------------------
    # GRAPE - BLACK ROT
    # --------------------------------------------------------
    "grape - black rot": {
        "type": "disease",
        "crop": "Grape",
        "disease": "Black rot",
        "pathogen": "Guignardia bidwellii (fungus)",
        "symptoms": [
            "Brownish circular spots with dark margins on leaves.",
            "Dark, firm lesions that may shrivel on berries.",
            "Mummified shrivelled fruit.",
        ],
        "early_warning": [
            "Small brown spots on leaves and developing berries.",
            "Darkening of young berries.",
        ],
        "severity_indicators": [
            "Fruit shrivelling and mummifying.",
            "Rapid spread in wet, warm weather.",
        ],
        "favorable_conditions": [
            "Warm, wet weather during the growing season.",
            "High humidity around the canopy.",
        ],
        "prevention": [
            "Maintain good vineyard sanitation.",
            "Remove mummified fruit and infected debris.",
            "Improve canopy airflow through pruning.",
            "Monitor during warm, wet periods.",
        ],
        "cultural_control": [
            "Prune regularly to improve airflow and light penetration.",
            "Remove infected fruit and debris.",
            "Keep the canopy open.",
        ],
        "mechanical_control": [
            "Remove mummified berries from vines and ground.",
            "Trellis and canopy management to dry foliage.",
        ],
        "biological_control": [
            "Some registered biofungicides are available in some regions; "
            "verify local registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect developing fruit and leaves weekly.",
            "Monitor during warm, wet weather.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Agricultural IPM practice; Penn State Extension",
    },

    # --------------------------------------------------------
    # CORN - COMMON RUST
    # --------------------------------------------------------
    "corn - common rust": {
        "type": "disease",
        "crop": "Corn",
        "disease": "Common rust",
        "pathogen": "Puccinia sorghi (fungus)",
        "symptoms": [
            "Dark brown, cinnamon-coloured oval pustules on both leaf "
            "surfaces.",
            "Pustules may be surrounded by a light halo.",
            "Severe infection can cause yellowing and drying of leaves.",
        ],
        "early_warning": [
            "Small dark raised spots on leaves.",
            "Reddish-brown dust when pustules break open.",
        ],
        "severity_indicators": [
            "Many pustules across the leaves.",
            "Leaves drying from the top down.",
        ],
        "favorable_conditions": [
            "Cool, moist weather.",
            "High humidity early in the season.",
        ],
        "prevention": [
            "Use resistant hybrids where available.",
            "Maintain balanced plant nutrition.",
            "Monitor early in the season during cool, wet conditions.",
        ],
        "cultural_control": [
            "Choose tolerant hybrids.",
            "Maintain good plant vigour with balanced fertility.",
        ],
        "mechanical_control": [
            "No widely applicable mechanical control; early removal of "
            "severely infected plants where practical.",
        ],
        "biological_control": [],
        "chemical_control": [],
        "monitoring": [
            "Scout leaves weekly during early, cool wet periods.",
            "Look for pustules breaking open on the leaf surface.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Purdue University Extension",
    },

    # --------------------------------------------------------
    # CORN - GRAY LEAF SPOT
    # --------------------------------------------------------
    "corn - cercospora gray leaf spot": {
        "type": "disease",
        "crop": "Corn",
        "disease": "Cercospora gray leaf spot",
        "pathogen": "Cercospora zeae-maydis (fungus)",
        "symptoms": [
            "Long, narrow, rectangular lesions running parallel to leaf "
            "veins.",
            "Grey to tan lesions with dark margins.",
            "Lesions can merge and cause leaf blighting.",
        ],
        "early_warning": [
            "Small narrow spots on lower leaves.",
            "Lesions appearing first near the base of the plant.",
        ],
        "severity_indicators": [
            "Lesions spreading to upper leaves, especially near ears.",
            "Extensive leaf blighting.",
        ],
        "favorable_conditions": [
            "Warm, humid weather.",
            "Extended leaf wetness, especially no-till with residue.",
        ],
        "prevention": [
            "Use resistant hybrids.",
            "Manage crop residue through rotation or tillage.",
            "Maintain balanced nitrogen.",
            "Monitor in warm, humid conditions.",
        ],
        "cultural_control": [
            "Rotate crops to reduce residue-borne inoculum.",
            "Increase plant vigour with balanced fertility.",
        ],
        "mechanical_control": [
            "Manage crop residue to reduce overwintering spores.",
        ],
        "biological_control": [],
        "chemical_control": [],
        "monitoring": [
            "Scout lower leaves for lesions in warm, humid weather.",
            "Watch for lesions moving up to the upper leaves.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Purdue University Extension",
    },

    # --------------------------------------------------------
    # CORN - NORTHERN LEAF BLIGHT
    # --------------------------------------------------------
    "corn - northern leaf blight": {
        "type": "disease",
        "crop": "Corn",
        "disease": "Northern leaf blight",
        "pathogen": "Exserohilum turcicum (fungus)",
        "symptoms": [
            "Large, elongate, grey-green to tan lesions on leaves.",
            "Lesions may run in cigarette-shape between veins.",
            "Severe blighting can reduce grain fill.",
        ],
        "early_warning": [
            "Long spindle-shaped lesions on leaves.",
            "Lesions appearing first on lower leaves.",
        ],
        "severity_indicators": [
            "Lesions progressing to upper leaves near the ear.",
            "Extensive leaf blighting.",
        ],
        "favorable_conditions": [
            "Warm, humid conditions.",
            "Cloudy, wet weather.",
        ],
        "prevention": [
            "Use resistant hybrids.",
            "Manage crop residue.",
            "Maintain balanced fertility.",
            "Monitor in warm, humid weather.",
        ],
        "cultural_control": [
            "Rotate crops.",
            "Manage residue.",
            "Maintain balanced nutrition.",
        ],
        "mechanical_control": [
            "Manage crop residue to reduce inoculum.",
        ],
        "biological_control": [],
        "chemical_control": [],
        "monitoring": [
            "Scout leaves weekly under warm, humid conditions.",
            "Check for lesions on lower leaves first.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Purdue University Extension",
    },

    # --------------------------------------------------------
    # APPLE - SCAB
    # --------------------------------------------------------
    "apple - scab": {
        "type": "disease",
        "crop": "Apple",
        "disease": "Apple scab",
        "pathogen": "Venturia inaequalis (fungus)",
        "symptoms": [
            "Olive-green to black velvety spots on leaves.",
            "Dark scabby lesions on fruit.",
            "Distorted leaf growth and early leaf drop in severe cases.",
        ],
        "early_warning": [
            "Small olive-green spots on young leaves.",
            "Appearance of spots soon after wet spring weather.",
        ],
        "severity_indicators": [
            "Lesions on fruit.",
            "Irregular corky scab on the fruit surface.",
            "Defoliation.",
        ],
        "favorable_conditions": [
            "Cool, wet spring weather.",
            "Extended periods of leaf and shoot wetness.",
        ],
        "prevention": [
            "Use scab-resistant varieties where available.",
            "Rake and remove fallen leaves (a key overwintering source).",
            "Improve airflow through pruning.",
            "Monitor during the primary infection period in spring.",
        ],
        "cultural_control": [
            "Remove fallen leaves in autumn to reduce overwintering spores.",
            "Prune to open the canopy and improve drying.",
        ],
        "mechanical_control": [
            "Rake and destroy fallen leaves and infected prunings.",
        ],
        "biological_control": [],
        "chemical_control": [],
        "monitoring": [
            "Monitor temperature and leaf wetness to predict infection periods.",
            "Inspect leaves and fruit after rainy spring periods.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Penn State Extension",
    },

    # --------------------------------------------------------
    # PEACH - BACTERIAL SPOT
    # --------------------------------------------------------
    "peach - bacterial spot": {
        "type": "disease",
        "crop": "Peach",
        "disease": "Bacterial spot",
        "pathogen": "Xanthomonas arboricola pv. pruni (bacteria)",
        "symptoms": [
            "Small, angular, water-soaked spots on leaves.",
            "Shot-hole appearance as spots drop out.",
            "Dark, sunken lesions on fruit.",
        ],
        "early_warning": [
            "Small water-soaked spots on young leaves.",
            "Yellowing around leaf spots.",
        ],
        "severity_indicators": [
            "Defoliation in severe cases.",
            "Fruit lesions and reduced marketability.",
        ],
        "favorable_conditions": [
            "Warm, wet spring weather.",
            "Wind-driven rain spreading bacteria.",
        ],
        "prevention": [
            "Use disease-resistant or tolerant varieties.",
            "Maintain good airflow through pruning.",
            "Water management to reduce leaf wetness.",
            "Prune out infected twigs where practical.",
        ],
        "cultural_control": [
            "Choose tolerant varieties.",
            "Prune to improve airflow.",
            "Avoid overhead irrigation.",
        ],
        "mechanical_control": [
            "Prune and remove infected twigs and debris.",
        ],
        "biological_control": [
            "Copper-based products can suppress bacterial spot in some "
            "regions; verify local registration and label.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect young leaves and fruit during warm, wet weather.",
            "Check for leaf spots after wind-driven rain.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Agricultural IPM practice; Penn State Extension",
    },

    # --------------------------------------------------------
    # BELL PEPPER - BACTERIAL SPOT
    # --------------------------------------------------------
    "bell pepper - bacterial spot": {
        "type": "disease",
        "crop": "Bell pepper",
        "disease": "Bacterial spot",
        "pathogen": "Xanthomonas spp. (bacteria)",
        "symptoms": [
            "Small water-soaked spots on leaves.",
            "Raised, scabby spots on fruit.",
            "Spotty yellowing and leaf drop.",
        ],
        "early_warning": [
            "Small dark specks on young leaves.",
            "Brown spots on fruit.",
        ],
        "severity_indicators": [
            "Defoliation and fruit blemishing.",
            "Spots merging on fruit.",
        ],
        "favorable_conditions": [
            "Warm, wet weather; spread by rain splash.",
            "Working among wet plants.",
        ],
        "prevention": [
            "Use disease-free seed and transplants.",
            "Rotate crops.",
            "Water at the base; avoid wet foliage.",
            "Avoid working among wet plants.",
            "Maintain good spacing for airflow.",
        ],
        "cultural_control": [
            "Rotate away from pepper and tomato.",
            "Use drip irrigation.",
            "Avoid leaf wetting.",
        ],
        "mechanical_control": [
            "Remove symptomatic leaves where practical.",
            "Disinfect tools.",
        ],
        "biological_control": [
            "Copper-based products can suppress bacterial spot in some "
            "regions; verify local registration and label.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect leaves and fruit regularly.",
            "Check transplants before planting.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University of Minnesota Extension",
    },

    # --------------------------------------------------------
    # STRAWBERRY - LEAF SCORCH
    # --------------------------------------------------------
    "strawberry - leaf scorch": {
        "type": "disease",
        "crop": "Strawberry",
        "disease": "Leaf scorch",
        "pathogen": "Diplocarpon earlianum (fungus)",
        "symptoms": [
            "Purple to reddish-brown spots on leaves.",
            "Dark spots with lighter centres on leaflets.",
            "Leaves may dry and appear scorched in severe cases.",
        ],
        "early_warning": [
            "Small purple spots on leaf surfaces.",
            "Reddish discoloration on older leaves.",
        ],
        "severity_indicators": [
            "Many spots and leaf drying.",
            "Reduced plant vigour.",
        ],
        "favorable_conditions": [
            "Warm, wet or humid weather.",
            "Overhead irrigation and wet foliage.",
        ],
        "prevention": [
            "Use certified disease-free plants.",
            "Provide adequate spacing and airflow.",
            "Use drip irrigation; keep foliage dry.",
            "Remove and destroy infected debris.",
            "Rotate to clean beds.",
        ],
        "cultural_control": [
            "Maintain plant spacing.",
            "Avoid overhead irrigation.",
            "Remove old leaves through renovation.",
        ],
        "mechanical_control": [
            "Remove infected leaves and debris.",
            "Keep weed pressure low to improve airflow.",
        ],
        "biological_control": [
            "Some registered biofungicides exist in some regions; verify "
            "local registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect leaves regularly during warm, wet weather.",
            "Scout quickly after rain or overhead irrigation.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University of Minnesota Extension",
    },

    # --------------------------------------------------------
    # APPLE - BLACK ROT
    # --------------------------------------------------------
    "apple - black rot": {
        "type": "disease",
        "crop": "Apple",
        "disease": "Black rot",
        "pathogen": "Botryosphaeria obtusa (fungus)",
        "symptoms": [
            "Large, firm, brown circular spots on fruit that often "
            "expand into a bull's-eye pattern.",
            "Affected fruit may turn dark brown or black and shrivel into "
            "mummies.",
            "Rough, sunken cankers on branches and trunk.",
            "Purple-then-brown leaf spots (frogeye leaf spot).",
        ],
        "early_warning": [
            "Small brown spots appearing on fruit near harvest.",
            "Dead or dying branch wood (cankers) creating inoculum.",
            "Mummified fruit left on the tree or ground.",
        ],
        "severity_indicators": [
            "Rapid expansion of fruit rot during warm, humid weather.",
            "Multiple cankers girdling a limb.",
        ],
        "favorable_conditions": [
            "Warm, wet weather in spring and near harvest.",
            "Poor air circulation in a dense canopy.",
            "Heavy rain splashing spores onto fruit.",
        ],
        "prevention": [
            "Prune out cankers and remove mummified fruit and dead wood.",
            "Maintain an open canopy to speed drying.",
            "Rake and remove fallen fruit and debris in autumn.",
            "Follow regional orchard sanitation practices.",
        ],
        "cultural_control": [
            "Prune to improve airflow and sunlight penetration.",
            "Avoid wounding trees during pruning.",
            "Remove alternate hosts and infected wood.",
        ],
        "mechanical_control": [
            "Pick off and destroy infected fruit (do not leave on ground).",
            "Disinfect pruning tools between cuts on affected wood.",
        ],
        "biological_control": [
            "Maintain good orchard hygiene to limit overwintering inoculum.",
            "Conserve beneficial organisms that suppress fungal decay in "
            "some systems; verify local practice.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout for cankers and mummified fruit during pruning.",
            "Inspect fruit regularly during warm, wet periods.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Penn State Extension; West Virginia University Extension",
    },

    # --------------------------------------------------------
    # APPLE - CEDAR APPLE RUST
    # --------------------------------------------------------
    "apple - cedar apple rust": {
        "type": "disease",
        "crop": "Apple",
        "disease": "Cedar apple rust",
        "pathogen": "Gymnosporangium juniperi-virginianae (fungus)",
        "symptoms": [
            "Bright orange to yellow spots on the upper leaf surface.",
            "Small dark dots (pustules) appear within the orange spots.",
            "Spots may enlarge and the leaf may yellow and drop.",
            "Lesions can also appear on fruit and young shoots.",
        ],
        "early_warning": [
            "First orange spots appearing on young leaves in spring.",
            "Orange, gelatinous galls on nearby cedar/juniper trees.",
        ],
        "severity_indicators": [
            "Numerous leaf spots and premature leaf drop.",
            "Fruit scarring reducing market quality.",
        ],
        "favorable_conditions": [
            "Wet spring weather and the presence of cedar/juniper near "
            "the orchard (alternate host).",
            "Spores released during rain in spring.",
        ],
        "prevention": [
            "Avoid planting apple near cedars/junipers, or remove nearby "
            "cedar galls.",
            "Select less-susceptible apple varieties where available.",
            "Maintain an open canopy.",
        ],
        "cultural_control": [
            "Manage the alternate host (cedar/juniper) distance.",
            "Remove galls from nearby cedar trees where feasible.",
            "Keep the orchard well-ventilated.",
        ],
        "mechanical_control": [
            "Remove and destroy heavily infected leaves where practical.",
        ],
        "biological_control": [
            "No effective biological control is widely established; rely "
            "on host resistance and sanitation.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout young leaves from bud break through early summer.",
            "Watch for orange spots after spring rains.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Penn State Extension; University of Minnesota Extension",
    },

    # --------------------------------------------------------
    # CHERRY - POWDERY MILDEW
    # --------------------------------------------------------
    "cherry - powdery mildew": {
        "type": "disease",
        "crop": "Cherry",
        "disease": "Powdery mildew",
        "pathogen": "Podosphaera clandestina (fungus)",
        "symptoms": [
            "White, powdery fungal growth on young leaves and shoots.",
            "Leaves may become distorted, curled or stunted.",
            "Mildew patches may darken or dry out.",
        ],
        "early_warning": [
            "Faint white fungal patches on the newest leaves.",
            "Slight leaf curling or cupping on shoot tips.",
        ],
        "severity_indicators": [
            "White growth spreading across the canopy.",
            "Shoot and leaf distortion reducing fruit quality.",
        ],
        "favorable_conditions": [
            "Moderate humidity and warm days with cool nights.",
            "Dense, shaded canopy.",
        ],
        "prevention": [
            "Plant in full sun with good airflow.",
            "Prune to open the canopy.",
            "Avoid excess nitrogen that promotes soft growth.",
            "Remove and destroy heavily infected shoots in dormant season.",
        ],
        "cultural_control": [
            "Space trees to allow airflow.",
            "Water at the base and avoid wetting foliage.",
            "Maintain balanced fertility.",
        ],
        "mechanical_control": [
            "Prune out infected shoot tips.",
            "Trim to improve light penetration.",
        ],
        "biological_control": [
            "Some bio-fungicides are registered for powdery mildew in "
            "select regions; verify local approval.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Repeat scouting of young growth during warm, humid weather.",
            "Check cultivar differences in susceptibility.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Washington State University Extension; University of Minnesota Extension",
    },

    # --------------------------------------------------------
    # GRAPE - ESCA (BLACK MEASLES)
    # --------------------------------------------------------
    "grape - esca (black measles)": {
        "type": "disease",
        "crop": "Grape",
        "disease": "Esca (black measles)",
        "pathogen": "Complex of wood-colonising fungi (e.g. Phaeoacremonium, "
                    "Fomitiporia)",
        "symptoms": [
            "Tiger-stripe pattern: interveinal chlorosis (yellowing strips) "
            "on older leaves.",
            "Shoot and trunk canker, sometimes with internal wood rot.",
            "Small, dark spots ('black measles') on berry skin.",
            "Sudden wilting and death of a shoot or leaf cluster in severe "
            "cases.",
        ],
        "early_warning": [
            "Interveinal yellow stripes appearing on mid-season leaves.",
            "Patchy ripening or shrivelling of berries.",
        ],
        "severity_indicators": [
            "Progressive decline of the vine over seasons.",
            "Whole-shoot dieback.",
        ],
        "favorable_conditions": [
            "Stress from heat and drought.",
            "Older vines with large pruning wounds.",
            "Wet conditions favouring infection.",
        ],
        "prevention": [
            "Use clean, certified planting material.",
            "Minimise large pruning wounds and protect them from infection.",
            "Promote vine vigour and avoid excessive stress.",
            "Remove and replant severely declining vines.",
        ],
        "cultural_control": [
            "Avoid unnecessary wounding during pruning.",
            "Maintain balanced crop load to reduce stress.",
            "Ensure good drainage and irrigation management.",
        ],
        "mechanical_control": [
            "Prune out and destroy visibly infected wood where practical.",
            "Rogue out dying vines.",
        ],
        "biological_control": [
            "Trunk-disease management relies on wound prevention and "
                    "sanitation more than on biological control; no reliable "
                    "bio-based cure is established.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect leaves for the tiger-stripe symptom from mid-season.",
            "Flag declining vines for removal and replanting.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University of California Agriculture & Natural Resources; "
                  "Cornell University",
    },

    # --------------------------------------------------------
    # GRAPE - LEAF BLIGHT (ISARIOPSIS LEAF SPOT)
    # --------------------------------------------------------
    "grape - leaf blight (isariopsis leaf spot)": {
        "type": "disease",
        "crop": "Grape",
        "disease": "Leaf blight (Isariopsis leaf spot)",
        "pathogen": "Pseudocercospora vitis (fungus)",
        "symptoms": [
            "Angular dark-brown to black spots on leaves.",
            "Spots may enlarge and coalesce, causing blighting.",
            "Premature leaf drop affecting sugar accumulation.",
            "Berries may show dark mottled discoloration.",
        ],
        "early_warning": [
            "Small angular dark spots on older leaves in late summer.",
            "Browning at leaf margins.",
        ],
        "severity_indicators": [
            "Rapid spread and heavy leaf blight.",
            "Significant premature defoliation.",
        ],
        "favorable_conditions": [
            "Warm, wet weather, especially late season.",
            "Dense canopy and vine crowding.",
        ],
        "prevention": [
            "Improve canopy airflow by pruning and shoot thinning.",
            "Maintain balanced nitrogen to avoid excess foliage.",
            "Remove and destroy infected leaf litter in autumn.",
        ],
        "cultural_control": [
            "Open the canopy to speed leaf drying.",
            "Avoid overhead irrigation late in the season.",
        ],
        "mechanical_control": [
            "Clean up and compost/remove fallen infected leaves.",
        ],
        "biological_control": [
            "Some bio-fungicide options exist in some regions; verify "
            "local registration and label.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout lower leaves from mid-to-late season.",
            "Inspect after extended wet periods.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University of California Agriculture & Natural Resources; "
                  "Penn State Extension",
    },

    # --------------------------------------------------------
    # ORANGE - HUANGLONGBING (CITRUS GREENING)
    # --------------------------------------------------------
    "orange - huanglongbing (citrus greening)": {
        "type": "disease",
        "crop": "Orange",
        "disease": "Huanglongbing (citrus greening)",
        "pathogen": "Candidatus Liberibacter asiaticus, transmitted by the "
                    "Asian citrus psyllid",
        "symptoms": [
            "Blotchy, asymmetric leaf mottling (yellow patches).",
            "Yellowing of one shoot or of the whole canopy.",
            "Small, lopsided, green-tinged fruit that fails to color fully.",
            "Bitter, off-flavour fruit.",
        ],
        "early_warning": [
            "A single branch showing blotchy mottle and yellow shoots.",
            "Presence of Asian citrus psyllid adults or nymphs.",
        ],
        "severity_indicators": [
            "Fruit drop and small, misshapen fruit.",
            "Tree decline and dieback over time.",
        ],
        "favorable_conditions": [
            "Presence and activity of the Asian citrus psyllid.",
            "Movement of infested nursery material.",
        ],
        "prevention": [
            "Source trees only from certified, psyllid-free nurseries.",
            "Monitor and manage Asian citrus psyllid populations.",
            "Remove infected trees; this is a regulated disease in many "
            "regions.",
            "Follow local regulatory requirements and report findings.",
        ],
        "cultural_control": [
            "Maintain a psyllid-free environment around commercial groves.",
            "Use only certified disease-free planting stock.",
            "Avoid moving plant material between regions.",
        ],
        "mechanical_control": [
            "Remove and destroy visibly infected trees to slow spread.",
        ],
        "biological_control": [
            "Conserve natural enemies of the Asian citrus psyllid such as "
                    "parasitoids (e.g. Tamarixia) where available.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Regular scouting for the psyllid and for blotchy mottle.",
            "Use sticky/trap monitoring for psyllid adults.",
            "Report suspected infections to the local agricultural office.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Huanglongbing is a regulatory disease in many regions; "
            "contact your local agriculture office before action.",
        ],
        "source": "University of Florida IFAS; Texas A&M AgriLife; USDA",
    },

    # --------------------------------------------------------
    # TOMATO - TARGET SPOT
    # --------------------------------------------------------
    "tomato - target spot": {
        "type": "disease",
        "crop": "Tomato",
        "disease": "Target spot",
        "pathogen": "Corynespora cassiicola (fungus)",
        "symptoms": [
            "Small, dark spots on leaves that enlarge into rings with a "
            "light center (target-like).",
            "Spots on petioles, stems and fruit.",
            "Yellowing around leaf lesions.",
        ],
        "early_warning": [
            "Small, water-soaked dark dots on older leaves.",
            "Browning at leaf edges.",
        ],
        "severity_indicators": [
            "Lesions spreading up the plant and onto fruit.",
            "Leaf blighting and defoliation.",
        ],
        "favorable_conditions": [
            "Warm, humid weather with wet foliage.",
            "Frequent rain, dew or overhead irrigation.",
        ],
        "prevention": [
            "Use clean seed and disease-free transplants.",
            "Improve airflow through spacing and pruning.",
            "Water at the base and allow foliage to dry.",
            "Remove and destroy infected plant debris.",
            "Practice crop rotation.",
        ],
        "cultural_control": [
            "Rotate away from tomato and related crops.",
            "Improve airflow and avoid prolonged leaf wetness.",
        ],
        "mechanical_control": [
            "Remove severely infected leaves and debris.",
        ],
        "biological_control": [
            "Some bio-fungicide products are registered in some regions; "
            "verify local approval and label.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout lower foliage at least weekly.",
            "Inspect after rainy or humid periods.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University of Florida IFAS; North Carolina State University",
    },

    # --------------------------------------------------------
    # TOMATO - TOMATO YELLOW LEAF CURL VIRUS
    # --------------------------------------------------------
    "tomato - tomato yellow leaf curl virus": {
        "type": "disease",
        "crop": "Tomato",
        "disease": "Tomato yellow leaf curl virus",
        "pathogen": "Tomato yellow leaf curl virus (TYLCV, begomovirus), "
                    "transmitted by the whitefly",
        "symptoms": [
            "Yellowing and upward curling of leaf margins.",
            "Marked stunting of the whole plant.",
            "Reduced and misshapen flowers, poor fruit set.",
        ],
        "early_warning": [
            "Initial mild yellowing and slight upward leaf cupping at "
            "the growing point.",
            "Presence of whiteflies on the underside of leaves.",
        ],
        "severity_indicators": [
            "Severe stunting and lack of flowering.",
            "Very low or no fruit yield.",
        ],
        "favorable_conditions": [
            "High whitefly populations and warm conditions.",
            "Nearby infected tomato or weed reservoirs.",
        ],
        "prevention": [
            "Use certified virus- and whitefly-free transplants.",
            "Manage whiteflies with appropriate methods and netting.",
            "Remove infected plants and weed reservoirs.",
            "Install reflective mulches or row covers where practical.",
        ],
        "cultural_control": [
            "Avoid planting near infected crops.",
            "Maintain plant vigour; remove infected plants promptly.",
        ],
        "mechanical_control": [
            "Rogue out (remove) infected plants.",
            "Use insect-exclusion netting in high-risk areas.",
        ],
        "biological_control": [
            "Conserve natural enemies of whitefly (e.g. parasitoids, "
            "lacewings) where available.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Monitor whiteflies with sticky traps.",
            "Inspect new transplants for early symptoms.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University of Florida IFAS; Texas A&M AgriLife",
    },

    # --------------------------------------------------------
    # TOMATO - TOMATO MOSAIC VIRUS
    # --------------------------------------------------------
    "tomato - tomato mosaic virus": {
        "type": "disease",
        "crop": "Tomato",
        "disease": "Tomato mosaic virus",
        "pathogen": "Tomato mosaic virus (ToMV, tobamovirus)",
        "symptoms": [
            "Light and dark green mosaic / mottling on leaves.",
            "Leaf distortion, puckering or fern-like (shoestring) leaves.",
            "Reduced plant growth and atypical fruit set.",
        ],
        "early_warning": [
            "Mottled colour pattern on the youngest leaves.",
            "Slight leaf puckering near the growing point.",
        ],
        "severity_indicators": [
            "Severe mosaic and stunting across many plants.",
            "Poor fruit set and reduced yield.",
        ],
        "favorable_conditions": [
            "Mechanical spread via contaminated seed, tools, hands "
            "or plant sap.",
            "Close plant contact and frequent handling.",
        ],
        "prevention": [
            "Use certified virus-free seed and transplants.",
            "Do not smoke or use tobacco products near plants (tobamovirus "
            "reservoir).",
            "Sanitise hands and tools between plant batches.",
            "Remove infected plants promptly to reduce spread.",
        ],
        "cultural_control": [
            "Use clean seed and transplants.",
            "Wash hands and tools; avoid working with wet plants.",
        ],
        "mechanical_control": [
            "Remove and destroy infected plants safely (do not compost).",
            "Disinfect benches, tools and equipment.",
        ],
        "biological_control": [
            "Viral diseases have no direct biological control; rely on "
            "clean seed, sanitation and resistance.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect seedlings and growing points for mottling.",
            "Check source seed lot health.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Cornell University; University of Florida IFAS",
    },

    # --------------------------------------------------------
    # TOMATO - SPIDER MITES
    # --------------------------------------------------------
    "tomato - spider mites": {
        "type": "disease",
        "crop": "Tomato",
        "disease": "Spider mites (two-spotted)",
        "pathogen": "Two-spotted spider mite (Tetranychus urticae) - a pest",
        "symptoms": [
            "Fine stippling (pale speckling) on the upper leaf surface.",
            "Yellowing and bronzing of leaves.",
            "Fine silken webbing between leaves and stems.",
            "Leaves may dry and drop under heavy infestation.",
        ],
        "early_warning": [
            "Tiny pale dots appearing on the top of leaves.",
            "Faint webbing at leaf axils.",
        ],
        "severity_indicators": [
            "Rapid bronzing and defoliation.",
            "Webbing across much of the plant.",
        ],
        "favorable_conditions": [
            "Hot, dry, dusty conditions.",
            "Plants under water stress.",
        ],
        "prevention": [
            "Maintain adequate irrigation to avoid plant stress.",
            "Avoid dusty conditions and flowering weeds near the crop.",
            "Inspect seedlings before transplanting.",
            "Reduce broad-spectrum pesticide use that disrupts natural "
            "enemies.",
        ],
        "cultural_control": [
            "Maintain good plant hydration and mulch to retain moisture.",
            "Reduce dust (the mites flourish under dusty, dry conditions).",
        ],
        "mechanical_control": [
            "Knock mites off with a strong stream of water.",
            "Remove and destroy heavily infested plant parts.",
        ],
        "biological_control": [
            "Conserve and protect natural enemies such as predatory "
            "mites (e.g. Phytoseiulus) and lady beetles.",
            "Avoid pesticides that harm these predators.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Tap leaves over white paper and check for tiny moving specks.",
            "Scout the underside of leaves for adult mites, eggs and webbing.",
            "Pay most attention during hot, dry weather.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Mites are not insects; some general insecticides are "
            "ineffective and can worsen outbreaks by killing predators.",
        ],
        "source": "University of Minnesota Extension; UC IPM",
    },
}


# ============================================================
# PEST KNOWLEDGE BASE
# ============================================================
#
# Key format: "<crop> - <pest>" (lowercase, normalized).
# chemical_control is intentionally left EMPTY so we never invent
# insecticides or application doses.

PEST_DB = {

    # --------------------------------------------------------
    # TOMATO - APHID
    # --------------------------------------------------------
    "tomato - aphid": {
        "type": "pest",
        "crop": "Tomato",
        "pest": "Aphid",
        "pest_type": "Sucking insect (Hemiptera)",
        "identification": [
            "Small, soft-bodied insects often found in clusters on the "
            "underside of leaves and on new shoots.",
            "Usually green, but can be yellow, black or reddish.",
            "May be covered with a white waxy, powdery coating.",
            "Present together with shiny, sticky honeydew and often ants.",
        ],
        "damage_signs": [
            "Curling, yellowing or stunting of new growth.",
            "Sticky honeydew on leaves and fruit.",
            "Sooty mould (black fungal growth) on honeydew.",
            "Deformed or distorted young leaves.",
        ],
        "early_warning": [
            "A few winged or wingless aphids on the underside of young "
            "leaves.",
            "Slight leaf curling on new growth.",
            "First appearance of ants on plants.",
        ],
        "severity_info": (
            "A heavy build-up on the undersides of leaves can weaken the "
            "plant, and aphids can transmit plant viruses. Acting early "
            "greatly reduces harm."
        ),
        "prevention": [
            "Encourage natural enemies (ladybugs, lacewings, parasitic "
            "wasps) by avoiding broad-spectrum insecticides.",
            "Avoid excess nitrogen which produces soft, attractive new "
            "growth.",
            "Use reflective mulch where practical to deter winged aphids.",
            "Inspect transplants before planting.",
        ],
        "cultural_control": [
            "Use balanced fertilization to avoid lush, soft growth.",
            "Remove weeds around the crop that may host aphids.",
            "Use row covers where appropriate where this fits the season.",
        ],
        "mechanical_control": [
            "Wash aphids off with a strong stream of water.",
            "Hand removal or use of sticky traps to monitor flight.",
            "Prune or remove heavily infested shoot tips.",
        ],
        "biological_control": [
            "Conserve and release natural enemies (ladybeetles, lacewings, "
            "parasitic wasps, predatory midges).",
            "Insecticidal soaps and horticultural oils can suppress "
            "aphids; verify local registration and label.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect the underside of young leaves and new shoots weekly.",
            "Watch for ants, which indicate honeydew-producing pests.",
            "Use yellow sticky traps to detect winged aphids.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Avoid broad-spectrum insecticides that harm natural enemies.",
        ],
        "source": "University of California Statewide IPM Program (UC IPM)",
    },

    # --------------------------------------------------------
    # TOMATO - WHITEFLY
    # --------------------------------------------------------
    "tomato - whitefly": {
        "type": "pest",
        "crop": "Tomato",
        "pest": "Whitefly",
        "pest_type": "Sucking insect (Hemiptera)",
        "identification": [
            "Tiny, white winged insects that fly up when the plant is "
            "disturbed.",
            "Adults are dusted with white wax.",
            "Larvae are small, flat, translucent scale-like forms on leaf "
            "undersides.",
        ],
        "damage_signs": [
            "Yellowing, stunting and leaf drop.",
            "Honeydew leading to sticky leaves and sooty mould.",
            "Transmission of plant viruses.",
        ],
        "early_warning": [
            "A sudden flight of small white insects when touching plants.",
            "Sticky spots on upper leaves.",
        ],
        "severity_info": (
            "High populations can seriously weaken plants and spread "
            "viruses. Early detection and action are important."
        ),
        "prevention": [
            "Inspect transplants thoroughly before planting.",
            "Use yellow sticky traps to monitor.",
            "Encourage predators and parasitoids.",
            "Avoid over-fertilization that produces attractive growth.",
            "Screen greenhouses and vents where applicable.",
        ],
        "cultural_control": [
            "Remove heavily infested plants and weeds.",
            "Maintain balanced nutrition.",
            "Avoid moving infested material between areas.",
        ],
        "mechanical_control": [
            "Use yellow sticky traps to monitor and reduce adult flight.",
            "Vacuuming has been used in enclosed production; do not rely "
            "on it alone.",
        ],
        "biological_control": [
            "Conserve and release natural enemies (predatory mites, "
            "parasitoid wasps, lacewings).",
            "Insecticidal soaps and oils can suppress young stages; verify "
            "local registration and label.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Use yellow sticky cards placed just above the canopy.",
            "Inspect undersides of leaves for nymphs.",
            "Check transplants before and after planting.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Avoid broad-spectrum insecticides that harm biological "
            "control agents.",
        ],
        "source": "University of California Statewide IPM Program (UC IPM)",
    },

    # --------------------------------------------------------
    # TOMATO - THRIPS
    # --------------------------------------------------------
    "tomato - thrips": {
        "type": "pest",
        "crop": "Tomato",
        "pest": "Thrips",
        "pest_type": "Sucking insect (Thysanoptera)",
        "identification": [
            "Very small, slender, elongated insects.",
            "Adults may be yellow, brown or black with narrow fringed "
            "wings.",
            "Often found in flowers and on the undersides of leaves.",
        ],
        "damage_signs": [
            "Silvery or bronzed streaks on leaves.",
            "Distorted and damaged young leaves and fruit.",
            "White or black specks (excrement) on leaves.",
        ],
        "early_warning": [
            "Silvery patches on leaves.",
            "Presence of thrips in flower buds.",
        ],
        "severity_info": (
            "Thrips damage tender growth and may transmit plant viruses. "
            "Monitor flowers and young leaves closely."
        ),
        "prevention": [
            "Inspect transplants before planting.",
            "Use blue or yellow sticky traps to monitor.",
            "Remove weeds that serve as alternate hosts.",
            "Encourage natural enemies (predatory mites, minute pirate "
            "bugs).",
        ],
        "cultural_control": [
            "Remove weedy alternate hosts around the crop.",
            "Maintain plant vigour.",
            "Avoid excessive nitrogen.",
        ],
        "mechanical_control": [
            "Use blue/yellow sticky cards to monitor and reduce adults.",
            "Bag and remove heavily infested plant parts.",
        ],
        "biological_control": [
            "Conserve and release predatory mites and minute pirate bugs.",
            "Some botanical/soap products can suppress thrips; verify local "
            "registration and label.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Place blue sticky cards near flowers and young leaves.",
            "Tap flowers over a white surface to detect adults.",
            "Inspect transplants and early-season growth.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Thrips can become resistant; rely on monitoring and "
            "biological control.",
        ],
        "source": "University of California Statewide IPM Program (UC IPM)",
    },

    # --------------------------------------------------------
    # TOMATO - TWO-SPOTTED SPIDER MITE
    # --------------------------------------------------------
    "tomato - spider mite": {
        "type": "pest",
        "crop": "Tomato",
        "pest": "Two-spotted spider mite",
        "pest_type": "Mite (Acari)",
        "identification": [
            "Tiny (about the size of a pepper grain) mites, often with two "
            "dark spots on the body.",
            "Fine webbing (silk) on the underside of leaves.",
            "Mites cluster on the undersides of leaves.",
        ],
        "damage_signs": [
            "Stippled, pale or silvery dotted leaves.",
            "Yellowing and bronzing of leaves.",
            "Fine webbing between leaves and stems.",
            "Leaf drop in severe outbreaks.",
        ],
        "early_warning": [
            "Fine speckling on the upper leaf surface.",
            "Tiny webbing near leaf veins.",
        ],
        "severity_info": (
            "Spider mites multiply quickly in hot, dry conditions. "
            "Early detection and management are important."
        ),
        "prevention": [
            "Avoid water stress; maintain adequate irrigation.",
            "Avoid dusty conditions which favour mites.",
            "Conserve natural predators (predatory mites, ladybugs).",
            "Inspect undersides of leaves regularly.",
        ],
        "cultural_control": [
            "Maintain good irrigation to reduce plant stress.",
            "Reduce dust and keep plants well-spaced.",
        ],
        "mechanical_control": [
            "Wash foliage with a stream of water to dislodge mites and "
            "webbing.",
            "Remove heavily infested leaves.",
        ],
        "biological_control": [
            "Conserve and release predatory mites (e.g. Phytoseiulus "
            "persimilis).",
            "Insecticidal soaps and horticultural oils can suppress mites; "
            "verify local registration and label.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect the undersides of leaves for mites, eggs and webbing.",
            "Watch for stippling on upper leaves.",
            "Monitor during hot, dry weather.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Spider mites are often a secondary problem triggered by "
            "broad-spectrum insecticide use.",
        ],
        "source": "University of California Statewide IPM Program (UC IPM)",
    },

    # --------------------------------------------------------
    # RICE - BROWN PLANTHOPPER
    # --------------------------------------------------------
    "rice - brown plant hopper": {
        "type": "pest",
        "crop": "Rice",
        "pest": "Brown planthopper",
        "pest_type": "Sucking insect (Hemiptera)",
        "identification": [
            "Small, brown, winged planthoppers found at the base of rice "
            "plants near the water line.",
            "Adults jump when disturbed.",
            "Nymphs are pale and wingless, clustered near the stem base.",
        ],
        "damage_signs": [
            "Yellowing and drying of plants (hopperburn) in patches.",
            "Heavy honeydew and sooty mould near the stem base.",
            "Plants lodging or dying in circular patches.",
        ],
        "early_warning": [
            "Adults/nymphs at the base of tillers.",
            "Honeydew on stems and soil surface.",
            "Small patches of plants yellowing.",
        ],
        "severity_info": (
            "Planthoppers can multiply very quickly in warm, humid "
            "conditions and cause hopperburn. Early action is essential."
        ),
        "prevention": [
            "Avoid excessive nitrogen that produces lush, attractive growth.",
            "Maintain optimum plant spacing and drainage.",
            "Conserve natural enemies (spiders, mirid bugs, dryinid wasps).",
            "Monitor regularly, especially during warm, humid weather.",
        ],
        "cultural_control": [
            "Use balanced (not excess) nitrogen fertilisation.",
            "Keep the field well drained and avoid standing water.",
            "Avoid close and dense planting.",
        ],
        "mechanical_control": [
            "Use light traps / yellow sticky traps to monitor adults.",
            "Remove heavily infested plants where practical.",
        ],
        "biological_control": [
            "Conserve and encourage natural enemies (spiders, predatory "
            "bugs, parasitic wasps).",
            "Avoid broad-spectrum insecticides that kill natural enemies.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect the base of plants for adults and nymphs weekly.",
            "Look for honeydew and sooty mould.",
            "Watch for small patches of yellowing plants.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Avoid broad-spectrum insecticides that harm natural enemies.",
        ],
        "source": "International Rice Research Institute (IRRI); "
                 "State agricultural university IPM extension",
    },

    # --------------------------------------------------------
    # RICE - WHITE BACKED PLANTHOPPER
    # --------------------------------------------------------
    "rice - white backed plant hopper": {
        "type": "pest",
        "crop": "Rice",
        "pest": "White-backed planthopper",
        "pest_type": "Sucking insect (Hemiptera)",
        "identification": [
            "Small planthoppers with pale, whitish wings/body.",
            "Found near the base of rice stems.",
            "Nymphs are pale and cluster near the stem base.",
        ],
        "damage_signs": [
            "Yellowing and drying of leaves in patches.",
            "Honeydew and sooty mould on stems.",
            "Hopperburn patches that spread.",
        ],
        "early_warning": [
            "Adults at the base of the plant.",
            "Honeydew and black sooty mould near stems.",
        ],
        "severity_info": (
            "Can cause rapid hopperburn injury. Monitor early and support "
            "natural enemies."
        ),
        "prevention": [
            "Use balanced fertilisation (avoid excess nitrogen).",
            "Maintain proper spacing and drainage.",
            "Conserve natural enemies.",
            "Monitor regularly during warm, humid weather.",
        ],
        "cultural_control": [
            "Balanced nitrogen, good drainage, moderate spacing.",
            "Avoid standing water when possible.",
        ],
        "mechanical_control": [
            "Yellow sticky traps / light traps to monitor adults.",
        ],
        "biological_control": [
            "Conserve spiders, predatory bugs and wasps.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect stem bases weekly.",
            "Watch for honeydew and sooty mould.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "International Rice Research Institute (IRRI)",
    },

    # --------------------------------------------------------
    # RICE - RICE LEAF ROLLER
    # --------------------------------------------------------
    "rice - rice leaf roller": {
        "type": "pest",
        "crop": "Rice",
        "pest": "Rice leaf roller",
        "pest_type": "Foliage-feeding caterpillar (Lepidoptera)",
        "identification": [
            "Green caterpillars that fold or roll rice leaves into a tube.",
            "Larvae feed inside the folded leaf.",
            "Moths are small and pale.",
        ],
        "damage_signs": [
            "Leaves rolled/folded and eaten from within.",
            "Scraped, whitish window-pane damage on leaves.",
            "Reduced photosynthesis and tiller vigour.",
        ],
        "early_warning": [
            "Young leaves folded or stitched together.",
            "Small scraper marks on leaf surfaces.",
        ],
        "severity_info": (
            "Heavy infestation can reduce yields. Early detection of rolled "
            "leaves helps."
        ),
        "prevention": [
            "Avoid excess nitrogen that encourages lush growth.",
            "Use resistant varieties where available.",
            "Conserve natural enemies (parasitic wasps).",
            "Monitor regularly.",
        ],
        "cultural_control": [
            "Balanced fertilisation, moderate spacing.",
            "Avoid very dense crop canopy.",
        ],
        "mechanical_control": [
            "Hand-pick and destroy folded leaves/insects in small areas.",
            "Remove and destroy heavily infested leaves.",
        ],
        "biological_control": [
            "Conserve parasitoids and predators of caterpillars.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect leaves for folding/rolling weekly.",
            "Look for damage on young leaves first.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "International Rice Research Institute (IRRI)",
    },

    # --------------------------------------------------------
    # RICE - ASIATIC RICE BORER / STEM BORER
    # --------------------------------------------------------
    "rice - asiatic rice borer": {
        "type": "pest",
        "crop": "Rice",
        "pest": "Rice stem borer (asiatic rice borer)",
        "pest_type": "Stem-boring caterpillar (Lepidoptera)",
        "identification": [
            "Larvae bore inside rice stems.",
            "Moths are straw-coloured with a dark spot on each wing.",
            "Egg masses laid on leaf surfaces.",
        ],
        "damage_signs": [
            "Dead central shoot (deadheart) in young plants.",
            "Whiteheads (empty, white panicles) at flowering.",
            "Entry holes and frass (sawdust) at stem base.",
        ],
        "early_warning": [
            "Entry holes and frass at the stem base.",
            "A few deadheart shoots among green tillers.",
        ],
        "severity_info": (
            "Stem borers cause deadheart and whiteheads that reduce yield. "
            "Monitor early for entry holes and dead shoots."
        ),
        "prevention": [
            "Use tolerant/resistant varieties where available.",
            "Use balanced nitrogen (avoid excess that attracts moths).",
            "Conserve natural enemies (egg parasites, wasps).",
            "Destroy crop stubble that harbours overwintering larvae.",
        ],
        "cultural_control": [
            "Remove and destroy stubble after harvest.",
            "Time planting to avoid peak moth activity where possible.",
            "Balanced fertilisation.",
        ],
        "mechanical_control": [
            "Collect and destroy egg masses where practical.",
            "Remove deadheart shoots manually.",
        ],
        "biological_control": [
            "Conserve and release egg/larval parasitoids.",
            "Use neem-based biopesticides as per local practice where "
            "verified.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Check for deadheart and whiteheads weekly.",
            "Look for egg masses and entry holes.",
            "Monitor moth populations with light traps.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "International Rice Research Institute (IRRI); "
                 "State agricultural university IPM extension",
    },

    # --------------------------------------------------------
    # RICE - RICE GALL MIDGE
    # --------------------------------------------------------
    "rice - rice gall midge": {
        "type": "pest",
        "crop": "Rice",
        "pest": "Rice gall midge",
        "pest_type": "Insect (Cecidomyiidae)",
        "identification": [
            "Small mosquito-like flies.",
            "Maggots develop inside the rice stem/leaf sheath.",
            "Larvae cause a gall (silver shoot).",
        ],
        "damage_signs": [
            "Silver or onion-like shoots (galls).",
            "Plants producing tillers but no panicles.",
            "Stunted growth and leaf tubes.",
        ],
        "early_warning": [
            "Appearance of silver shoots (galls).",
            "Excessive tillering with no panicle.",
        ],
        "severity_info": (
            "Gall midge can cause significant tiller loss. Early removal of "
            "silver shoots and monitoring help."
        ),
        "prevention": [
            "Use resistant varieties where available.",
            "Avoid excessive nitrogen.",
            "Maintain good field drainage.",
            "Monitor for silver shoots.",
        ],
        "cultural_control": [
            "Use resistant/tolerant rice varieties.",
            "Balanced nitrogen and good drainage.",
        ],
        "mechanical_control": [
            "Remove and destroy silver shoots where practical.",
        ],
        "biological_control": [
            "Conserve parasitoid wasps of gall midge.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Look for silver shoots weekly.",
            "Monitor adult midge populations.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "International Rice Research Institute (IRRI)",
    },

    # --------------------------------------------------------
    # RICE - RICE LEAFHOPPER
    # --------------------------------------------------------
    "rice - rice leafhopper": {
        "type": "pest",
        "crop": "Rice",
        "pest": "Rice leafhopper",
        "pest_type": "Sucking insect (Hemiptera)",
        "identification": [
            "Small, green or brown leafhoppers on the leaf surface.",
            "They jump when disturbed.",
            "Nymphs are wingless and pale.",
        ],
        "damage_signs": [
            "White speckling/stippling on leaves.",
            "Honeydew and sooty mould.",
            "Leaf yellowing and reduced vigour.",
            "Can transmit viral diseases.",
        ],
        "early_warning": [
            "Leafhoppers jumping on leaves.",
            "Fine whitish speckles on upper leaves.",
        ],
        "severity_info": (
            "Feeding causes speckling, and leafhoppers can vector viruses. "
            "Monitor early."
        ),
        "prevention": [
            "Avoid excess nitrogen.",
            "Conserve natural enemies.",
            "Use tolerant varieties where available.",
            "Monitor leaves regularly.",
        ],
        "cultural_control": [
            "Balanced nitrogen; moderate spacing.",
        ],
        "mechanical_control": [
            "Yellow sticky traps to monitor.",
        ],
        "biological_control": [
            "Conserve predatory bugs and spiders.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect leaves for leafhoppers and speckling.",
            "Use yellow sticky cards.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "International Rice Research Institute (IRRI)",
    },

    # --------------------------------------------------------
    # WHEAT - ENGLISH GRAIN APHID
    # --------------------------------------------------------
    "wheat - english grain aphid": {
        "type": "pest",
        "crop": "Wheat",
        "pest": "English grain aphid",
        "pest_type": "Sucking insect (Hemiptera)",
        "identification": [
            "Small, green or reddish-brown aphids on wheat leaves and "
            "heads.",
            "Found on the upper leaves and developing grain.",
            "Honeydew present; ants may be present.",
        ],
        "damage_signs": [
            "Yellowing of leaves and heads.",
            "Sticky honeydew and sooty mould.",
            "Reduced grain fill and shrivelled kernels.",
        ],
        "early_warning": [
            "A few aphids on the flag leaf and heads.",
            "Honeydew or ants on plants.",
        ],
        "severity_info": (
            "Aphids feed on developing grain and can vector viruses. "
            "Monitor heads and flag leaves."
        ),
        "prevention": [
            "Avoid excess nitrogen.",
            "Conserve natural enemies (parasitic wasps, ladybeetles).",
            "Use tolerant varieties where available.",
            "Monitor when aphids appear near heading.",
        ],
        "cultural_control": [
            "Balanced nitrogen; maintain plant health.",
        ],
        "mechanical_control": [
            "Strong water jet or biological agents for small infestations; "
            "use yellow sticky traps to monitor.",
        ],
        "biological_control": [
            "Conserve and release ladybeetles, lacewings and parasitic "
            "wasps.",
            "Insecticidal soaps/oils can suppress aphids; verify local "
            "registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Check flag leaf and heads from heading onward.",
            "Watch for honeydew and ants.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Avoid broad-spectrum insecticides that harm natural enemies.",
        ],
        "source": "University extension IPM guidance for cereals",
    },

    # --------------------------------------------------------
    # WHEAT - BLOSSOM MIDGE
    # --------------------------------------------------------
    "wheat - wheat blossom midge": {
        "type": "pest",
        "crop": "Wheat",
        "pest": "Wheat blossom midge",
        "pest_type": "Insect (Cecidomyiidae)",
        "identification": [
            "Small orange-red larvae on wheat heads.",
            "Adults are tiny, midge-like flies on heads in the evening.",
            "Larvae feed between the glumes.",
        ],
        "damage_signs": [
            "Shrivelled, distorted or hollow grains.",
            "Damage concentrated in the head.",
            "Ears not filling at the tip.",
        ],
        "early_warning": [
            "Tiny larvae on the head between glumes.",
            "Adults present in the crop at evening.",
        ],
        "severity_info": (
            "Midges reduce grain quality and yield. Monitor the crop from "
            "the boot stage."
        ),
        "prevention": [
            "Use tolerant wheat varieties where available.",
            "Monitor during head emergence in the evening.",
            "Conserve natural enemies.",
        ],
        "cultural_control": [
            "Use tolerant varieties; keep nitrogen balanced.",
        ],
        "mechanical_control": [
            "None broadly applicable; rely on monitoring.",
        ],
        "biological_control": [
            "Conserve parasitoid wasps of midge.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Check heads from boot stage, especially in the evening.",
            "Look for larvae between the glumes.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance for cereals",
    },

    # --------------------------------------------------------
    # CORN - CORN BORER
    # --------------------------------------------------------
    "corn - corn borer": {
        "type": "pest",
        "crop": "Corn",
        "pest": "Corn borer",
        "pest_type": "Stem-boring caterpillar (Lepidoptera)",
        "identification": [
            "Caterpillars bore into corn stalks, tassels, whorls and ears.",
            "Moths are pale with irregular markings.",
            "Egg masses on the undersides of leaves.",
        ],
        "damage_signs": [
            "Holes and frass (sawdust) in the stalk.",
            "Broken or lodged stalks.",
            "Tassel and ear damage, 'shothole' whorl feeding.",
        ],
        "early_warning": [
            "Small holes and frass in early-season whorls.",
            "Leaf feeding (shotholes) in the whorl.",
        ],
        "severity_info": (
            "Borer injury can weaken stalks and reduce yield. Monitor the "
            "whorl and entry holes."
        ),
        "prevention": [
            "Use Bt or resistant hybrids where available and allowed.",
            "Manage crop residue (stalks).",
            "Conserve natural enemies (parasitoids, predators).",
            "Monitor the whorl stage.",
        ],
        "cultural_control": [
            "Manage and shred crop residue after harvest.",
            "Rotate crops.",
        ],
        "mechanical_control": [
            "Remove and destroy infested stalks where practical.",
        ],
        "biological_control": [
            "Conserve parasitic wasps (Trichogramma) and other natural "
            "enemies.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect whorls for shotholes and live larvae.",
            "Check tassel and stalk base for holes and frass.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance for field corn",
    },

    # --------------------------------------------------------
    # CORN - ARMYWORM
    # --------------------------------------------------------
    "corn - army worm": {
        "type": "pest",
        "crop": "Corn",
        "pest": "Armyworm",
        "pest_type": "Foliage-feeding caterpillar (Lepidoptera)",
        "identification": [
            "Greenish to dark caterpillars with pale stripes along the "
            "body.",
            "Raised dark spots along the side of each segment.",
            "Often found in groups during early instars.",
        ],
        "damage_signs": [
            "Leaves eaten / window-paned.",
            "Ragged leaf edges and defoliation.",
            "In severe cases caterpillars may cut lower leaves.",
        ],
        "early_warning": [
            "Small groups of caterpillars on leaves.",
            "Scattered 'window-pane' feeding marks.",
        ],
        "severity_info": (
            "Caterpillars can defoliate plants rapidly. Scout for early "
            "instars and monitor edges."
        ),
        "prevention": [
            "Monitor fields, especially field edges and grassy areas.",
            "Encourage natural enemies.",
            "Remove grassy weeds that host larvae.",
        ],
        "cultural_control": [
            "Keep weed pressure low in and around fields.",
        ],
        "mechanical_control": [
            "Hand-pick in small areas or use treated-field monitoring.",
        ],
        "biological_control": [
            "Conserve parasitoids and predators of armyworm.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout the whorl and lower leaves weekly.",
            "Check field edges and grassy areas first.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance for field crops",
    },

    # --------------------------------------------------------
    # GENERAL - BLACK CUTWORM
    # --------------------------------------------------------
    "corn - black cutworm": {
        "type": "pest",
        "crop": "Corn",
        "pest": "Black cutworm",
        "pest_type": "Soil-dwelling caterpillar (Lepidoptera)",
        "identification": [
            "Dark grey-black caterpillars that curve into a C when "
            "disturbed.",
            "Feed at night near soil level.",
            "Hide in soil clods during the day.",
        ],
        "damage_signs": [
            "Young seedlings cut off at the soil line.",
            "Missing or wilted plants in scattered patches.",
            "Holes in lower stems.",
        ],
        "early_warning": [
            "Cut/severed seedlings in patches.",
            "Caterpillars curled in the soil near cut plants.",
        ],
        "severity_info": (
            "Cutworms cut seedlings at ground level, causing stand loss. "
            "Scout seedling stands early."
        ),
        "prevention": [
            "Manage winter weeds that host cutworm.",
            "Monitor seedling stands early.",
            "Conserve natural enemies.",
        ],
        "cultural_control": [
            "Remove weeds and crop residue before planting.",
            "Use a clean, well-prepared seedbed.",
        ],
        "mechanical_control": [
            "Scout and hand-remove small infestations near cut plants.",
        ],
        "biological_control": [
            "Conserve parasitic wasps and ground beetles.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect seedling stands for cut plants daily for the first "
            "weeks.",
            "Look for caterpillars in the soil near damaged plants.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance for field crops",
    },

    # --------------------------------------------------------
    # RICE - MOLE CRICKET
    # --------------------------------------------------------
    "rice - mole cricket": {
        "type": "pest",
        "crop": "Rice",
        "pest": "Mole cricket",
        "pest_type": "Soil-dwelling insect (Orthoptera)",
        "identification": [
            "Large, brown crickets with powerful front legs adapted for "
            "digging.",
            "Live in soil; make tunnels.",
            "Adults are active at night.",
        ],
        "damage_signs": [
            "Disturbed soil and tunnels in fields/seedbeds.",
            "Damaged roots and seedlings near tunnels.",
            "Dying seedlings in patches.",
        ],
        "early_warning": [
            "Tunnels and loose soil mounds.",
            "Hopping crickets at night.",
        ],
        "severity_info": (
            "Mole crickets damage seedlings and roots in fields and "
            "seedbeds. Check for soil disturbance."
        ),
        "prevention": [
            "Prepare a well-drained seedbed.",
            "Avoid excessive organic matter that attracts crickets.",
        ],
        "cultural_control": [
            "Good seedbed preparation and ploughing to expose them to "
            "predators.",
        ],
        "mechanical_control": [
            "Flood/monitor tunnels; hand-catch where practical.",
        ],
        "biological_control": [
            "Encourage natural predators (birds, ants).",
        ],
        "chemical_control": [],
        "monitoring": [
            "Look for fresh tunnels and soil mounds.",
            "Check seedlings near tunnels for root damage.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "Agricultural extension pest guidance",
    },

    # --------------------------------------------------------
    # GENERAL - STEM BORER
    # --------------------------------------------------------
    "general - stem borer": {
        "type": "pest",
        "crop": "Various field crops",
        "pest": "Stem borer",
        "pest_type": "Stem-boring caterpillar/larva (Lepidoptera/Diptera)",
        "identification": [
            "Larvae bore into stems, feeding from the inside.",
            "Entry holes with frass (sawdust-like droppings) on the plant.",
            "Adults are moths or flies that lay eggs on the plant.",
        ],
        "damage_signs": [
            "Dead tops (deadheart) in young plants.",
            "Whiteheads / empty heads in cereals.",
            "Broken, lodged or bored stems with entry holes and frass.",
        ],
        "early_warning": [
            "Entry holes and frass at the stem base.",
            "Yellowing or drying central shoots.",
            "Deadheart among otherwise healthy tillers.",
        ],
        "severity_info": (
            "Borer damage can cause stand loss and reduce yield. Monitor "
            "for entry holes, frass and dead shoots early."
        ),
        "prevention": [
            "Use tolerant/resistant varieties where available.",
            "Use balanced nitrogen (avoid excess that attracts moths).",
            "Destroy crop stubble and residue after harvest.",
            "Monitor for egg masses and entry holes.",
        ],
        "cultural_control": [
            "Remove/destroy stubble and crop residue.",
            "Rotate crops and time planting away from peak moth flight.",
            "Balanced fertilisation.",
        ],
        "mechanical_control": [
            "Remove and destroy egg masses and dead shoots where practical.",
        ],
        "biological_control": [
            "Conserve parasitic wasps (egg/larval parasitoids) and "
            "predators.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout for deadheart and whiteheads weekly.",
            "Look for egg masses and entry holes with frass.",
            "Monitor adult moths with light traps.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance for field crops",
    },

    # --------------------------------------------------------
    # GENERAL - WEEVIL
    # --------------------------------------------------------
    "general - weevil": {
        "type": "pest",
        "crop": "Various crops",
        "pest": "Weevil",
        "pest_type": "Beetle (Curculionidae) - adults and grubs",
        "identification": [
            "Small beetles with a distinct, elongated snout.",
            "Larvae are grubs that live in soil, roots, seeds or stems.",
            "Adults may feed on leaves, roots or developing seed.",
        ],
        "damage_signs": [
            "Notched or eaten leaves and shoots.",
            "Damaged roots, stems or developing seeds/grain.",
            "Wilted or stunted plants in patches.",
        ],
        "early_warning": [
            "Notched feeding on leaf edges.",
            "Adult weevils present on plants or near the ground.",
        ],
        "severity_info": (
            "Weevils can damage roots, shoots and seed. Monitor adults and "
            "larval damage early."
        ),
        "prevention": [
            "Inspect transplants and seed before planting.",
            "Maintain clean fields and manage crop residue.",
            "Rotate crops.",
            "Monitor early in the season.",
        ],
        "cultural_control": [
            "Rotate crops and manage residue.",
            "Remove weeds that host weevils.",
        ],
        "mechanical_control": [
            "Hand-collect adults where practical.",
        ],
        "biological_control": [
            "Conserve natural enemies (parasitoids, predators).",
        ],
        "chemical_control": [],
        "monitoring": [
            "Look for notched leaves and adults.",
            "Inspect roots/seed for grubs.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance",
    },

    # --------------------------------------------------------
    # GENERAL - WHITE GRUB / SOIL GRUB
    # --------------------------------------------------------
    "general - white grub": {
        "type": "pest",
        "crop": "Various field crops",
        "pest": "White grub / soil grub",
        "pest_type": "Beetle larva (Scarabaeidae/Elateridae)",
        "identification": [
            "C-shaped, off-white to cream-coloured grubs in the soil.",
            "Found near the root zone; feed on roots.",
            "Adults are scarab or click beetles (may be seen at night).",
        ],
        "damage_signs": [
            "Wilted, stunted or dying plants in patches.",
            "Damaged or chewed roots.",
            "Loosened soil or adult beetles flying at dusk.",
        ],
        "early_warning": [
            "Wilted plants in circular patches.",
            "Grubs found when digging near roots.",
        ],
        "severity_info": (
            "Soil grubs damage roots causing wilting and stand loss. Check "
            "the root zone for grubs."
        ),
        "prevention": [
            "Deep ploughing/soil preparation.",
            "Manage crop residue and organic matter.",
            "Avoid leaving the soil undisturbed between crops.",
        ],
        "cultural_control": [
            "Deep tillage to expose grubs to predators.",
            "Good field hygiene.",
        ],
        "mechanical_control": [
            "Hand-collect grubs during field operations where practical.",
        ],
        "biological_control": [
            "Encourage birds and predatory ground beetles.",
            "Some biopesticides target soil grubs in some regions; verify "
            "local registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Dig around the root zone of wilted plants.",
            "Watch for adult beetles flying at dusk.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance",
    },

    # --------------------------------------------------------
    # GENERAL - SCALE INSECT
    # --------------------------------------------------------
    "general - scale insect": {
        "type": "pest",
        "crop": "Fruit / ornamentals / perennials",
        "pest": "Scale insect",
        "pest_type": "Sucking insect (Hemiptera - Coccoidea)",
        "identification": [
            "Small, sessile, shield- or shell-like insects on stems "
            "and leaves.",
            "Often look like waxy bumps that can be scraped off.",
            "Adults are wingless; nymphs ('crawlers') move briefly.",
        ],
        "damage_signs": [
            "Sticky honeydew and sooty mould.",
            "Yellowing, stunting and dieback of shoots.",
            "Reduced vigour and fruit quality.",
        ],
        "early_warning": [
            "Small waxy bumps appearing on stems/leaves.",
            "Sooty mould or ants (honeydew).",
        ],
        "severity_info": (
            "Heavy scale build-up weakens plants. Monitor for waxy bumps "
            "and honeydew."
        ),
        "prevention": [
            "Inspect nursery stock and transplants.",
            "Maintain plant health and avoid stress.",
            "Prune heavily infested branches.",
            "Encourage natural enemies.",
        ],
        "cultural_control": [
            "Prune infested branches; improve airflow.",
        ],
        "mechanical_control": [
            "Scrape or hose off scales in small infestations.",
            "Prune and remove heavily infested parts.",
        ],
        "biological_control": [
            "Conserve and release ladybeetles and parasitic wasps.",
            "Horticultural oils/soaps can suppress scales; verify local "
            "registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect stems and undersides of leaves for waxy bumps.",
            "Watch for sooty mould and ants.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance",
    },

    # --------------------------------------------------------
    # GENERAL - MEALYBUG
    # --------------------------------------------------------
    "general - mealybug": {
        "type": "pest",
        "crop": "Fruit / ornamentals / perennials",
        "pest": "Mealybug",
        "pest_type": "Sucking insect (Hemiptera)",
        "identification": [
            "Soft-bodied insects covered with a white, waxy, powdery "
            "coating.",
            "Found in clusters in leaf axils, under leaves and on fruit.",
            "Often accompanied by ants and honeydew.",
        ],
        "damage_signs": [
            "Sticky honeydew and sooty mould.",
            "Yellowing, stunting and wilting.",
            "Reduced growth and fruit quality.",
        ],
        "early_warning": [
            "White powdery clusters on stems/leaf axils.",
            "Ants moving up plants.",
        ],
        "severity_info": (
            "Mealybugs weaken plants and produce honeydew. Monitor leaf "
            "axils and new growth."
        ),
        "prevention": [
            "Inspect plants before bringing in nursery stock.",
            "Control ants that protect mealybugs.",
            "Encourage natural enemies.",
            "Avoid excessive nitrogen.",
        ],
        "cultural_control": [
            "Prune infested parts and improve airflow.",
        ],
        "mechanical_control": [
            "Remove with a cotton swab/alcohol for small infestations or "
            "hose off.",
        ],
        "biological_control": [
            "Conserve ladybeetles, lacewings and parasitic wasps.",
            "Insecticidal soaps/oils can suppress mealybugs; verify local "
            "registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect leaf axils and undersides for white clusters.",
            "Watch for ants and sooty mould.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance",
    },

    # --------------------------------------------------------
    # GENERAL - GRASSHOPPER / LOCUST
    # --------------------------------------------------------
    "general - grasshopper": {
        "type": "pest",
        "crop": "Various field crops",
        "pest": "Grasshopper / locust",
        "pest_type": "Chewing insect (Orthoptera)",
        "identification": [
            "Brown, green or yellow insects with strong hind legs for "
            "jumping.",
            "Large populations may swarm.",
            "Nymphs are wingless and smaller.",
        ],
        "damage_signs": [
            "Ragged, chewed leaf edges.",
            "Large numbers feeding on foliage.",
            "Severe defoliation in outbreak areas.",
        ],
        "early_warning": [
            "A few grasshoppers feeding on plants.",
            "Ragged leaves at field edges.",
        ],
        "severity_info": (
            "Grasshoppers can defoliate crops rapidly in high numbers. "
            "Monitor field edges and grassy areas."
        ),
        "prevention": [
            "Manage weedy, grassy areas near the crop.",
            "Encourage natural enemies (birds, parasitoids).",
            "Monitor early for nymphs.",
        ],
        "cultural_control": [
            "Remove grassy weeds and maintain clean field margins.",
        ],
        "mechanical_control": [
            "Physical removal/low-intensity methods for small areas.",
        ],
        "biological_control": [
            "Encourage predatory birds and parasitoids.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Scout field edges and grassy areas.",
            "Watch for nymphs early in the season.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance",
    },

    # --------------------------------------------------------
    # GENERAL - BLISTER BEETLE
    # --------------------------------------------------------
    "general - blister beetle": {
        "type": "pest",
        "crop": "Forage / field crops",
        "pest": "Blister beetle",
        "pest_type": "Beetle (Meloidae)",
        "identification": [
            "Elongated, brightly coloured (black, grey, orange-striped) "
            "beetles.",
            "Soft wing covers.",
            "Feed in groups on flowers and foliage.",
        ],
        "damage_signs": [
            "Defoliation of leaves and flowers.",
            "Beetles present in groups.",
        ],
        "early_warning": [
            "Groups of beetles on flowers/foliage.",
            "Ragged leaf edges near flowering.",
        ],
        "severity_info": (
            "Beetles feed on flowers and foliage. Treat with care; handling "
            "can release blister-causing substances - do not crush on skin."
        ),
        "prevention": [
            "Monitor flowering crops.",
            "Manage weedy hosts.",
            "Use care when handling to avoid skin contact.",
        ],
        "cultural_control": [
            "Keep weeds and alternate hosts down.",
        ],
        "mechanical_control": [
            "Remove by hand with care (wear gloves, do not crush).",
        ],
        "biological_control": [
            "Conserve natural enemies where present.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect flowers and young foliage for groups of beetles.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Do not crush blister beetles on skin; wash hands after contact.",
        ],
        "source": "University extension IPM guidance",
    },

    # --------------------------------------------------------
    # GENERAL - LEAF BEETLE / FLEA BEETLE
    # --------------------------------------------------------
    "general - leaf beetle": {
        "type": "pest",
        "crop": "Various crops",
        "pest": "Leaf beetle / flea beetle",
        "pest_type": "Beetle (Chrysomelidae)",
        "identification": [
            "Small to medium chewing beetles on leaves.",
            "Flea beetles are tiny and jump when disturbed.",
            "Larvae may feed on roots or leaves.",
        ],
        "damage_signs": [
            "Chewed, ragged holes in leaves.",
            "Shot-hole / pin-hole feeding on young leaves.",
            "Stunted young seedlings.",
        ],
        "early_warning": [
            "Small holes in young leaves.",
            "Beetles jumping/feeding when disturbed.",
        ],
        "severity_info": (
            "Beetles feed on foliage, especially damaging seedlings. "
            "Monitor young plants."
        ),
        "prevention": [
            "Use clean seed and transplants.",
            "Control weeds that host beetles.",
            "Use row covers where appropriate.",
        ],
        "cultural_control": [
            "Remove weedy alternate hosts.",
        ],
        "mechanical_control": [
            "Sticky traps / hand-removal in small areas.",
        ],
        "biological_control": [
            "Conserve predatory insects and birds.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect young leaves for holes.",
            "Watch for beetles jumping at the base of plants.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance",
    },

    # --------------------------------------------------------
    # GENERAL - FRUIT FLY
    # --------------------------------------------------------
    "general - fruit fly": {
        "type": "pest",
        "crop": "Fruit crops",
        "pest": "Fruit fly (Bactrocera/Dacus)",
        "pest_type": "Fly (Tephritidae)",
        "identification": [
            "Small flies with clear or patterned wings and a distinctive "
            "wing spot.",
            "Female lays eggs into ripening fruit.",
            "Larvae (maggots) feed inside the fruit.",
        ],
        "damage_signs": [
            "Small puncture/oviposition marks on fruit.",
            "Fruit rotting, shrivelling or dropping.",
            "Maggots present inside the fruit.",
        ],
        "early_warning": [
            "Puncture marks on ripening fruit.",
            "Fruit dropping with soft spots.",
        ],
        "severity_info": (
            "Fruit flies damage ripening fruit. Prompt removal of infested "
            "fruit reduces breeding."
        ),
        "prevention": [
            "Monitor with lure/parapheromone traps.",
            "Keep orchard clean; remove fallen fruit.",
            "Bagging of fruit where practical.",
            "Use resistant/thin-skinned varieties where available.",
        ],
        "cultural_control": [
            "Sanitation - remove and destroy fallen and infested fruit.",
            "Bag fruit (where practical).",
        ],
        "mechanical_control": [
            "Use sticky/methyl-eugenol or protein-bait traps.",
            "Hand-remove infested fruit.",
        ],
        "biological_control": [
            "Conserve parasitoid wasps.",
            "Conserve released sterile sterile-insect programs where "
            "present.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Set fruit fly traps and check regularly.",
            "Inspect ripening fruit for puncture marks.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
            "Sanitation (removing infested fruit) is the key first step.",
        ],
        "source": "University extension IPM guidance",
    },

    # --------------------------------------------------------
    # GENERAL - LEAFMINER
    # --------------------------------------------------------
    "general - leafminer": {
        "type": "pest",
        "crop": "Vegetables / fruit",
        "pest": "Leafminer",
        "pest_type": "Fly larva / moth larva",
        "identification": [
            "Larvae tunnel inside leaf tissue.",
            "Visible as winding, whitish or brown trails (mines) on "
            "leaves.",
            "Small adult flies or moths.",
        ],
        "damage_signs": [
            "Winding white/grey tunnels in leaves.",
            "Blotchy or disfigured leaf surfaces.",
            "Reduced photosynthesis and leaf drop.",
        ],
        "early_warning": [
            "Tiny serpentine mines on young leaves.",
            "Small white/brown winding trails.",
        ],
        "severity_info": (
            "Severe mining reduces leaf area. Monitor young foliage and "
            "remove infested leaves."
        ),
        "prevention": [
            "Inspect transplants before planting.",
            "Use row covers where appropriate.",
            "Encourage parasitoid wasps.",
            "Remove infested leaves/plants.",
        ],
        "cultural_control": [
            "Remove and destroy heavily infested leaves.",
        ],
        "mechanical_control": [
            "Remove and dispose of mined leaves by hand.",
            "Yellow sticky traps for adults.",
        ],
        "biological_control": [
            "Conserve parasitoid wasps that attack leafminers.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect young leaves for mines and trails.",
            "Use yellow sticky traps for adults.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance",
    },

    # --------------------------------------------------------
    # GENERAL - MIRID / TRUE BUG
    # --------------------------------------------------------
    "general - mirid bug": {
        "type": "pest",
        "crop": "Various crops",
        "pest": "Mirid / plant bug",
        "pest_type": "Sucking bug (Hemiptera - Miridae)",
        "identification": [
            "Small, oval, greenish or brownish bugs.",
            "Feeds by sucking sap on shoots, buds and fruit.",
            "Both nymphs and adults feed.",
        ],
        "damage_signs": [
            "Distorted, blasted or deformed young shoots and fruit.",
            "Small sunken or scarred spots on fruit.",
            "Flower/fruit drop.",
        ],
        "early_warning": [
            "Nymphs on new growth and buds.",
            "Deformed young shoots/fruit.",
        ],
        "severity_info": (
            "Plant bugs reduce quality and yield by feeding on young "
            "growth. Monitor shoots and buds."
        ),
        "prevention": [
            "Manage weedy alternate hosts.",
            "Monitor new growth and buds.",
            "Encourage natural enemies.",
        ],
        "cultural_control": [
            "Control weeds that host plant bugs.",
        ],
        "mechanical_control": [
            "Sweep nets / beating to detect and reduce adults.",
        ],
        "biological_control": [
            "Conserve natural enemies (spiders, parasitoids).",
        ],
        "chemical_control": [],
        "monitoring": [
            "Sweep net or inspect emerging shoots and buds.",
            "Check fruit for sunken scars.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance",
    },

    # --------------------------------------------------------
    # GENERAL - FOLIAGE CATERPILLAR
    # --------------------------------------------------------
    "general - foliage caterpillar": {
        "type": "pest",
        "crop": "Various crops",
        "pest": "Foliage-feeding caterpillar",
        "pest_type": "Caterpillar (Lepidoptera)",
        "identification": [
            "Caterpillars (larvae) feeding on leaves, flowers or inside "
            "rolled leaves.",
            "Moths lay eggs on the crop.",
            "Damage increases with instar growth.",
        ],
        "damage_signs": [
            "Chewed, ragged or window-paned leaves.",
            "Scraped leaf surfaces.",
            "Defoliation and reduced plant vigour.",
        ],
        "early_warning": [
            "Early-stage caterpillars in small groups.",
            "Ragged leaf edges or window-pane feeding.",
        ],
        "severity_info": (
            "Caterpillars can defoliate rapidly. Scout for early instars, "
            "rolled leaves and egg masses."
        ),
        "prevention": [
            "Scout for eggs and early larvae.",
            "Encourage natural enemies (parasitoids, predators).",
            "Use tolerant/resistant varieties where available.",
            "Remove weeds that host caterpillars.",
        ],
        "cultural_control": [
            "Manage weeds and crop residue.",
        ],
        "mechanical_control": [
            "Hand-pick/remove early larvae and egg masses in small areas.",
            "Remove rolled/infested leaves.",
        ],
        "biological_control": [
            "Conserve parasitic wasps and predatory insects.",
            "Neem-based biopesticides are used in many regions; verify "
            "local registration.",
        ],
        "chemical_control": [],
        "monitoring": [
            "Inspect leaves for eggs, caterpillars and feeding damage.",
            "Watch the undersides of leaves.",
        ],
        "safety_notes": [
            CHEMICAL_FALLBACK,
            REGIONAL_NOTE,
        ],
        "source": "University extension IPM guidance",
    },
}


# ============================================================
# PEST NAME ALIASES
# ============================================================
# The YOLO pest detector returns one of ~102 class names (e.g.
# "brown plant hopper", "asiatice rice borer", "Dacus dorsalis").
# Many are variants of the same pest OR use obscure Latin names.
# This map routes each class name to a canonical knowledge-base
# record so that a real detection ALWAYS returns management and
# prevention guidance (never fabricated; chemical stays empty).

PEST_ALIASES = {
    "rice leaf roller": "rice - rice leaf roller",
    "rice leaf caterpillar": "general - foliage caterpillar",
    "paddy stem maggot": "general - stem borer",
    "asiatic rice borer": "rice - asiatic rice borer",
    "asiatice rice borer": "rice - asiatic rice borer",
    "yellow rice borer": "general - stem borer",
    "rice gall midge": "rice - rice gall midge",
    "rice stemfly": "general - stem borer",
    "brown plant hopper": "rice - brown plant hopper",
    "white backed plant hopper": "rice - white backed plant hopper",
    "small brown plant hopper": "rice - brown plant hopper",
    "rice water weevil": "general - weevil",
    "rice leafhopper": "rice - rice leafhopper",
    "grain spreader thrips": "tomato - thrips",
    "rice shell pest": "general - mirid bug",
    "grub": "general - white grub",
    "mole cricket": "rice - mole cricket",
    "wireworm": "general - white grub",
    "white margined moth": "general - foliage caterpillar",
    "black cutworm": "corn - black cutworm",
    "large cutworm": "corn - black cutworm",
    "yellow cutworm": "corn - black cutworm",
    "red spider": "tomato - spider mite",
    "corn borer": "corn - corn borer",
    "army worm": "corn - army worm",
    "armyworm": "corn - army worm",
    "aphids": "tomato - aphid",
    "potosiabre vitarsis": "general - white grub",
    "peach borer": "general - stem borer",
    "english grain aphid": "wheat - english grain aphid",
    "green bug": "tomato - aphid",
    "bird cherry-oataphid": "tomato - aphid",
    "bird cherry-oat aphid": "tomato - aphid",
    "wheat blossom midge": "wheat - wheat blossom midge",
    "penthaleus major": "tomato - spider mite",
    "longlegged spider mite": "tomato - spider mite",
    "wheat phloeothrips": "tomato - thrips",
    "wheat sawfly": "general - stem borer",
    "cerodonta denticornis": "general - stem borer",
    "beet fly": "general - leafminer",
    "flea beetle": "general - leaf beetle",
    "cabbage army worm": "corn - army worm",
    "beet army worm": "corn - army worm",
    "beet spot flies": "general - leafminer",
    "meadow moth": "general - foliage caterpillar",
    "beet weevil": "general - weevil",
    "sericaorient alismots chulsky": "general - white grub",
    "alfalfa weevil": "general - weevil",
    "flax budworm": "general - foliage caterpillar",
    "alfalfa plant bug": "general - mirid bug",
    "tarnished plant bug": "general - mirid bug",
    "locustoidea": "general - grasshopper",
    "lytta polita": "general - blister beetle",
    "legume blister beetle": "general - blister beetle",
    "blister beetle": "general - blister beetle",
    "therioaphis maculata buckton": "tomato - aphid",
    "odontothrips loti": "tomato - thrips",
    "thrips": "tomato - thrips",
    "alfalfa seed chalcid": "wheat - wheat blossom midge",
    "pieris canidia": "general - foliage caterpillar",
    "apolygus lucorum": "general - mirid bug",
    "limacodidae": "general - foliage caterpillar",
    "viteus vitifoliae": "tomato - aphid",
    "colomerus vitis": "tomato - spider mite",
    "brevipoalpus lewisi mcgregor": "tomato - spider mite",
    "oides decempunctata": "general - leaf beetle",
    "polyphagotars onemus latus": "tomato - spider mite",
    "pseudococcus comstocki kuwana": "general - mealybug",
    "parathrene regalis": "general - stem borer",
    "ampelophaga": "general - foliage caterpillar",
    "lycorma delicatula": "general - mirid bug",
    "xylotrechus": "general - stem borer",
    "cicadella viridis": "rice - rice leafhopper",
    "miridae": "general - mirid bug",
    "trialeurodes vaporariorum": "tomato - whitefly",
    "erythroneura apicalis": "rice - rice leafhopper",
    "papilio xuthus": "general - foliage caterpillar",
    "panonchus citri mcgregor": "tomato - spider mite",
    "phyllocoptes oleiverus ashmead": "tomato - spider mite",
    "icerya purchasi maskell": "general - scale insect",
    "unaspis yanonensis": "general - scale insect",
    "ceroplastes rubens": "general - scale insect",
    "chrysomphalus aonidum": "general - scale insect",
    "parlatoria zizyphus lucus": "general - scale insect",
    "nipaecoccus vastalor": "general - mealybug",
    "aleurocanthus spiniferus": "tomato - whitefly",
    "tetradacus c bactrocera minax": "general - fruit fly",
    "dacus dorsalis(hendel)": "general - fruit fly",
    "bactrocera tsuneonis": "general - fruit fly",
    "prodenia litura": "corn - army worm",
    "adristyrannus": "general - foliage caterpillar",
    "phyllocnistis citrella stainton": "general - leafminer",
    "toxoptera citricidus": "tomato - aphid",
    "toxoptera aurantii": "tomato - aphid",
    "aphis citricola vander goot": "tomato - aphid",
    "scirtothrips dorsalis hood": "tomato - thrips",
    "dasineura sp": "wheat - wheat blossom midge",
    "lawana imitata melichar": "general - mirid bug",
    "salurnis marginella guerr": "general - mirid bug",
    "deporaus marginatus pascoe": "general - weevil",
    "chlumetia transversa": "general - stem borer",
    "mango flat beak leafhopper": "rice - rice leafhopper",
    "rhytidodera bowrinii white": "general - stem borer",
    "sternochetus frigidus": "general - weevil",
    "cicadellidae": "rice - rice leafhopper",
}


# ============================================================
# RETRIEVAL LOGIC
# ============================================================

def _normalize(text):
    """Lowercase and clean a crop/disease/pest name for lookups."""
    if text is None:
        return ""
    cleaned = str(text).strip().lower().replace("_", " ").replace("-", " ")
    # Strip punctuation that can appear in detector labels ("Pepper, bell",
    # "Esca (Black Measles)") so those names match the knowledge base.
    cleaned = re.sub(r"[(),.;:'\"!?/]", " ", cleaned)
    return " ".join(cleaned.split())


# Make alias lookups punctuation-insensitive: normalise every alias key so
# hyphenated / underscore detector labels ("bird cherry-oataphid") match the
# normalised problem string used in _find_record.
PEST_ALIASES = {_normalize(k): v for k, v in PEST_ALIASES.items()}


def _token_set(text):
    return set(_normalize(text).split())


def _matches(left, right):
    """Return True when two names loosely refer to the same thing."""
    left, right = _normalize(left), _normalize(right)
    if not left or not right:
        return False
    if left == right:
        return True
    lt, rt = _token_set(left), _token_set(right)
    if lt and rt and lt.intersection(rt):
        return True
    return left in right or right in left


def _split_crop_problem(crop, problem):
    """Handle the case where detection returns 'crop - problem' as one string."""
    if not crop and problem and " - " in str(problem):
        parts = str(problem).split(" - ", 1)
        crop = parts[0].strip()
        problem = parts[1].strip()
    return crop, problem


def _find_record(store, crop, problem, aliases=None):
    """Locate a knowledge-base record for a crop + problem combination."""
    crop_n = _normalize(crop)
    prob_n = _normalize(problem)

    # Detection may supply the whole string "crop - problem" as the problem.
    if not crop_n and prob_n and " - " in prob_n:
        parts = prob_n.split(" - ", 1)
        crop_n = _normalize(parts[0])
        prob_n = _normalize(parts[1])

    # Pass 1: exact key match.
    if crop_n and prob_n:
        key = f"{crop_n} - {prob_n}"
        if key in store:
            return store[key]

    # Pass 1a: punctuation-normalised key match. Detector labels and stored
    # keys can differ in parentheses/hyphens/spelling, so compare the fully
    # normalised "crop - problem" key. This lets "Tomato - Target spot" map
    # precisely and avoids the loose token fallback picking a wrong record.
    if crop_n and prob_n:
        norm_key = _normalize(f"{crop_n} - {prob_n}")
        for _k, _rec in store.items():
            if _normalize(_k) == norm_key:
                return _rec

    # Pass 1b: alias map (maps detector class names to a canonical record).
    if aliases:
        canon = aliases.get(prob_n)
        if canon and canon in store:
            return store[canon]

    # Pass 2: token-based crop + problem match.
    for key, record in store.items():
        chunks = key.split(" - ")
        if len(chunks) != 2:
            continue
        k_crop, k_prob = chunks[0], chunks[1]
        if _matches(crop_n, k_crop) and _matches(prob_n, k_prob):
            return record

    # Pass 3: problem-only match as a fallback when crop is unknown.
    if not crop_n:
        for key, record in store.items():
            chunks = key.split(" - ")
            if len(chunks) == 2 and _matches(prob_n, chunks[1]):
                return record

    return None


# ============================================================
# RISK ASSESSMENT HELPERS
# ============================================================

def _as_float(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _confidence_label(confidence):
    """Turn a raw confidence value into a labeled risk assessment."""
    value = _as_float(confidence)
    if value is None:
        return {
            "percent": None,
            "level": "UNKNOWN",
            "label": "Confidence not provided.",
            "warning": "Confidence is unavailable. Verify identification "
                       "with an expert before acting.",
        }
    if value <= 1.0:
        value = value * 100.0
    value = round(value, 1)
    if value >= 90:
        level, label = "HIGH", "High-confidence prediction."
    elif value >= 70:
        level, label = "MEDIUM", "Likely detection."
    elif value >= 50:
        level, label = "LOW", ("Possible detection - further inspection "
                               "recommended.")
    else:
        level, label = "UNKNOWN", (
            "Unable to confidently identify the problem from the image. "
            "Please upload a clearer image or seek expert inspection."
        )
    warning = level in ("LOW", "UNKNOWN")
    return {
        "percent": value,
        "level": level,
        "label": label,
        "warning": warning,
        "message": ("Verify the identification with a local agricultural "
                    "expert before taking action.") if warning else None,
    }


def _weather_risk(temperature, humidity, rainfall):
    """Classify current weather as a disease/pest risk factor."""
    score = 0
    factors = []

    humidity_value = _as_float(humidity)
    if humidity_value is not None:
        if humidity_value >= 90:
            score += 2
            factors.append("Very high humidity (>= 90%).")
        elif humidity_value >= 75:
            score += 1
            factors.append("High humidity (>= 75%).")

    rainfall_value = _as_float(rainfall)
    if rainfall_value is not None:
        if rainfall_value >= 10:
            score += 2
            factors.append("Recent/heavy rainfall (>= 10 mm).")
        elif rainfall_value >= 2:
            score += 1
            factors.append("Some rainfall (>= 2 mm).")

    temperature_value = _as_float(temperature)
    if temperature_value is not None and 18 <= temperature_value <= 30:
        score += 1
        factors.append("Moderate temperatures (18-30 C).")

    level = "HIGH" if score >= 4 else ("MEDIUM" if score >= 2 else "LOW")
    if score >= 2:
        explanation = ("Current weather conditions may favour disease/pest "
                       "development. Continue monitoring closely.")
    else:
        explanation = ("Current weather conditions do not strongly favour "
                       "disease/pest development.")

    return {
        "level": level,
        "score": score,
        "factors": factors,
        "explanation": explanation,
        "note": "Weather is a risk indicator only and does not confirm the "
                "presence of a disease or pest.",
    }


def _severity_info(severity):
    """Map a reported severity value to a standard label."""
    if severity is None or severity == "":
        return {
            "provided": False,
            "level": None,
            "label": "Could not be determined",
            "note": SEVERITY_UNKNOWN + " Use the symptoms and monitoring "
                                       "guidance to assess the situation.",
        }
    mapping = {
        "low": "LOW", "mild": "LOW", "minor": "LOW", "slight": "LOW",
        "moderate": "MODERATE", "medium": "MODERATE",
        "high": "HIGH", "severe": "HIGH", "heavy": "HIGH", "critical": "HIGH",
    }
    level = mapping.get(_normalize(severity))
    if level:
        return {
            "provided": True,
            "level": level,
            "label": level.title(),
            "note": (f"Reported severity: {level.title()}. Higher severity "
                     "generally warrants faster action; begin with "
                     "prevention and non-chemical controls."),
        }
    return {
        "provided": True,
        "level": None,
        "label": "Unknown",
        "note": (f"Reported severity ({severity}) was not recognised. "
                 "Treat the situation with caution and consult an expert."),
    }


IPM_ORDER = [
    "Prevention",
    "Monitoring",
    "Cultural control",
    "Mechanical control",
    "Biological control",
    "Chemical control",
]


def _management_steps(cultural, mechanical, biological, chemical, monitoring):
    """Assemble an ordered, dedicated 'WHAT TO DO NOW' action list."""
    steps = []
    for section in (cultural, mechanical, biological, chemical, monitoring):
        for item in section:
            text = item.strip() if isinstance(item, str) else str(item)
            if text and text.lower() not in (s.lower() for s in steps):
                steps.append(text)
    return steps


def _level_score(level):
    return {"LOW": 1, "MEDIUM": 2, "MODERATE": 2, "HIGH": 3,
            "UNKNOWN": 0, None: 0}.get(level, 0)


def _risk_level(confidence_level, severity_level, weather_level):
    """Combine confidence, severity and weather into an overall risk level."""
    score = 0
    score += _level_score(severity_level) + _level_score(weather_level)
    if confidence_level == "HIGH":
        pass
    elif confidence_level == "MEDIUM":
        pass
    elif confidence_level == "LOW":
        score += 1
    elif confidence_level == "UNKNOWN":
        score += 2
    if score >= 5:
        return "HIGH"
    if score >= 3:
        return "MEDIUM"
    return "LOW"


# ============================================================
# RESPONSE BUILDERS
# ============================================================

def _base_result(crop, problem, problem_type, confidence, severity,
                 temperature, humidity, rainfall, location):
    return {
        "success": True,
        "crop": crop,
        "problem_type": problem_type,
        "problem": problem,
        "in_knowledge_base": False,
        "confidence": _confidence_label(confidence),
        "severity": _severity_info(severity),
        "weather_risk": _weather_risk(temperature, humidity, rainfall),
        "location": location,
        "pathogen": None,
        "pest_type": None,
        "message": None,
        "identification": [],
        "symptoms": [],
        "damage_signs": [],
        "early_warning": [],
        "severity_indicators": [],
        "favorable_conditions": [],
        "prevention": [],
        "cultural_control": [],
        "mechanical_control": [],
        "biological_control": [],
        "chemical_control": [],
        "monitoring": [],
        "safety_notes": [],
        "sources": [],
        "ipm_order": IPM_ORDER,
        "chemical_explanation": None,
    }


def _apply_chemical_safety(result):
    """Make sure we NEVER present an empty chemical-control section."""
    if not result.get("chemical_control"):
        result["chemical_control"] = [CHEMICAL_FALLBACK]
        result["chemical_explanation"] = (
            "No verified chemical recommendation is stored in the "
            "knowledge base. Consult a local agronomist and follow the "
            "product label."
        )


def _finalize_risk(result):
    """Attach the ordered action list, early-stage flag and overall risk."""
    result["management"] = _management_steps(
        result.get("cultural_control", []),
        result.get("mechanical_control", []),
        result.get("biological_control", []),
        result.get("chemical_control", []),
        result.get("monitoring", []) or [
            "Continue monitoring the crop for further spread.",
        ],
    )

    conf_level = (result.get("confidence") or {}).get("level")
    sev_level = (result.get("severity") or {}).get("level")
    weather_level = (result.get("weather_risk") or {}).get("level")

    result["risk_level"] = _risk_level(
        conf_level, sev_level, weather_level
    )
    result["early_stage"] = sev_level in ("LOW", None, "UNKNOWN")


def get_disease_management(crop, disease, confidence=None, severity=None,
                           temperature=None, humidity=None, rainfall=None,
                           location=None):
    """Return structured, data-driven guidance for a detected disease."""
    crop, disease = _split_crop_problem(crop, disease)
    result = _base_result(crop, disease, "disease", confidence, severity,
                          temperature, humidity, rainfall, location)

    # Healthy sample: no disease symptoms are present, so no management is
    # required. Report this clearly rather than returning "not available".
    if "healthy" in _normalize(disease):
        result["in_knowledge_base"] = True
        if not result.get("crop"):
            result["crop"] = crop or "Unknown"
        result["message"] = (
            "No disease symptoms were detected in this sample. "
            "Continue routine scouting and good field hygiene."
        )
        result["prevention"] = [
            "Continue routine scouting for early symptoms.",
            "Maintain field sanitation and balanced fertility.",
            "Re-inspect if symptoms begin to appear.",
        ]
        result["safety_notes"] = GENERAL_SAFETY
        result["sources"] = [{"title": "No disease detected", "url": None}]
        result["risk_level"] = "LOW"
        result["early_stage"] = False
        return result

    record = _find_record(DISEASE_DB, crop, disease)

    if record is None:
        result["message"] = NO_RECORD_MESSAGE
        result["safety_notes"] = GENERAL_SAFETY
        result["management"] = []
        result["risk_level"] = _risk_level(
            (result["confidence"] or {}).get("level"),
            (result["severity"] or {}).get("level"),
            (result["weather_risk"] or {}).get("level"),
        )
        result["early_stage"] = (result["severity"] or {}).get("level") in (
            "LOW", None, "UNKNOWN"
        )
        return result

    result["in_knowledge_base"] = True
    result["message"] = "Management and prevention guidance retrieved."
    if not result.get("crop"):
        result["crop"] = record.get("crop", crop)
    result["pathogen"] = record.get("pathogen")
    result["identification"] = record.get("identification", [])
    result["symptoms"] = record.get("symptoms", [])
    result["early_warning"] = record.get("early_warning", [])
    result["severity_indicators"] = record.get("severity_indicators", [])
    result["favorable_conditions"] = record.get("favorable_conditions", [])
    result["prevention"] = record.get("prevention", [])
    result["cultural_control"] = record.get("cultural_control", [])
    result["mechanical_control"] = record.get("mechanical_control", [])
    result["biological_control"] = record.get("biological_control", [])
    result["chemical_control"] = record.get("chemical_control", [])
    result["monitoring"] = record.get("monitoring", [])
    result["safety_notes"] = (record.get("safety_notes", []) + GENERAL_SAFETY)
    result["sources"] = [{"title": record.get("source", ""), "url": None}]
    _apply_chemical_safety(result)
    _finalize_risk(result)
    return result


def get_pest_management(crop, pest, confidence=None, severity=None,
                        temperature=None, humidity=None, rainfall=None,
                        location=None):
    """Return structured, data-driven guidance for a detected pest."""
    crop, pest = _split_crop_problem(crop, pest)
    result = _base_result(crop, pest, "pest", confidence, severity,
                          temperature, humidity, rainfall, location)
    record = _find_record(PEST_DB, crop, pest, aliases=PEST_ALIASES)

    if record is None:
        result["message"] = NO_RECORD_MESSAGE
        result["safety_notes"] = GENERAL_SAFETY
        result["management"] = []
        result["risk_level"] = _risk_level(
            (result["confidence"] or {}).get("level"),
            (result["severity"] or {}).get("level"),
            (result["weather_risk"] or {}).get("level"),
        )
        result["early_stage"] = (result["severity"] or {}).get("level") in (
            "LOW", None, "UNKNOWN"
        )
        return result

    result["in_knowledge_base"] = True
    result["message"] = "Management and prevention guidance retrieved."
    if not result.get("crop"):
        result["crop"] = record.get("crop", crop)
    result["pest_type"] = record.get("pest_type")
    result["identification"] = record.get("identification", [])
    result["damage_signs"] = record.get("damage_signs", [])
    result["early_warning"] = record.get("early_warning", [])
    result["prevention"] = record.get("prevention", [])
    result["cultural_control"] = record.get("cultural_control", [])
    result["mechanical_control"] = record.get("mechanical_control", [])
    result["biological_control"] = record.get("biological_control", [])
    result["chemical_control"] = record.get("chemical_control", [])
    result["monitoring"] = record.get("monitoring", [])
    result["safety_notes"] = (record.get("safety_notes", []) + GENERAL_SAFETY)
    result["sources"] = [{"title": record.get("source", ""), "url": None}]
    result["severity"]["note"] = record.get(
        "severity_info", result["severity"]["note"]
    )
    _apply_chemical_safety(result)
    _finalize_risk(result)
    return result


def get_management_prevention(crop, problem):
    """Backwards-compatible convenience lookup used by existing callers."""
    record = _find_record(DISEASE_DB, crop, problem) or _find_record(
        PEST_DB, crop, problem
    )
    if record is None:
        return None
    return {
        "crop": record.get("crop", crop),
        "problem": record.get("disease") or record.get("pest", problem),
        "type": record.get("type"),
        "prevention": record.get("prevention", []),
        "management": [
            *record.get("cultural_control", []),
            *record.get("mechanical_control", []),
            *record.get("biological_control", []),
            *record.get("chemical_control", []),
        ],
        "source": record.get("source", ""),
    }
