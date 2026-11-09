import pandas as pd
import sqlite3 as sql

df = pd.read_csv("data/processed/chss_cleaned.csv")
print(df.head().to_string())

sql.connect("wellnessiq.db")

conn = sql.connect("wellnessiq.db")

print("Database connection successful!")

df.to_sql("seniors", conn, if_exists="replace", index = False)

conn.close()



