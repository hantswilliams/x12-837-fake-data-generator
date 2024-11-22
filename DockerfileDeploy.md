# Deployment with GCP

## Utilization Cloud Run
- Prequests:
    - Need to push image to a registry, like docker hub 
        - e.g., `docker buildx build --platform linux/amd64 -t form837 .` # this is important for building on a M1/M2 processor 
            - can then test with `docker run -p 5005:5005 form837`
        - e.g., `docker tag form837 hants/form837-demo`
        - e.g., `docker push hants/form837-demo`
    - In the current iteration, have pushed image to docker hub (docker.io/hants/837-demo)

- Steps:
    - Create a new service in Cloud Run
    - Select the image from the registry
    - Set the port in the image to match the port in the Cloud Run service, which currently is 5005