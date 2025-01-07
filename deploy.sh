#!/bin/bash

PROJECT_ID="fluted-sentry-447013-j5"
IMAGE_NAME="ootd-fastapi-app"
SERVICE_NAME="ootd-app"
REGION="asia-northeast3"

# Re-create new builder and activate it
docker buildx rm multiarch
docker-buildx create --name multiarch --use
docker buildx inspect --bootstrap

# Build multi architecture image
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t gcr.io/$PROJECT_ID/$IMAGE_NAME \
    --push .

# Build Docker image
# docker build -t gcr.io/$PROJECT_ID/$IMAGE_NAME .

# Push Docker image
# docker push gcr.io/$PROJECT_ID/$IMAGE_NAME

# Deploy Cloud Run
gcloud run deploy ootd-app \
  --image gcr.io/fluted-sentry-447013-j5/ootd-fastapi-app \
  --platform managed \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --add-cloudsql-instances=fluted-sentry-447013-j5:asia-northeast3:ootd-instance
