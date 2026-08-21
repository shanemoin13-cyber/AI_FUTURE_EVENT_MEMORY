import streamlit as st
import pandas as pd
import pickle
import json
import os
from datetime import datetime


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Future Event Memory",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# FILE PATHS
# =========================================================

MODEL_FILE = "models/machine_model.pkl"
MEMORY_FILE = "future_memory.json"


# =========================================================
# LOAD AI MODEL
# =========================================================

@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_FILE):
        return None

    try:
        with open(MODEL_FILE, "rb") as file:
            return pickle.load(file)

    except Exception:
        return None


model = load_model()


# =========================================================
# MODEL CHECK
# =========================================================

if model is None:

    st.error(
        "AI model not found.\n\n"
        "Make sure this file exists:\n"
        "models/machine_model.pkl"
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.title("🤖 AI Future Event Memory")

st.write(
    "AI-powered machine condition monitoring, "
    "future scenario simulation, risk analysis "
    "and prediction memory."
)

st.divider()


# =========================================================
# SIDEBAR MACHINE INPUT
# =========================================================

st.sidebar.header("⚙️ Machine Input")


temperature = st.sidebar.number_input(
    "Temperature (°C)",
    min_value=0.0,
    max_value=200.0,
    value=50.0,
    step=1.0
)


vibration = st.sidebar.number_input(
    "Vibration",
    min_value=0.0,
    max_value=100.0,
    value=15.0,
    step=1.0
)


power = st.sidebar.number_input(
    "Power",
    min_value=0.0,
    max_value=200.0,
    value=80.0,
    step=1.0
)


speed = st.sidebar.number_input(
    "Speed",
    min_value=0.0,
    max_value=5000.0,
    value=1500.0,
    step=50.0
)


run_prediction = st.sidebar.button(
    "🔮 Run AI Prediction",
    width="stretch"
)


# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict_machine(
    temp,
    vib,
    pwr,
    spd
):

    data = pd.DataFrame(
        [[
            temp,
            vib,
            pwr,
            spd
        ]],
        columns=[
            "temperature",
            "vibration",
            "power",
            "speed"
        ]
    )


    prediction = int(
        model.predict(data)[0]
    )


    abnormal_probability = 0.0


    if hasattr(
        model,
        "predict_proba"
    ):

        probabilities = (
            model.predict_proba(data)[0]
        )


        classes = list(
            model.classes_
        )


        if 1 in classes:

            abnormal_index = (
                classes.index(1)
            )


            abnormal_probability = (
                probabilities[
                    abnormal_index
                ] * 100
            )


    return (
        prediction,
        abnormal_probability
    )


# =========================================================
# CURRENT MACHINE PREDICTION
# =========================================================

prediction, abnormal_probability = (
    predict_machine(
        temperature,
        vibration,
        power,
        speed
    )
)


if prediction == 1:

    status = "⚠️ ABNORMAL"

else:

    status = "✅ NORMAL"


machine_health = max(
    0,
    100 - abnormal_probability
)


# =========================================================
# CURRENT MACHINE CONDITION
# =========================================================

st.header(
    "🔎 Current Machine Condition"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "AI Prediction",
        status
    )


with col2:

    st.metric(
        "Abnormal Probability",
        f"{abnormal_probability:.2f}%"
    )


with col3:

    st.metric(
        "Machine Health",
        f"{machine_health:.2f}%"
    )


st.progress(
    int(
        max(
            0,
            min(
                100,
                machine_health
            )
        )
    )
)


st.divider()


# =========================================================
# FUTURE SCENARIOS
# =========================================================

st.header(
    "🔮 Future Scenario Simulation"
)


scenarios = [

    {
        "Scenario": "Current Condition",

        "temperature": temperature,

        "vibration": vibration,

        "power": power,

        "speed": speed
    },


    {
        "Scenario": "Temperature +10%",

        "temperature": temperature * 1.10,

        "vibration": vibration,

        "power": power,

        "speed": speed
    },


    {
        "Scenario": "Vibration +20%",

        "temperature": temperature,

        "vibration": vibration * 1.20,

        "power": power,

        "speed": speed
    },


    {
        "Scenario": "Power +10%",

        "temperature": temperature,

        "vibration": vibration,

        "power": power * 1.10,

        "speed": speed
    },


    {
        "Scenario": "Speed -10%",

        "temperature": temperature,

        "vibration": vibration,

        "power": power,

        "speed": speed * 0.90
    },


    {
        "Scenario": "Multiple Stress Factors",

        "temperature": temperature * 1.10,

        "vibration": vibration * 1.20,

        "power": power * 1.10,

        "speed": speed * 0.90
    }

]


# =========================================================
# ANALYZE FUTURE SCENARIOS
# =========================================================

results = []


for scenario in scenarios:

    pred, probability = (
        predict_machine(
            scenario["temperature"],
            scenario["vibration"],
            scenario["power"],
            scenario["speed"]
        )
    )


    if pred == 1:

        prediction_text = (
            "⚠️ ABNORMAL"
        )

    else:

        prediction_text = (
            "✅ NORMAL"
        )


    results.append({

        "Scenario":
            scenario["Scenario"],

        "Temperature":
            round(
                scenario["temperature"],
                2
            ),

        "Vibration":
            round(
                scenario["vibration"],
                2
            ),

        "Power":
            round(
                scenario["power"],
                2
            ),

        "Speed":
            round(
                scenario["speed"],
                2
            ),

        "Prediction":
            prediction_text,

        "Abnormal Probability":
            round(
                probability,
                2
            )
    })


results_df = pd.DataFrame(
    results
)


# =========================================================
# FUTURE SCENARIO TABLE
# =========================================================

st.dataframe(
    results_df,
    width="stretch",
    hide_index=True
)


st.divider()


# =========================================================
# FUTURE RISK COMPARISON
# =========================================================

st.header(
    "📊 Future Risk Comparison"
)


chart_df = results_df[
    [
        "Scenario",
        "Abnormal Probability"
    ]
].copy()


chart_df = chart_df.set_index(
    "Scenario"
)


st.bar_chart(
    chart_df,
    y="Abnormal Probability",
    width="stretch"
)


# =========================================================
# HIGHEST FUTURE RISK
# =========================================================

highest_risk = results_df.loc[
    results_df[
        "Abnormal Probability"
    ].idxmax()
]


risk_probability = (
    highest_risk[
        "Abnormal Probability"
    ]
)


risk_scenario = (
    highest_risk[
        "Scenario"
    ]
)


st.subheader(
    "🚨 Highest Future Risk"
)


if risk_probability >= 70:

    st.error(
        f"High future risk detected: "
        f"**{risk_scenario}** "
        f"({risk_probability:.2f}% "
        f"abnormal probability)"
    )


elif risk_probability >= 30:

    st.warning(
        f"Moderate future risk: "
        f"**{risk_scenario}** "
        f"({risk_probability:.2f}% "
        f"abnormal probability)"
    )


else:

    st.success(
        f"Low future risk. "
        f"Highest scenario is "
        f"**{risk_scenario}** "
        f"at {risk_probability:.2f}%."
    )


st.divider()


# =========================================================
# LOAD EXISTING MEMORY
# =========================================================

memory = []


if os.path.exists(
    MEMORY_FILE
):

    try:

        with open(
            MEMORY_FILE,
            "r"
        ) as file:

            loaded_memory = json.load(
                file
            )


        if isinstance(
            loaded_memory,
            list
        ):

            memory = loaded_memory

    except Exception:

        memory = []


# =========================================================
# SAVE NEW PREDICTIONS
# =========================================================

if run_prediction:

    for result in results:

        if "ABNORMAL" in (
            result["Prediction"]
        ):

            prediction_value = 1

        else:

            prediction_value = 0


        record = {

            "timestamp":
                datetime.now().isoformat(),

            "scenario":
                result["Scenario"],

            "temperature":
                result["Temperature"],

            "vibration":
                result["Vibration"],

            "power":
                result["Power"],

            "speed":
                result["Speed"],

            "prediction":
                prediction_value,

            "abnormal_probability":
                result[
                    "Abnormal Probability"
                ]
        }


        memory.append(
            record
        )


    with open(
        MEMORY_FILE,
        "w"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4
        )


    st.success(
        "✅ Future predictions "
        "saved successfully."
    )


# =========================================================
# AI PREDICTION MEMORY
# =========================================================

st.header(
    "🧠 AI Prediction Memory"
)


if len(memory) > 0:

    st.success(
        f"{len(memory)} prediction "
        f"records stored."
    )


    memory_df = pd.DataFrame(
        memory
    )


    st.dataframe(
        memory_df,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No prediction stored yet. "
        "Click 'Run AI Prediction'."
    )


# =========================================================
# PREDICTION ACCURACY
# =========================================================

st.divider()

st.header(
    "🎯 Prediction Accuracy"
)


checked_records = []


for record in memory:

    if (
        "actual_result" in record
        and
        "prediction_correct" in record
    ):

        checked_records.append(
            record
        )


if len(checked_records) == 0:

    st.info(
        "No reality-checked "
        "predictions yet."
    )


    st.write(
        "Use reality_checker.py "
        "to compare AI predictions "
        "with actual machine results."
    )


else:

    total_checked = len(
        checked_records
    )


    correct_predictions = sum(
        1
        for record
        in checked_records
        if record[
            "prediction_correct"
        ]
    )


    incorrect_predictions = (
        total_checked
        -
        correct_predictions
    )


    accuracy = (
        correct_predictions
        /
        total_checked
        *
        100
    )


    col1, col2, col3, col4 = (
        st.columns(4)
    )


    with col1:

        st.metric(
            "Checked Predictions",
            total_checked
        )


    with col2:

        st.metric(
            "Correct",
            correct_predictions
        )


    with col3:

        st.metric(
            "Incorrect",
            incorrect_predictions
        )


    with col4:

        st.metric(
            "Accuracy",
            f"{accuracy:.2f}%"
        )


    accuracy_df = pd.DataFrame({

        "Result": [
            "Correct",
            "Incorrect"
        ],

        "Count": [
            correct_predictions,
            incorrect_predictions
        ]

    })


    st.subheader(
        "📈 Accuracy Overview"
    )


    st.bar_chart(
        accuracy_df.set_index(
            "Result"
        ),
        y="Count",
        width="stretch"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "AI Future Event Memory | "
    "Machine Prediction | "
    "Future Scenario Simulation | "
    "Risk Analysis | "
    "Prediction Memory | "
    "Reality Checking"
)