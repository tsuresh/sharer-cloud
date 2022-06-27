IMAGE_URL=gcr.io/share-cloud-353919/sharer-cloud-backend:v1
docker build -t $IMAGE_URL .
docker push $IMAGE_URL