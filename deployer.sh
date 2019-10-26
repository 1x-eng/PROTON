#!/bin/bash

# BSD 3-Clause License
#
# Copyright (c) 2018, Pruthvi Kumar All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
#
# Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## @Author: Pruthvi Kumar
## @Email: pruthvikumar.123@gmail.com
## @Desc: Script to deploy PROTON by prepping remote (Ubuntu) environment with all required dependencies
## @Pre-requisites: THis script must be run as sudo.

echo -e "[Pre-Requisites] Only continue should you have met all the below PROTON deployer pre-requisites:"
echo -e "1. You need to have a DNS mapped to a domain/sub-domain."
echo -e "2. This DNS must be pointing to your remote PROTON server @ default http(80) & https(443) ports."
echo -e "3. Should you opt in to Automated mode, deployer will need to have permission to create new directory from a level above this file\n"

while getopts d:a: option
do
 case "${option}"
 in
 d) dns=${OPTARG};;
 a) automated=${OPTARG};;
 *) : ;;
 esac
done

if [[ -z ${dns} ]]; then
    echo -e "PROTON deployer cannot be initialized unless mandatory server dns is provided\n"
    echo -e "Please meet all pre-requisites and re-initialize PROTON deployer. Thanks \n"
    exit 1
fi

# Install docker & docker-compose
echo -e "********* PROTON DEPLOYER INITIALIZED *********\n"
ROOT_DIR=$(pwd)

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
echo -e "\n"

# Install nginx and http reverse proxy to PROTON
echo -e "[Step - 2] Installing NGINX and configuring HTTP reverse proxy to PROTON\n"
sudo apt-get update
sudo apt-get install -y nginx
unlink /etc/nginx/sites-enabled/default
cd /etc/nginx/sites-available
cat <<EOT > reverse-proxy.conf
server {
                listen 80;
                listen [::]:80;
                server_name ${dns};

                access_log /var/log/nginx/reverse-access.log;
                error_log /var/log/nginx/reverse-error.log;

                location / {
                            proxy_pass http://127.0.0.1:3000;
            }
        }
EOT
ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf
sudo nginx -t
sudo service nginx restart
echo -e "\n"

# Configure HTTPS and reverse proxy HTTPS as default to PROTON.
echo -e "[Step - 3] Configuring HTTPS reverse proxy to PROTON\n"
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:certbot/certbot -y
sudo apt-get update
sudo apt-get install -y python-certbot-nginx
sudo certbot --nginx --non-interactive --agree-tos -m pruthvikumar.123@gmail.com -d ${dns}
echo -e "\n"

# Avoiding permission issues for PROTON stack.
echo -e "[Step - 4] Granting PROTON stack with required folder level permissions."
cd ..
sudo chmod 777 -R ./PROTON
cd ${ROOT_DIR}
echo -e "\n"

echo -e "Infrastructure prep completed for PROTON\n"

if [[ ${automated} == 'yes' ]]; then
    echo -e "DEPLOYER is proceeding in AUTOMATED mode\n"
    echo -e "Generating platform config \n"

    cd ${ROOT_DIR}
    cd ..
    mkdir -p proton_db
    cd proton_db
    mkdir -p pg
    mkdir -p sqlite
    mkdir -p redis

    AUTOMATED_PROTON_DB_PATH=$(pwd)
    cd ${ROOT_DIR}

    cat << EOF > .env
# PS: ANY CHANGES HERE WILL AFFECT BUILD PROCESS.
# PS: DO NOT DELETE ANY VARIABLES OR RENAME THEM. PROTON'S CONTAINERS RELY ON THESE VARIABLES.
PG_USERNAME=$(openssl rand -base64 12)
PG_PASSWORD=$(openssl rand -base64 12)
PG_TARGET_DB=proton
PG_TARGET_PORT=5432
REDIS_TARGET_PORT=6379
PROTON_BIND_ADDRESS=0.0.0.0
PROTON_TARGET_PORT=3000
PROTON_SQLITE_VOLUME_MOUNT=${AUTOMATED_PROTON_DB_PATH}/sqlite
PROTON_POSTGRES_VOLUME_MOUNT=${AUTOMATED_PROTON_DB_PATH}/postgres
PROTON_REDIS_VOLUME_MOUNT=${AUTOMATED_PROTON_DB_PATH}/redis
EOF

    echo -e "Initializing PROTON Stack\n"
    ./cproton.sh -U yes
    echo -e "\n"

    echo -e "*******************************************************"
    echo -e "PROTON Stack successfully initialized in automated mode"
    echo -e "*******************************************************\n"

    echo -e "PS:"
    echo -e "1. Check https://${dns} in your favourite browser or API client to be welcomed by PROTON."
    echo -e "2. Should you want to view logs, use this command- docker logs -f proton"
    echo -e "3. Should you want to see all PROTON stack's containers, use this command- docker ps -a"
    echo -e "4. Deployer has structured your PROTON DB's to be mounted here - ${AUTOMATED_PROTON_DB_PATH}\n"
else
    echo -e "PS:"
    echo -e "1. Infrastructure is prepared for PROTON stack"
    echo -e "2. Since you've not asked for automated mode, please continue to initialize PROTON stack manually."
    echo -e "3. You may start with this command - ./cproton.sh -U yes"
    echo -e "4. Once PROTON stack is up, you may visit https://${dns} in yout favourite browser or API client to be greeted by PROTON\n"
fi


