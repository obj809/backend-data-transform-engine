#!/bin/bash
set -e

IMAGE_NAME="data-transform-api"
CONTAINER_NAME="test-api-$$"
PORT=8000

cleanup() {
    echo "Cleaning up..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
}

trap cleanup EXIT

echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .

echo "Starting container..."
docker run -d -p "$PORT:8000" --name "$CONTAINER_NAME" "$IMAGE_NAME"

echo "Waiting for container to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s "http://localhost:$PORT/health" > /dev/null 2>&1; then
        echo "Container is ready!"
        break
    fi
    attempt=$((attempt + 1))
    sleep 1
done

if [ $attempt -eq $max_attempts ]; then
    echo "ERROR: Container failed to become ready"
    docker logs "$CONTAINER_NAME"
    exit 1
fi

echo "Testing /health endpoint..."
health_response=$(curl -s "http://localhost:$PORT/health")
expected_health='{"status":"healthy"}'
if [ "$health_response" = "$expected_health" ]; then
    echo "  /health: PASSED"
else
    echo "  /health: FAILED"
    echo "  Expected: $expected_health"
    echo "  Got: $health_response"
    exit 1
fi

echo "Testing / endpoint..."
root_response=$(curl -s "http://localhost:$PORT/")
expected_root='{"message":"Hello World"}'
if [ "$root_response" = "$expected_root" ]; then
    echo "  /: PASSED"
else
    echo "  /: FAILED"
    echo "  Expected: $expected_root"
    echo "  Got: $root_response"
    exit 1
fi

echo ""
echo "All Docker tests passed!"
