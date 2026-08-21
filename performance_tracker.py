import json
import os

MEMORY_FILE = "future_memory.json"


# ==========================================
# CHECK MEMORY
# ==========================================

if not os.path.exists(MEMORY_FILE):
    print("No memory file found.")
    print("Run future_scenarios.py first.")
    exit()


# ==========================================
# LOAD MEMORY
# ==========================================

try:

    with open(MEMORY_FILE, "r") as file:
        memory = json.load(file)

except:

    print("Could not read future_memory.json.")
    exit()


if len(memory) == 0:

    print("No predictions stored yet.")
    exit()


# ==========================================
# CALCULATE PERFORMANCE
# ==========================================

total_checked = 0
correct = 0
incorrect = 0


for record in memory:

    if "actual_result" not in record:
        continue

    total_checked += 1

    if record["prediction_correct"] is True:
        correct += 1

    else:
        incorrect += 1


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n======================================")
print("       AI PERFORMANCE TRACKER")
print("======================================")

print(
    f"Total predictions stored: {len(memory)}"
)

print(
    f"Predictions actually checked: "
    f"{total_checked}"
)

print(
    f"Correct predictions: {correct}"
)

print(
    f"Incorrect predictions: {incorrect}"
)


# ==========================================
# ACCURACY
# ==========================================

if total_checked > 0:

    accuracy = (
        correct / total_checked
    ) * 100

    print(
        f"\nHistorical Accuracy: "
        f"{accuracy:.2f}%"
    )

else:

    print(
        "\nHistorical Accuracy: "
        "No verified predictions yet."
    )


# ==========================================
# STATUS
# ==========================================

print("\n======================================")

if total_checked == 0:

    print(
        "STATUS: Waiting for real outcomes."
    )

elif accuracy >= 90:

    print(
        "STATUS: Excellent historical performance."
    )

elif accuracy >= 75:

    print(
        "STATUS: Good historical performance."
    )

elif accuracy >= 50:

    print(
        "STATUS: Moderate historical performance."
    )

else:

    print(
        "STATUS: Needs improvement."
    )

print("======================================")