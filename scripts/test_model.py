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