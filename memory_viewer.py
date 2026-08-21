import json
import os


MEMORY_FILE = "future_memory.json"


# ==========================================
# CHECK MEMORY FILE
# ==========================================

if not os.path.exists(MEMORY_FILE):

    print("No future memory found.")

    print(
        "Run future_scenarios.py first."
    )

    exit()


# ==========================================
# LOAD MEMORY
# ==========================================

try:

    with open(MEMORY_FILE, "r") as file:
        memory = json.load(file)

except json.JSONDecodeError:

    print("Memory file is empty or damaged.")

    exit()


# ==========================================
# CHECK MEMORY
# ==========================================

if len(memory) == 0:

    print("No predictions stored yet.")

    exit()


# ==========================================
# DISPLAY HEADER
# ==========================================

print("\n")
print("==============================================================")
print("                 AI FUTURE MEMORY")
print("==============================================================")


# ==========================================
# DISPLAY RECORDS
# ==========================================

for number, record in enumerate(memory, start=1):

    print("\n--------------------------------------------------------------")

    print(
        f"Record: {number}"
    )

    print(
        f"Time: {record.get('timestamp', 'Unknown')}"
    )

    print(
        f"Scenario: {record.get('scenario', 'Unknown')}"
    )

    print(
        f"Temperature: "
        f"{record.get('temperature', 0)} °C"
    )

    print(
        f"Vibration: "
        f"{record.get('vibration', 0)}"
    )

    print(
        f"Power: "
        f"{record.get('power', 0)}"
    )

    print(
        f"Speed: "
        f"{record.get('speed', 0)}"
    )

    prediction = record.get(
        "prediction",
        "Unknown"
    )

    if prediction == 1:

        status = "ABNORMAL"

    elif prediction == 0:

        status = "NORMAL"

    else:

        status = str(prediction)


    print(
        f"AI Prediction: {status}"
    )

    print(
        f"Abnormal Probability: "
        f"{record.get('abnormal_probability', 0)}%"
    )


# ==========================================
# SUMMARY
# ==========================================

print("\n==============================================================")

print(
    f"Total stored predictions: {len(memory)}"
)

print("==============================================================")