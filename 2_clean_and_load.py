# Step 2: Clean the data with pandas and load it into a SQLite database
import sqlite3
import pandas as pd

df = pd.read_csv("raw_deliveries.csv")
print("Raw rows:", len(df))

# 1. Remove duplicate orders
df = df.drop_duplicates(subset="order_id")

# 2. Fix hub names (inconsistent upper/lower case)
canonical = {h.lower(): h for h in df["hub"].unique() if h != h.lower()}
df["hub"] = df["hub"].str.lower().map(canonical)

# 3. Fill missing riders
df["rider_id"] = df["rider_id"].fillna("UNKNOWN")

# 4. Fix mixed date formats
def parse_dt(col):
    a = pd.to_datetime(col, format="%Y-%m-%d %H:%M", errors="coerce")
    b = pd.to_datetime(col, format="%d/%m/%Y %H:%M", errors="coerce")
    return a.fillna(b)

for col in ["pickup_time", "promised_time", "delivery_time"]:
    df[col] = parse_dt(df[col])

# 5. Add a useful column: was it on time?
df["on_time"] = ((df["status"] == "Delivered") & (df["delivery_time"] <= df["promised_time"])).astype(int)

print("Clean rows:", len(df))

# Load into SQLite
conn = sqlite3.connect("deliveries.db")
df.to_sql("deliveries", conn, if_exists="replace", index=False)
conn.close()
print("Loaded into deliveries.db")
