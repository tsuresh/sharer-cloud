#FROM rabbitmq:management-alpine
FROM python:3

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

# Install PM2 process manager
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt -y install nodejs
RUN apt -y install npm
RUN npm install pm2 -g

# Copy all files
COPY . .

# Install python dependancies
RUN pip3 install -r requirements.txt

# Expose port
EXPOSE 5000

# Set env
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development
ENV FLASK_APP=main.py

# Make tmp directory
RUN mkdir tmp
RUN chmod 777 tmp

# Set python entrypoint
ENTRYPOINT ["/bin/bash", "/start.sh"]