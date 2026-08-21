import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

# Load training data
df = pd.read_csv("training_data.csv")

# Input features
X = df[
    [
        "temperature",
        "vibration",
        "power",
        "speed"
    ]
]

# Target
y = df["abnormal"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create AI model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Test
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("AI model trained!")
print("Accuracy:", accuracy)

# Create models folder
os.makedirs("models", exist_ok=True)

# Save model
with open("models/machine_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully!")