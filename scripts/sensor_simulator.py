import random
import time
import sqlite3
import pickle
import pandas as pd


# ==================================
# Load Trained AI Model
# ==================================

with open("models/model.pkl", "rb") as file:
    model = pickle.load(file)


# ==================================
# Generate Virtual Sensor Data
# ==================================

def generate_sensor_data():

    temperature = round(
        random.uniform(30, 90), 2
    )

    vibration = round(
        random.uniform(0.1, 3.0), 2
    )

    rpm = round(
        random.uniform(800, 1800), 2
    )

    pressure = round(
        random.uniform(3, 10), 2
    )

    runtime = round(
        random.uniform(0, 1000), 2
    )

    return (
        temperature,
        vibration,
        rpm,
        pressure,
        runtime
    )


# ==================================
# Failure Probability
# ==================================

def failure_probability(
    temperature,
    vibration,
    rpm
):

    score = 0

    if temperature > 60:
        score += 30

    if vibration > 1.2:
        score += 30

    if rpm < 1000:
        score += 40

    return min(score, 100)


# ==================================
# Connect Database
# ==================================

conn = sqlite3.connect(
    "database/machine.db"
)

cursor = conn.cursor()

print("=" * 50)
print("AI MACHINE MONITORING STARTED")
print("=" * 50)


# ==================================
# Continuous Monitoring
# ==================================

while True:

    (
        temperature,
        vibration,
        rpm,
        pressure,
        runtime
    ) = generate_sensor_data()

    # ------------------------------
    # Prepare AI Input
    # ------------------------------

    input_data = pd.DataFrame(
        [[
            temperature,
            vibration,
            rpm,
            pressure,
            runtime
        ]],
        columns=[
            "Temperature",
            "Vibration",
            "RPM",
            "Pressure",
            "Runtime"
        ]
    )

    # ------------------------------
    # AI Prediction
    # ------------------------------

    prediction = model.predict(
        input_data
    )[0]

    # ------------------------------
    # Convert Number to Text
    # ------------------------------

    if prediction == 0:
        status = "HEALTHY"

    elif prediction == 1:
        status = "WARNING"

    else:
        status = "FAILURE"

    # ------------------------------
    # Failure Probability
    # ------------------------------

    probability = failure_probability(
        temperature,
        vibration,
        rpm
    )

    # ------------------------------
    # Store in Database
    # ------------------------------

    cursor.execute(
        """
        INSERT INTO MachineData
        (
            temperature,
            vibration,
            rpm,
            pressure,
            runtime,
            prediction
        )

        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        """,
        (
            temperature,
            vibration,
            rpm,
            pressure,
            runtime,
            prediction
        )
    )

    conn.commit()

    # ------------------------------
    # Display Results
    # ------------------------------

    print("\n")
    print("-" * 50)

    print(
        f"Temperature : {temperature} °C"
    )

    print(
        f"Vibration   : {vibration}"
    )

    print(
        f"RPM         : {rpm}"
    )

    print(
        f"Pressure    : {pressure}"
    )

    print(
        f"Runtime     : {runtime}"
    )

    print(
        f"AI Status   : {status}"
    )

    print(
        f"Failure Probability : {probability}%"
    )

    print("-" * 50)

    time.sleep(5)