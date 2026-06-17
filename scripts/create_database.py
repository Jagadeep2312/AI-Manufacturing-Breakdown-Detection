import sqlite3

conn = sqlite3.connect(
    "database/machine.db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS MachineData (

id INTEGER PRIMARY KEY AUTOINCREMENT,

temperature REAL,

vibration REAL,

rpm REAL,

pressure REAL,

runtime REAL,

prediction INTEGER,

timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()

conn.close()

print(
    "Database Created Successfully"
)