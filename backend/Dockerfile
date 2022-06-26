#FROM rabbitmq:management-alpine
FROM ubuntu

# Set work directory
WORKDIR /

# Update system
RUN apt update

# Install python/pip
RUN apt -y install python3-pip

# Install RabbitMQ
RUN apt -y install curl
RUN curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.deb.sh | bash
RUN apt update
RUN apt -y install rabbitmq-server
RUN service rabbitmq-server start

# Copy all files
COPY . .

# Install python dependancies
RUN pip3 install -r requirements.txt

# Expose port
EXPOSE 5000

# Set python entrypoint
ENTRYPOINT [ "python3", "-m" , "main", "run", "--host=0.0.0.0"]