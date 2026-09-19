from kubernetes import client, config
import re
import json

config.load_kube_config()
v1 = client.CoreV1Api()

pods = v1.list_namespaced_pod(
    namespace="default", label_selector="job-name=shard-validation-job"
)

results = []
for pod in pods.items:
    logs = v1.read_namespaced_pod_log(pod.metadata.name, "default")
    match = re.search(r"RESULT_JSON:(\{.*\})", logs)
    result = json.loads(match.group(1))
    results.append(result)

results.sort(key=lambda r: r["completion_index"])

total_invalid = 0
for r in results:
    print(f"shard {r['completion_index']}: "
          f"{r['invalid_rows']} invalid / {r['total_rows']} total rows "
          f"(pod {r['pod_name']} on node {r['node_name']})")
    total_invalid += r["invalid_rows"]

print(f"\nTotal invalid rows across all 8 shards: {total_invalid}")