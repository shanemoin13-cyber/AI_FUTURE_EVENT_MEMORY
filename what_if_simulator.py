import pickle
import pandas as pd

MODEL_FILE = "models/machine_model.pkl"

# Load AI model
try:
    with open(MODEL_FILE, "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    print("ERROR: machine_model.pkl was not found.")
    exit()

# Get input
print("\n================================")
print("       AI WHAT-IF SIMULATOR")
print("================================")

temperature = float(input("Temperature (°C): "))
vibration = float(input("Vibration: "))
power = float(input("Power: "))
speed = float(input("Speed: "))

# Create input data
data = pd.DataFrame(
    [[temperature, vibration, power, speed]],
    columns=[
        "temperature",
        "vibration",
        "power",
        "speed"
    ]
)

# AI prediction
prediction = model.predict(data)[0]
probabilities = model.predict_proba(data)[0]

# Show probabilities
print("\n================================")
print("       RAW AI PROBABILITIES")
print("================================")

for i, probability_value in enumerate(probabilities):
    print(
        f"Class {model.classes_[i]}: "
        f"{probability_value * 100:.2f}%"
    )

# Find confidence of predicted class
prediction_index = list(model.classes_).index(prediction)

prediction_probability = (
    probabilities[prediction_index] * 100
)

# Result
print("\n================================")
print("          AI RESULT")
print("================================")

print(f"Prediction: {prediction}")

print(
    f"Prediction confidence: "
    f"{prediction_probability:.2f}%"
)

# Interpretation
print("\n================================")
print("       POSSIBLE FUTURE")
print("================================")

if prediction_probability >= 80:
    print("The AI has high confidence in this prediction.")

elif prediction_probability >= 60:
    print("The AI has moderate confidence in this prediction.")

else:
    print("The AI has low confidence in this prediction.")

print("\n================================")