# --- Stage 1: builder — has compilers, installs everything ---
FROM python:3.12 AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/build/deps -r requirements.txt

# --- Stage 2: runtime — slim base, only copies the finished packages ---
FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /build/deps /usr/local/lib/python3.12/site-packages
COPY . .

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
