import json
import os

FILE_NAME = "future_memory.json"


def save_event(event):

    if os.path.exists(FILE_NAME):

        with open(FILE_NAME, "r") as file:
            memory = json.load(file)

    else:
        memory = []

    memory.append(event)

    with open(FILE_NAME, "w") as file:
        json.dump(memory, file, indent=4)


def show_memory():

    if not os.path.exists(FILE_NAME):
        print("No future events found.")
        return

    with open(FILE_NAME, "r") as file:
        memory = json.load(file)

    print("\n===== FUTURE MEMORY =====")

    for event in memory:

        print("\nEvent:", event["event_name"])
        print("Probability:", event["probability"], "%")
        print("Expected Time:", event["expected_time"])
        print("Status:", event["status"])