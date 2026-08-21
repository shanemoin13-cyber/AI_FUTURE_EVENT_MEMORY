import pickle
import pandas as pd
import json
import os
from datetime import datetime

MODEL_FILE = "models/machine_model.pkl"
MEMORY_FILE = "future_memory.json"

# LOAD MODEL
try:
    with open(MODEL_FILE, "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    print("ERROR: machine_model.pkl not found.")
    exit()

# INPUT
print("\n======================================")
print("       FUTURE SCENARIO GENERATOR")
print("======================================")

temperature = float(input("Current Temperature (°C): "))
vibration = float(input("Current Vibration: "))
power = float(input("Current Power: "))
speed = float(input("Current Speed: "))

# SCENARIOS
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

# LOAD MEMORY
if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE, "r") as file:
            memory = json.load(file)

        if not isinstance(memory, list):
            memory = []

    except:
        memory = []
else:
    memory = []

# ANALYSIS
print("\n======================================")
print("          AI FUTURE ANALYSIS")
print("======================================")

for scenario in scenarios:

    data = pd.DataFrame(
        [[
            scenario["temperature"],
            scenario["vibration"],
            scenario["power"],
            scenario["speed"]
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

    abnormal_index = list(model.classes_).index(1)

    abnormal_probability = (
        probabilities[abnormal_index] * 100
    )

    # SAVE RECORD
    record = {
        "timestamp": datetime.now().isoformat(),
        "scenario": scenario["name"],
        "temperature": round(scenario["temperature"], 2),
        "vibration": round(scenario["vibration"], 2),
        "power": round(scenario["power"], 2),
        "speed": round(scenario["speed"], 2),
        "prediction": int(prediction),
        "abnormal_probability": round(
            abnormal_probability, 2
        )
    }

    memory.append(record)

    # DISPLAY
    print("\n--------------------------------------")
    print(f"Scenario: {scenario['name']}")
    print(f"Temperature: {scenario['temperature']:.2f}")
    print(f"Vibration: {scenario['vibration']:.2f}")
    print(f"Power: {scenario['power']:.2f}")
    print(f"Speed: {scenario['speed']:.2f}")
    print(f"AI Prediction: {prediction}")
    print(
        f"Abnormal Probability: "
        f"{abnormal_probability:.2f}%"
    )

# SAVE MEMORY
with open(MEMORY_FILE, "w") as file:
    json.dump(memory, file, indent=4)

print("\n======================================")
print("       FUTURE ANALYSIS COMPLETE")
print("======================================")

print("\nFuture predictions saved successfully.")
print("Memory file:", MEMORY_FILE)
print("Total stored predictions:", len(memory))

print("======================================")