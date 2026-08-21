import random
import pandas as pd

data = []

for time in range(1000):

    temperature = random.uniform(40, 60)
    vibration = random.uniform(10, 25)
    power = random.uniform(70, 90)
    speed = random.uniform(1400, 1600)

    data.append({
        "time": time,
        "temperature": temperature,
        "vibration": vibration,
        "power": power,
        "speed": speed
    })

df = pd.DataFrame(data)

df.to_csv("machine_data.csv", index=False)

print("Machine data generated successfully!")
print(df.head())