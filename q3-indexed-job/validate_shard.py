import os
import re
import csv
import json
import socket
import time

completion_index = int(os.environ.get("JOB_COMPLETION_INDEX", "0"))

pod_name = os.environ.get("POD_NAME", socket.gethostname())
node_name = os.environ.get("NODE_NAME", "unknown")

shard_path = f"/data/shard_{completion_index}.csv"

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_row_invalid(row):
    if not row["first_name"] or not row["last_name"] or not row["email"]:
        return True
    if not EMAIL_PATTERN.match(row["email"]):
        return True
    return False

total_rows = 0
invalid_rows = 0

with open(shard_path, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_rows += 1
        if is_row_invalid(row):
            invalid_rows += 1

result = {
    "completion_index": completion_index,
    "shard_file": f"shard_{completion_index}.csv",
    "total_rows": total_rows,
    "invalid_rows": invalid_rows,
    "pod_name": pod_name,
    "node_name": node_name,
}

print("RESULT_JSON:" + json.dumps(result))
