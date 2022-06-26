FROM alpine:3.10

# Set work directory
WORKDIR /

# Install Alpine Dependencies
RUN apk update && apk upgrade && apk add --update alpine-sdk && \
    apk add --no-cache bash git openssh make cmake 

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Install Docker
RUN apk add --update docker openrc
RUN rc-update add docker boot
RUN dockerd

# Install RUNQ/QEMU environment
RUN git clone --recurse-submodules https://github.com/gotoz/runq.git
RUN cd runq && make release && make release-install

# Copy RUNQ configs to docker config
RUN echo '{\n\
"runtimes": {\n\
    "runq": {\n\
      "path": "/var/lib/runq/runq",\n\
      "runtimeArgs": [\n\
        "--cpu", "1",\n\
        "--mem", "256",\n\
        "--dns", "8.8.8.8,8.8.4.4",\n\
        "--tmpfs", "/tmp"\n\
      ]\n\
    }\n\
  }\n\
}' > /etc/docker/daemon.json

RUN service docker reload

# Copy files
COPY . .

# Install python requirements
RUN pip3 install -r requirements.txt

# Set program entrypoint
ENTRYPOINT [ "python", "main.py" ]