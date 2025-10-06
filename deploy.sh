#!/usr/bin/env bash
set -euo pipefail

# Usage: ./deploy.sh <version>
# Requires: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, DOCKER_IMAGE (env)

IMAGE="${DOCKER_IMAGE:-wecarmobility/blh-homepage}"
VERSION="${1:-latest}"

echo "Logging into Docker Hub..."
echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

echo "Building image: $IMAGE:$VERSION"
docker build -t "$IMAGE:$VERSION" .

echo "Pushing image: $IMAGE:$VERSION"
docker push "$IMAGE:$VERSION"

echo "Done."


