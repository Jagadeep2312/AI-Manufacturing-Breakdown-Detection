import pandas as pd
import numpy as np

np.random.seed(42)

rows = 5000

temperature = []
vibration = []
rpm = []
pressure = []
runtime = []
status = []

for i in range(rows):

    temp = np.random.uniform(30,90)
    vib = np.random.uniform(0.1,3.0)
    r = np.random.uniform(800,1800)
    pres = np.random.uniform(3,10)
    run = np.random.uniform(0,1000)

    if temp > 75 or vib > 2.0 or r < 1000:
        s = 2

    elif temp > 60 or vib > 1.2:
        s = 1

    else:
        s = 0

    temperature.append(round(temp,2))
    vibration.append(round(vib,2))
    rpm.append(round(r,2))
    pressure.append(round(pres,2))
    runtime.append(round(run,2))
    status.append(s)

df = pd.DataFrame({
    "Temperature":temperature,
    "Vibration":vibration,
    "RPM":rpm,
    "Pressure":pressure,
    "Runtime":runtime,
    "Status":status
})

df.to_csv("data/machine_data.csv",index=False)

print("Dataset Created Successfully")
print(df.head())
print(df.shape)
print(df["Status"].value_counts())