FROM python:3.12-slim

WORKDIR /data
COPY shards/ /data/

WORKDIR /app
COPY validate_shard.py .

CMD ["python", "validate_shard.py"]
