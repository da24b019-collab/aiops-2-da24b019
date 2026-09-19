"""
generate_shards.py

Generates 8 synthetic CSV shards of user signup records. Each shard has
a known, seeded number of deliberately invalid rows (bad email format
or a missing required field), so we can verify the validator's output
against ground truth.
"""

import random
import csv
import os

random.seed(42)

NUM_SHARDS = 8
ROWS_PER_SHARD = 50

FIRST_NAMES = ["Alice", "Bob", "Charlie", "Dana", "Evan", "Fiona", "George", "Hana"]
LAST_NAMES = ["Smith", "Jones", "Lee", "Patel", "Garcia", "Kim", "Brown", "Diaz"]
DOMAINS = ["example.com", "mail.com", "test.org"]

os.makedirs("shards", exist_ok=True)

for shard_id in range(NUM_SHARDS):
    filepath = f"shards/shard_{shard_id}.csv"
    # Deliberately vary how many invalid rows each shard gets, but keep it
    # deterministic (seeded) so we know the ground truth ahead of time.
    num_invalid = (shard_id % 4) + 1  # 1 to 4 invalid rows per shard

    rows = []
    for i in range(ROWS_PER_SHARD):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        email = f"{first.lower()}.{last.lower()}@{random.choice(DOMAINS)}"
        signup_id = f"{shard_id}-{i}"
        rows.append([signup_id, first, last, email])

    # Now deliberately corrupt exactly `num_invalid` rows in this shard
    invalid_indices = random.sample(range(ROWS_PER_SHARD), num_invalid)
    for idx in invalid_indices:
        corruption_type = random.choice(["bad_email", "missing_field"])
        if corruption_type == "bad_email":
            rows[idx][3] = "not-an-email"  # malformed email, no @ or domain
        else:
            rows[idx][1] = ""  # missing first name

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["signup_id", "first_name", "last_name", "email"])
        writer.writerows(rows)

    print(f"shard_{shard_id}.csv: {ROWS_PER_SHARD} rows, {num_invalid} deliberately invalid")