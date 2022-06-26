#! /bin/bash

# Update system software
sudo apt update && sudo apt upgrade -y

# Add repositories
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install python and pip
sudo apt install python3.8
sudo apt install python3-pip

# Install and setup docker 
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker
sudo dockerd

# Install CMake
sudo apt install cmake

# Install RUNQ environment
git clone --recurse-submodules https://github.com/gotoz/runq.git
cd runq && make release && make release-install
echo '{
"runtimes": {
    "runq": {
      "path": "/var/lib/runq/runq",
      "runtimeArgs": [
        "--cpu", "1",
        "--mem", "256",
        "--dns", "8.8.8.8,8.8.4.4",
        "--tmpfs", "/tmp"
      ]
    }
  }
}' > /etc/docker/daemon.json

echo '# Load vhost_vsock for runq
vhost_vsock' >> /etc/modules-load.d/vhost-vsock.conf

sudo systemctl restart docker

# Install PIP dependancies 
pip3 install -r requirements.txt

# Start application
python main.py