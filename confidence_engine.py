import json

FILE_NAME = "future_memory.json"


def get_historical_accuracy():

    try:
        with open(FILE_NAME, "r") as file:
            memory = json.load(file)

    except FileNotFoundError:
        return 50.0

    correct = 0
    completed = 0

    for event in memory:

        if event["status"] == "CORRECT":
            correct += 1
            completed += 1

        elif event["status"] == "INCORRECT":
            completed += 1

    if completed == 0:
        return 50.0

    accuracy = (correct / completed) * 100

    return accuracy


def calculate_confidence(ai_probability):

    historical_accuracy = get_historical_accuracy()

    adjusted_confidence = (
        ai_probability + historical_accuracy
    ) / 2

    return adjusted_confidence


# Test the confidence engine

ai_probability = 82.5

historical_accuracy = get_historical_accuracy()

confidence = calculate_confidence(
    ai_probability
)

print("\n==============================")
print("      CONFIDENCE ENGINE")
print("==============================")

print(
    f"AI probability: {ai_probability:.2f}%"
)

print(
    f"Historical accuracy: "
    f"{historical_accuracy:.2f}%"
)

print(
    f"Adjusted confidence: "
    f"{confidence:.2f}%"
)