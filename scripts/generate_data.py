import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

N_CLIENTS = 250
N_ORDERS = 5000

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)

STATUSES = ["Delivered", "Pending", "Returned", "Cancelled"]

def rand_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def main():
    clients = []
    for i in range(1, N_CLIENTS + 1):
        clients.append({
            "client_id": f"C{i:04d}",
            "client_name": fake.company(),
            "region": random.choice(["Northeast", "Midwest", "South", "West"]),
            "created_date": rand_date(START_DATE - timedelta(days=365), START_DATE).date().isoformat()
        })
    df_clients = pd.DataFrame(clients)

    reps = [f"rep_{i:02d}" for i in range(1, 11)]

    orders = []
    comms = []
    for i in range(1, N_ORDERS + 1):
        order_id = f"ORD{i:06d}"
        client = random.choice(clients)
        order_dt = rand_date(START_DATE, END_DATE)
        expected = order_dt + timedelta(days=random.randint(1, 7))

        status = random.choices(
            STATUSES,
            weights=[0.78, 0.14, 0.05, 0.03],
            k=1
        )[0]

        delivery_dt = None
        if status in ["Delivered", "Returned"]:
            if random.random() < 0.2:
                delivery_dt = expected + timedelta(days=random.randint(1, 5))
            else:
                delivery_dt = expected + timedelta(days=random.randint(-1, 2))

        processed_by = random.choice(reps)
        entry_ts = order_dt + timedelta(minutes=random.randint(5, 240))

        rushed = random.random() < 0.15
        accuracy_flag = 0 if (random.random() < (0.06 if rushed else 0.02)) else 1

        orders.append({
            "order_id": order_id,
            "client_id": client["client_id"],
            "order_datetime": order_dt.isoformat(sep=" "),
            "expected_delivery_date": expected.date().isoformat(),
            "delivery_datetime": delivery_dt.isoformat(sep=" ") if delivery_dt else None,
            "status": status,
            "processed_by": processed_by,
            "entry_timestamp": entry_ts.isoformat(sep=" "),
            "is_accurate": accuracy_flag,
            "item_count": int(np.clip(np.random.poisson(3), 1, 15)),
            "order_value_usd": round(float(np.clip(np.random.normal(220, 90), 20, 1200)), 2)
        })

        email_count = int(np.clip(np.random.poisson(1.0), 0, 5))
        call_count = int(np.clip(np.random.poisson(0.6), 0, 3))
        base_resp = np.random.lognormal(mean=1.1, sigma=0.6)
        if rushed:
            base_resp *= 1.2

        comms.append({
            "order_id": order_id,
            "email_count": email_count,
            "call_count": call_count,
            "first_response_time_hours": round(float(np.clip(base_resp, 0.2, 72)), 2),
            "followup_count": int(np.clip(email_count + call_count - 1, 0, 10))
        })

    df_orders = pd.DataFrame(orders)
    df_comms = pd.DataFrame(comms)

    df = df_orders.merge(df_comms, on="order_id", how="left")
    df["is_late"] = np.where(
        (df["delivery_datetime"].notna()) &
        (pd.to_datetime(df["delivery_datetime"]) > pd.to_datetime(df["expected_delivery_date"])),
        1, 0
    )
    df["order_cycle_days"] = np.where(
        df["delivery_datetime"].notna(),
        (pd.to_datetime(df["delivery_datetime"]) - pd.to_datetime(df["order_datetime"])).dt.total_seconds() / 86400,
        np.nan
    )
    df["responded_within_24h"] = np.where(df["first_response_time_hours"] <= 24, 1, 0)

    df_clients.to_csv("data/raw/clients.csv", index=False)
    df_orders.to_csv("data/raw/orders.csv", index=False)
    df_comms.to_csv("data/raw/communications.csv", index=False)
    df.to_csv("data/processed/order_ops_fact.csv", index=False)

    print("✅ Data generated successfully!")

if __name__ == "__main__":
    main()