import pandas as pd
import random

data = []

# Normal machine conditions
for _ in range(1000):
    temperature = random.uniform(40, 60)
    vibration = random.uniform(10, 25)
    power = random.uniform(70, 90)
    speed = random.uniform(1400, 1600)

    data.append([
        temperature, vibration, power, speed, 0
    ])


# Abnormal machine conditions
for _ in range(1000):
    temperature = random.uniform(65, 90)
    vibration = random.uniform(30, 50)
    power = random.uniform(95, 120)
    speed = random.uniform(1100, 1350)

    data.append([
        temperature, vibration, power, speed, 1
    ])


df = pd.DataFrame(
    data,
    columns=[
        "temperature",
        "vibration",
        "power",
        "speed",
        "abnormal"
    ]
)

df = df.sample(frac=1).reset_index(drop=True)

df.to_csv("training_data.csv", index=False)

print("Training data created successfully!")
print(df.head())
print("\nTotal records:", len(df))