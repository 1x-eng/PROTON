#!/bin/bash

echo -e "Preparing Infrastructure..."
echo -e "[Step - 1] Installing Docker & Docker-Compose\n"

sudo apt-get update
sudo apt-get install -y docker # needs to be tested
sudo apt-get install -y docker-compose # Needs to be tested
echo -e "\n"

# Enable $USER to run docker
echo -e "[Step -1a] Enabling ${USER} to run docker\n"
sudo groupadd docker
sudo gpasswd -a ${USER} docker
newgrp docker