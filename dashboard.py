import streamlit as st
import pandas as pd
import pickle
from pathlib import Path
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Future Event Memory",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# FIND AI MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "models" / "machine_model.pkl"

# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI Future Event Memory")
st.subheader("AI-Based Machine Condition Prediction System")

st.write(
    "This system analyzes machine sensor values and predicts "
    "whether the current or future machine condition is normal "
    "or abnormal."
)

st.divider()

# ============================================================
# LOAD MODEL
# ============================================================

if not MODEL_FILE.exists():

    st.error("❌ AI model not found!")

    st.write("Expected model location:")

    st.code(str(MODEL_FILE))

    st.write("Your GitHub project should contain:")

    st.code(
        "AI_FUTURE_EVENT_MEMORY/\n"
        "├── dashboard.py\n"
        "├── requirements.txt\n"
        "└── models/\n"
        "    └── machine_model.pkl"
    )

    st.stop()

try:

    with open(MODEL_FILE, "rb") as file:
        model = pickle.load(file)

except Exception as error:

    st.error("❌ Unable to load the AI model.")

    st.code(str(error))

    st.stop()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Machine Input")

temperature = st.sidebar.number_input(
    "Temperature (°C)",
    min_value=0.0,
    max_value=200.0,
    value=50.0,
    step=0.1
)

vibration = st.sidebar.number_input(
    "Vibration",
    min_value=0.0,
    max_value=200.0,
    value=15.0,
    step=0.1
)

power = st.sidebar.number_input(
    "Power",
    min_value=0.0,
    max_value=300.0,
    value=80.0,
    step=0.1
)

speed = st.sidebar.number_input(
    "Speed",
    min_value=0.0,
    max_value=5000.0,
    value=1500.0,
    step=1.0
)

predict_button = st.sidebar.button(
    "🔍 Analyze Machine"
)

# ============================================================
# CREATE INPUT DATA
# ============================================================

input_data = pd.DataFrame(
    [[
        temperature,
        vibration,
        power,
        speed
    ]],
    columns=[
        "temperature",
        "vibration",
        "power",
        "speed"
    ]
)

# ============================================================
# DISPLAY CURRENT SENSOR VALUES
# ============================================================

st.header("📊 Current Machine Condition")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌡️ Temperature",
        f"{temperature:.2f} °C"
    )

with col2:
    st.metric(
        "📳 Vibration",
        f"{vibration:.2f}"
    )

with col3:
    st.metric(
        "⚡ Power",
        f"{power:.2f}"
    )

with col4:
    st.metric(
        "⚙️ Speed",
        f"{speed:.0f} RPM"
    )

st.divider()

# ============================================================
# AI PREDICTION
# ============================================================

if predict_button:

    try:

        prediction = model.predict(input_data)[0]

        # ----------------------------------------------------
        # PROBABILITY
        # ----------------------------------------------------

        abnormal_probability = None
        normal_probability = None

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(
                input_data
            )[0]

            classes = list(model.classes_)

            if 0 in classes:

                normal_index = classes.index(0)

                normal_probability = (
                    probabilities[normal_index] * 100
                )

            if 1 in classes:

                abnormal_index = classes.index(1)

                abnormal_probability = (
                    probabilities[abnormal_index] * 100
                )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        st.header("🤖 AI Result")

        if int(prediction) == 1:

            st.error(
                "⚠️ ABNORMAL MACHINE CONDITION"
            )

            status = "ABNORMAL"

        else:

            st.success(
                "✅ NORMAL MACHINE CONDITION"
            )

            status = "NORMAL"

        # ----------------------------------------------------
        # RESULT METRICS
        # ----------------------------------------------------

        result_col1, result_col2 = st.columns(2)

        with result_col1:

            st.metric(
                "Prediction",
                status
            )

        with result_col2:

            if abnormal_probability is not None:

                st.metric(
                    "Abnormal Probability",
                    f"{abnormal_probability:.2f}%"
                )

        # ----------------------------------------------------
        # PROBABILITY DETAILS
        # ----------------------------------------------------

        st.subheader("📈 AI Confidence")

        if normal_probability is not None:

            st.write(
                f"Normal: **{normal_probability:.2f}%**"
            )

        if abnormal_probability is not None:

            st.write(
                f"Abnormal: **{abnormal_probability:.2f}%**"
            )

        # ----------------------------------------------------
        # INPUT TABLE
        # ----------------------------------------------------

        st.subheader("📋 Sensor Data Used")

        st.dataframe(
            input_data,
            width="stretch"
        )

        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        st.info(
            f"Analysis completed at: {current_time}"
        )

    except Exception as error:

        st.error(
            "❌ Prediction failed."
        )

        st.code(str(error))

# ============================================================
# FUTURE SCENARIO ANALYSIS
# ============================================================

st.divider()

st.header("🔮 Future Scenario Analysis")

st.write(
    "The system tests different future machine conditions "
    "to estimate how the AI model reacts to changing sensor values."
)

scenarios = [

    {
        "Scenario": "Current Condition",
        "Temperature": temperature,
        "Vibration": vibration,
        "Power": power,
        "Speed": speed
    },

    {
        "Scenario": "Temperature +10%",
        "Temperature": temperature * 1.10,
        "Vibration": vibration,
        "Power": power,
        "Speed": speed
    },

    {
        "Scenario": "Vibration +20%",
        "Temperature": temperature,
        "Vibration": vibration * 1.20,
        "Power": power,
        "Speed": speed
    },

    {
        "Scenario": "Power +10%",
        "Temperature": temperature,
        "Vibration": vibration,
        "Power": power * 1.10,
        "Speed": speed
    },

    {
        "Scenario": "Speed -10%",
        "Temperature": temperature,
        "Vibration": vibration,
        "Power": power,
        "Speed": speed * 0.90
    },

    {
        "Scenario": "Multiple Stress Factors",
        "Temperature": temperature * 1.10,
        "Vibration": vibration * 1.20,
        "Power": power * 1.10,
        "Speed": speed * 0.90
    }
]

future_results = []

for scenario in scenarios:

    scenario_data = pd.DataFrame(
        [[
            scenario["Temperature"],
            scenario["Vibration"],
            scenario["Power"],
            scenario["Speed"]
        ]],
        columns=[
            "temperature",
            "vibration",
            "power",
            "speed"
        ]
    )

    try:

        scenario_prediction = model.predict(
            scenario_data
        )[0]

        abnormal_probability = 0.0

        if hasattr(model, "predict_proba"):

            scenario_probabilities = model.predict_proba(
                scenario_data
            )[0]

            scenario_classes = list(
                model.classes_
            )

            if 1 in scenario_classes:

                abnormal_index = scenario_classes.index(1)

                abnormal_probability = (
                    scenario_probabilities[
                        abnormal_index
                    ] * 100
                )

        future_results.append(
            {
                "Scenario": scenario["Scenario"],
                "Temperature": round(
                    scenario["Temperature"], 2
                ),
                "Vibration": round(
                    scenario["Vibration"], 2
                ),
                "Power": round(
                    scenario["Power"], 2
                ),
                "Speed": round(
                    scenario["Speed"], 2
                ),
                "Prediction": (
                    "ABNORMAL"
                    if int(scenario_prediction) == 1
                    else "NORMAL"
                ),
                "Abnormal Probability": round(
                    abnormal_probability, 2
                )
            }
        )

    except Exception as error:

        future_results.append(
            {
                "Scenario": scenario["Scenario"],
                "Temperature": round(
                    scenario["Temperature"], 2
                ),
                "Vibration": round(
                    scenario["Vibration"], 2
                ),
                "Power": round(
                    scenario["Power"], 2
                ),
                "Speed": round(
                    scenario["Speed"], 2
                ),
                "Prediction": "ERROR",
                "Abnormal Probability": 0.0
            }
        )

# ============================================================
# DISPLAY FUTURE RESULTS
# ============================================================

future_df = pd.DataFrame(
    future_results
)

st.dataframe(
    future_df,
    width="stretch"
)

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Future Event Memory | Machine Condition Prediction "
    "and Future Scenario Analysis"
)
