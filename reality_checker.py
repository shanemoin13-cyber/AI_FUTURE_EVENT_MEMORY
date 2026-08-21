import json
import os
from datetime import datetime

MEMORY_FILE = "future_memory.json"


print("\n======================================")
print("          AI REALITY CHECKER")
print("======================================")

# Load prediction memory
if not os.path.exists(MEMORY_FILE):
    print("\nNo prediction memory found.")
    print("Run the future scenario generator first.")
    input("\nPress Enter to exit...")
    exit()

try:
    with open(MEMORY_FILE, "r") as file:
        memory = json.load(file)
except (json.JSONDecodeError, OSError):
    print("\nMemory file is empty or damaged.")
    input("\nPress Enter to exit...")
    exit()

if not memory:
    print("\nNo prediction records found.")
    input("\nPress Enter to exit...")
    exit()

print(f"\nFound {len(memory)} prediction records.")

# Show records
for i, record in enumerate(memory, start=1):

    scenario = record.get("scenario", "Unknown")
    prediction = record.get("prediction", 0)
    probability = record.get("abnormal_probability", 0)

    prediction_text = (
        "ABNORMAL"
        if int(prediction) == 1
        else "NORMAL"
    )

    print("\n--------------------------------------")
    print(f"Record: {i}")
    print(f"Scenario: {scenario}")
    print(f"AI Prediction: {prediction_text}")
    print(f"Abnormal Probability: {probability:.2f}%")

# Select record
print("\n======================================")

try:
    choice = int(
        input(
            f"Select prediction record (1-{len(memory)}): "
        )
    )

    if choice < 1 or choice > len(memory):
        raise ValueError

except ValueError:
    print("\nInvalid record number.")
    input("\nPress Enter to exit...")
    exit()

record = memory[choice - 1]

# Actual result
print("\n======================================")
print("          ACTUAL MACHINE RESULT")
print("======================================")

actual = input(
    "Enter actual result (0 = NORMAL, 1 = ABNORMAL): "
).strip()

if actual not in ["0", "1"]:
    print("\nPlease enter only 0 or 1.")
    input("\nPress Enter to exit...")
    exit()

actual = int(actual)

predicted = int(record.get("prediction", 0))

# Compare
correct = predicted == actual

if correct:
    result = "CORRECT"
else:
    result = "INCORRECT"

# Save reality result
record["actual_result"] = actual
record["prediction_correct"] = correct
record["checked_at"] = datetime.now().isoformat()

memory[choice - 1] = record

with open(MEMORY_FILE, "w") as file:
    json.dump(memory, file, indent=4)

# Display result
print("\n======================================")
print("             REALITY CHECK")
print("======================================")

print(
    "AI Prediction: ",
    "ABNORMAL" if predicted == 1 else "NORMAL"
)

print(
    "Actual Result: ",
    "ABNORMAL" if actual == 1 else "NORMAL"
)

print(f"Result: {result}")

print("\nReality check saved successfully.")

print("======================================")