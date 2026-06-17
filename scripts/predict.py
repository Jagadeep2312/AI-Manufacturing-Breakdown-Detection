import pickle
import pandas as pd

with open(
    "models/model.pkl",
    "rb"
) as file:

    model = pickle.load(file)

temperature = 80
vibration = 2.5
rpm = 900
pressure = 8
runtime = 500

input_data = pd.DataFrame(
    [[
        temperature,
        vibration,
        rpm,
        pressure,
        runtime
    ]],
    columns=
    [
        "Temperature",
        "Vibration",
        "RPM",
        "Pressure",
        "Runtime"
    ]
)

prediction = model.predict(
    input_data
)[0]

if prediction == 0:
    status = "HEALTHY"

elif prediction == 1:
    status = "WARNING"

else:
    status = "FAILURE"

print(
    f"Machine Status: {status}"
)