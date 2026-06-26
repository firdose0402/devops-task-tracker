# --- Stage 1: Build Stage ---
FROM python:3.11-alpine AS builder

WORKDIR /app

# Install necessary system dependencies for compiling SQLite and Python packages
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

COPY requirements.txt .

# Build Python wheels to avoid needing compilers in the final runtime stage
RUN pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: Final Runtime Stage ---
FROM python:3.11-alpine

WORKDIR /app

# Copy only the installed Python packages from the builder stage
COPY --from=builder /root/.local /root/.local
COPY . .

# Configure environment variables
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
