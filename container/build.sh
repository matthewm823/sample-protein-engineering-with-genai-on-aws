#!/usr/bin/env bash

AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
SAGEMAKER_ACCOUNT_ID="763104351884"
IMAGE_NAME="models/progen2"
IMAGE_TAG="latest"

# Full image URI for ECR
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${IMAGE_TAG}"


echo "Authenticating with SageMaker ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ${SAGEMAKER_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com


echo "Authenticating with your ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com


echo "Creating ECR repository if it doesn't exist..."
aws ecr describe-repositories --repository-names $IMAGE_NAME --region $AWS_REGION --no-cli-pager 2>/dev/null || \
aws ecr create-repository --repository-name $IMAGE_NAME --region $AWS_REGION --no-cli-pager

echo "Building Docker image..."
docker build --network sagemaker -t $IMAGE_NAME:$IMAGE_TAG .

echo "Tagging image for ECR..."
docker tag $IMAGE_NAME:$IMAGE_TAG $ECR_URI

echo "Pushing image to ECR..."
docker push $ECR_URI

echo "Successfully built and pushed image: $ECR_URI"
