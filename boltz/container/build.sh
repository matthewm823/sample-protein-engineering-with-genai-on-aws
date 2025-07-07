#!/usr/bin/env bash
# set -ex

AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
IMAGE_NAME="boltz2"
IMAGE_TAG="latest"

echo "Creating ECR repository if it doesn't exist..."
aws ecr describe-repositories --repository-names $IMAGE_NAME --region $AWS_REGION --no-cli-pager 2>/dev/null || \
aws ecr create-repository --repository-name $IMAGE_NAME --region $AWS_REGION --no-cli-pager
aws ecr set-repository-policy --repository-name $IMAGE_NAME --policy-text file://omics-ecr-repo-policy.json

echo "Building Docker image..."
docker build --network sagemaker -t $IMAGE_NAME:$IMAGE_TAG .

REGISTRY=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/
ECR_URI=${REGISTRY}${IMAGE_NAME}:${IMAGE_TAG}
echo "Tagging image for ECR...$ECR_URI"
docker tag $IMAGE_NAME:$IMAGE_TAG $ECR_URI

echo "Logging in to $REGISTRY ..."
aws ecr get-login-password | docker login --username AWS --password-stdin $REGISTRY

echo "Pushing image to ECR..."
docker image push $ECR_URI

echo "Successfully built and pushed image: $ECR_URI"