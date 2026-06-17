import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
df = pd.read_csv("data/machine_data.csv")

print(df.head())
X = df[
    [
        "Temperature",
        "Vibration",
        "RPM",
        "Pressure",
        "Runtime"
    ]
]
y = df["Status"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"Accuracy: {accuracy*100:.2f}%"
)
with open(
    "models/model.pkl",
    "wb"
) as file:
    pickle.dump(model,file)
    import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

df = pd.read_csv(
    "data/machine_data.csv"
)

X = df[
    [
        "Temperature",
        "Vibration",
        "RPM",
        "Pressure",
        "Runtime"
    ]
]

y = df["Status"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"Accuracy: {accuracy*100:.2f}%"
)

with open(
    "models/model.pkl",
    "wb"
) as file:
    pickle.dump(
        model,
        file
    )

print(
    "Model Saved Successfully"
)
import pickle

with open(
    "models/model.pkl",
    "rb"
) as file:
    model = pickle.load(file)

result = model.predict(
    [[80,2.5,900,8,500]]
)

print(result)