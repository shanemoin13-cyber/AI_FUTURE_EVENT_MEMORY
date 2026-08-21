from datetime import datetime, timedelta
import uuid
from future_memory import save_event
from confidence_engine import calculate_confidence
def create_future_event(
    event_name,
    probability,
    expected_minutes,
    evidence
):
    event_id = str(uuid.uuid4())[:8]

    current_time = datetime.now()
    expected_time = current_time + timedelta(
        minutes=expected_minutes
    )

    event = {
        "event_id": event_id,
        "event_name": event_name,
        "probability": probability,
        "created_at": current_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "expected_time": expected_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "evidence": evidence,
        "status": "PENDING"
    }

    return event


# Test Future Event

ai_probability = 82.5

final_confidence = calculate_confidence(
    ai_probability
)

event = create_future_event(
    event_name="Performance Degradation",
    probability=final_confidence,
    expected_minutes=30,
    evidence=[
        "Temperature increasing",
        "Vibration increasing",
        "Power consumption increasing"
    ]
)

save_event(event)

print("Future event saved successfully!")

print("\n===== FUTURE EVENT =====")

for key, value in event.items():
    print(f"{key}: {value}")