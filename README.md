# AIOps Module 3 Assignment

**Author:** Dhanush (DA24B019)
**Course:** AI Operations (AIOps)

This repository contains the work for all four questions of the Module 3 assignment.

---

## Question 1 — Naive vs Multi-Stage Docker Build

**Folder:** `q1/`

Packages the spam detection API two ways: a naive single-stage Dockerfile, and a multi-stage rewrite that separates the build environment (where dependencies are compiled) from the runtime environment. Both images are verified to serve identical `/predict` and `/healthz` behavior.


**To reproduce:**
```bash
cd q1
docker build -t spam-api-naive -f Dockerfile .
docker build -t spam-api-multistage -f Dockerfile.multistage .
docker images | grep spam-api

docker run -d -p 8000:8000 spam-api-naive
curl http://localhost:8000/healthz
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text":"WIN a FREE iPhone now! Click here"}'
```



---

## Question 2 — Docker Compose with Redis Caching

**Folder:** `q2/`

Extends the API with a Redis cache checked before every prediction, and orchestrates the two containers (`api`, `cache`) with Docker Compose, connected over Compose's internal network using the service name `cache` as the hostname.


**To reproduce:**
```bash
cd q2
docker compose up -d
docker compose ps

time curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text":"Congratulations you won a laptop"}'
time curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text":"Congratulations you won a laptop"}'
```



---

## Question 3 — Kubernetes Indexed Job for Parallel Shard Validation

**Folder:** `q3-indexed-job/`

An Indexed Job where each of 8 pods validates exactly one CSV shard of signup records (malformed emails, missing required fields) and reports an invalid-row count, read via `JOB_COMPLETION_INDEX`.


**To reproduce:**
```bash
cd q3-indexed-job
kubectl apply -f validate-job.yaml
kubectl get pods -o wide --watch
kubectl logs -l job-name=validate-shards --prefix | grep RESULT_JSON
```


---

## Question 4 — Kubernetes Deployment: Self-Healing & Rolling Update

**Folder:** `q4/`

Deploys the spam detection API as a Deployment with 2 replicas and a readinessProbe against `/healthz`, exposed through a NodePort Service, exercised for self-healing and a zero-downtime rolling update.



**To reproduce (self-healing):**
```bash
cd q4
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods -l app=spam-api
kubectl delete pod <pod-name>
kubectl get pods -l app=spam-api
```

**To reproduce (rolling update):**
```bash
docker build -t spam-api:v2 -f Dockerfile .
minikube image load spam-api:v2
# update image: field in deployment.yaml to spam-api:v2
kubectl apply -f deployment.yaml
kubectl rollout status deployment/spam-api
kubectl annotate deployment/spam-api kubernetes.io/change-cause="bumped image to spam-api:v2, added version string to /healthz response" --overwrite
kubectl rollout history deployment/spam-api
curl http://<minikube-ip>:30090/healthz
```

# AI Usage Disclosure

This document outlines how AI tools were used during the development of this project.

## Tools Used

* **Tool name:** Claude
* **Purpose:** Debugging, manifest/code review, and documentation support — not for generating the core project from scratch.

## Where AI Was Used

1. **Manifest Review** — Reviewed my Kubernetes manifests (`validate-job.yaml`, `deployment.yaml`, `service.yaml`) and Dockerfiles against the assignment rubric to check required fields were present. Parallelism and resource values were calculated by me; AI only confirmed the manifest expressed them correctly.

2. **Debugging** — Used AI to interpret `kubectl`/`docker` output and fix a folder mix-up where `q1/` briefly had the wrong `app.py`. All fixes were tested locally before being accepted.

3. **Evidence Review** — Cross-checked my terminal output/screenshots against the rubric, which surfaced two gaps I'd missed: an unannotated `CHANGE-CAUSE` and a missing `kubectl get svc` confirmation. Both were then captured directly from my own cluster.

4. **Documentation** — Used AI to help structure and phrase this README for clarity. Technical content was verified manually against my own codebase and command output.

