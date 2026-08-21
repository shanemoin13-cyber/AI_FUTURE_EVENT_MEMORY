import json

FILE_NAME = "future_memory.json"


def analyze_predictions():

    try:
        with open(FILE_NAME, "r") as file:
            memory = json.load(file)

    except FileNotFoundError:
        print("Future memory file not found.")
        return

    if not memory:
        print("No predictions available.")
        return

    total = 0
    correct = 0
    incorrect = 0
    pending = 0

    for event in memory:

        status = event["status"]

        if status == "CORRECT":

            correct += 1
            total += 1

        elif status == "INCORRECT":

            incorrect += 1
            total += 1

        elif status == "PENDING":

            pending += 1

    print("\n==============================")
    print("     PREDICTION ANALYSIS")
    print("==============================")

    print("Total completed predictions:", total)
    print("Correct predictions:", correct)
    print("Incorrect predictions:", incorrect)
    print("Pending predictions:", pending)

    if total > 0:

        accuracy = (correct / total) * 100

        print(
            f"Prediction accuracy: {accuracy:.2f}%"
        )

    else:

        print("Not enough completed predictions.")


analyze_predictions()