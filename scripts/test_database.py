import sqlite3

conn = sqlite3.connect(
    "database/machine.db"
)

cursor = conn.cursor()

cursor.execute("""
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
45,
0.4,
1500,
5,
120,
0
)
""")

conn.commit()

conn.close()

print(
    "Record Inserted"
)