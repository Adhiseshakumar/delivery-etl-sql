# Step 1: Create a messy fake delivery dataset (no real company data)
import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)
hubs = ["Bengaluru-Koramangala", "Bengaluru-Whitefield", "Chennai-Guindy", "Hyderabad-Gachibowli", "Mumbai-Andheri"]
cities = {"Bengaluru-Koramangala": "Bengaluru", "Bengaluru-Whitefield": "Bengaluru",
          "Chennai-Guindy": "Chennai", "Hyderabad-Gachibowli": "Hyderabad", "Mumbai-Andheri": "Mumbai"}
riders = [f"R{str(i).zfill(3)}" for i in range(1, 61)]
statuses = ["Delivered", "Delivered", "Delivered", "Delivered", "Failed", "RTO"]
fail_reasons = ["Customer unavailable", "Wrong address", "Refused", "Phone unreachable"]

rows = []
start = datetime(2026, 1, 1)
for i in range(1, 20001):
    hub = random.choice(hubs)
    pickup = start + timedelta(minutes=random.randint(0, 60 * 24 * 90))
    promised = pickup + timedelta(hours=random.choice([4, 6, 24]))
    status = random.choice(statuses)
    delay = random.randint(-120, 300)
    delivered = pickup + timedelta(minutes=random.randint(60, 600) + max(delay, 0))
    rows.append({
        "order_id": f"ORD{i:06d}",
        "hub": hub,
        "city": cities[hub],
        "rider_id": random.choice(riders),
        "pickup_time": pickup.strftime("%Y-%m-%d %H:%M"),
        "promised_time": promised.strftime("%Y-%m-%d %H:%M"),
        "delivery_time": delivered.strftime("%d/%m/%Y %H:%M") if random.random() < 0.1 else delivered.strftime("%Y-%m-%d %H:%M"),
        "status": status,
        "fail_reason": random.choice(fail_reasons) if status != "Delivered" else None,
    })

df = pd.DataFrame(rows)

# Make it messy on purpose
df = pd.concat([df, df.sample(300, random_state=1)], ignore_index=True)           # duplicates
df.loc[df.sample(frac=0.03, random_state=2).index, "rider_id"] = None   # missing riders
df.loc[df.sample(frac=0.05, random_state=3).index, "hub"] = df["hub"].str.lower()  # inconsistent case
df = df.sample(frac=1, random_state=4).reset_index(drop=True)

df.to_csv("raw_deliveries.csv", index=False)
print("Created raw_deliveries.csv with", len(df), "rows")
