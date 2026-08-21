import pickle
import pandas as pd

# Load trained AI model
with open("models/machine_model.pkl", "rb") as file:
    model = pickle.load(file)

print("AI model loaded successfully.")

# Get current machine readings
temperature = float(input("Enter temperature (°C): "))
vibration = float(input("Enter vibration: "))
power = float(input("Enter power: "))
speed = float(input("Enter speed (RPM): "))

# Create input data
data = pd.DataFrame([{
    "temperature": temperature,
    "vibration": vibration,
    "power": power,
    "speed": speed
}])

# Make prediction
prediction = model.predict(data)[0]

# Get probability
probability = model.predict_proba(data)[0][1] * 100

print("\n-----------------------------")

if prediction == 1:
    print("⚠️ ABNORMAL CONDITION DETECTED")
else:
    print("✅ MACHINE CONDITION IS NORMAL")

print(f"Abnormal probability: {probability:.2f}%")
print("-----------------------------")