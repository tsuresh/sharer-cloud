# Sharer Cloud - Real Time Cloud Workload Processing Network
Sharer Cloud focuses on creating an web resource sharing ecosystem that can be entirely run by community members by sharing the processing power of personal computers for real-time operations. The proposed architecture is made up of several modules, including Cluster Members Module, Workloads Module, Scheduler, Monitoring Module, and Workloads Runtime. Each module is in charge of handling specific system tasks. Aside from the main architecture, the research focuses on scaling and scheduling algorithms for accurate workload placement. When developing all of the workload scheduler algorithms, the author used a data-driven approach. In addition, for this task, the author used modern data forecasting machine learning models.

## High Level System Architecture
![FYP Diagrams-High Level (2)](https://user-images.githubusercontent.com/3047253/178161752-1e491641-5773-48a7-a9c7-e1d771059050.jpg)

## Resource Contributors
Service contributors are clients who join as stakeholders to give their system processing capacity to the system. Contributors will be given incentives based on their contributions.

Resource contributors can deploy the system in contributor devices/vacant servers via two ways:

 1. Direct Installation
 2. Docker Based Installation
 
### Direct Installation
The following steps can be taken to install the system directly via the BASH script as provided.
Initially navigate to the contributor client source directory

    cd contributor_client
Run the following BASH script as root

    $ ./setup.sh

### Build Docker Image
Docker image can be built as follows
Initially navigate to the contributor client source directory

    cd contributor_client
  Run the Docker build commands
  

    docker build -t user/imagename:tag .
Execute the container

    docker run user/imagename:tag

## Backend Service
The backend service can be deployed as a Docker container

### Build and run the Docker Image
Docker image can be built as follows
Initially navigate to the contributor client source directory

    cd requestor_client
  Run the Docker build commands
  

    docker build -t user/imagename:tag .
Execute the container

    docker run -p 5000:5000 user/imagename:tag
Backend service would be accessible on http://localhost:5000

## Resource Requestor Poral
Users who seek processing power through the system are referred to as Service Requestors.
React based service requestor portal can be deployed as follows; The portal will be accessible on http://localhost:8080/

Navigate to the respective directory

    cd requestor_client

Execute YARN development commands (For dev environments)

    yarn dev
    
Execute YARN serve commands (For prod environments)

    yarn serve
