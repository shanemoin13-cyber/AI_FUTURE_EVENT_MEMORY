import streamlit as st
import pandas as pd
import pickle
import json
import os

MODEL_FILE = "models/machine_model.pkl"
MEMORY_FILE = "future_memory.json"

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI Future Event Memory",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Future Event Memory")
st.write("AI-powered machine condition and future scenario simulator")

st.divider()

# ==========================================
# LOAD MODEL
# ==========================================

try:
    with open(MODEL_FILE, "rb") as file:
        model = pickle.load(file)

except FileNotFoundError:
    st.error("machine_model.pkl was not found.")
    st.info("Make sure the models folder contains machine_model.pkl")
    st.stop()

# ==========================================
# PREDICTION FUNCTION
# ==========================================

def predict_machine(temperature, vibration, power, speed):

    data = pd.DataFrame(
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

    prediction = model.predict(data)[0]

    probabilities = model.predict_proba(data)[0]

    classes = list(model.classes_)

    if 1 in classes:
        abnormal_index = classes.index(1)
        abnormal_probability = (
            probabilities[abnormal_index] * 100
        )
    else:
        abnormal_probability = 0.0

    return int(prediction), float(abnormal_probability)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🏭 Machine Input")

temperature = st.sidebar.number_input(
    "Temperature (°C)",
    min_value=0.0,
    max_value=200.0,
    value=50.0
)

vibration = st.sidebar.number_input(
    "Vibration",
    min_value=0.0,
    max_value=200.0,
    value=15.0
)

power = st.sidebar.number_input(
    "Power",
    min_value=0.0,
    max_value=300.0,
    value=80.0
)

speed = st.sidebar.number_input(
    "Speed",
    min_value=0.0,
    max_value=5000.0,
    value=1500.0
)

run_prediction = st.sidebar.button(
    "🤖 Run AI Prediction",
    width="stretch"
)

# ==========================================
# CURRENT MACHINE PREDICTION
# ==========================================

st.header("🔍 Current Machine Condition")

if run_prediction:

    prediction, probability = predict_machine(
        temperature,
        vibration,
        power,
        speed
    )

    if prediction == 1:
        status = "⚠️ ABNORMAL"
    else:
        status = "✅ NORMAL"

    health = 100.0 - probability

    if health < 0:
        health = 0.0

    if health > 100:
        health = 100.0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Prediction",
            status
        )

    with col2:
        st.metric(
            "Abnormal Probability",
            f"{probability:.2f}%"
        )

    with col3:
        st.metric(
            "Machine Health",
            f"{health:.2f}%"
        )

    st.progress(int(health))

else:

    st.info(
        "Enter the machine values in the sidebar "
        "and click 'Run AI Prediction'."
    )


# ==========================================
# FUTURE SCENARIOS
# ==========================================

st.divider()

st.header("🔮 Future Scenario Simulation")

scenarios = [
    {
        "name": "Current Condition",
        "temperature": temperature,
        "vibration": vibration,
        "power": power,
        "speed": speed
    },
    {
        "name": "Temperature +10%",
        "temperature": temperature * 1.10,
        "vibration": vibration,
        "power": power,
        "speed": speed
    },
    {
        "name": "Vibration +20%",
        "temperature": temperature,
        "vibration": vibration * 1.20,
        "power": power,
        "speed": speed
    },
    {
        "name": "Power +10%",
        "temperature": temperature,
        "vibration": vibration,
        "power": power * 1.10,
        "speed": speed
    },
    {
        "name": "Speed -10%",
        "temperature": temperature,
        "vibration": vibration,
        "power": power,
        "speed": speed * 0.90
    },
    {
        "name": "Multiple Stress Factors",
        "temperature": temperature * 1.10,
        "vibration": vibration * 1.20,
        "power": power * 1.10,
        "speed": speed * 0.90
    }
]

results = []

for scenario in scenarios:

    prediction, probability = predict_machine(
        scenario["temperature"],
        scenario["vibration"],
        scenario["power"],
        scenario["speed"]
    )

    if prediction == 1:
        result = "⚠️ ABNORMAL"
    else:
        result = "✅ NORMAL"

    results.append({
        "Scenario": scenario["name"],
        "Temperature": round(
            scenario["temperature"], 2
        ),
        "Vibration": round(
            scenario["vibration"], 2
        ),
        "Power": round(
            scenario["power"], 2
        ),
        "Speed": round(
            scenario["speed"], 2
        ),
        "Prediction": result,
        "Abnormal Risk": f"{probability:.2f}%"
    })

scenario_df = pd.DataFrame(results)

st.dataframe(
    scenario_df,
    width="stretch",
    hide_index=True
)


# ==========================================
# RISK CHART
# ==========================================

st.subheader("📊 Future Risk Comparison")

chart_data = scenario_df[
    ["Scenario", "Abnormal Risk"]
].copy()

chart_data["Abnormal Risk"] = (
    chart_data["Abnormal Risk"]
    .str.replace("%", "")
    .astype(float)
)

chart_data = chart_data.set_index("Scenario")

st.bar_chart(chart_data)


# ==========================================
# AI MEMORY
# ==========================================

st.divider()

st.header("🧠 AI Prediction Memory")

if os.path.exists(MEMORY_FILE):

    try:

        with open(MEMORY_FILE, "r") as file:
            memory = json.load(file)

        if isinstance(memory, list) and len(memory) > 0:

            memory_df = pd.DataFrame(memory)

            st.success(
                f"{len(memory)} prediction records stored."
            )

            st.dataframe(
                memory_df,
                width="stretch",
                hide_index=True
            )

        else:

            st.info(
                "No predictions stored yet."
            )

    except Exception:

        st.warning(
            "Memory file is empty or damaged."
        )

else:

    st.info(
        "No predictions stored yet."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Future Event Memory | Machine Prediction Prototype"
)