# Set docker image
IMAGE_URL=gcr.io/share-cloud-353919/sharer-cloud-backend:v1

# Build image
docker build -t $IMAGE_URL .

# Push to container registry
docker push $IMAGE_URL