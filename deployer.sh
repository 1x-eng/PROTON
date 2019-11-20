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

echo -e "[Pre-Requisites] Only continue should you have met all the below PROTON deployer pre-requisites:\n"
echo -e "1. You need to have a DNS mapped to a domain/sub-domain."
echo -e "2. This DNS must be pointing to your remote PROTON server @ default http(80) & https(443) ports."
echo -e "3. Should you opt in to Automated mode, deployer will need to have permission to create new directory from a level above this file\n"


echo -e "[How to] Run Deployer:\n"
echo -e "1. ./deployer.sh -d api.sparkle.apricity.co.in This will prep infrastructure, web-server, reverse proxy and makes the platform containerised proton ready"
echo -e "2. a. If you wanted to run the platform for the first time and wanted to spin up the platform with defaults; then use, ./deployer.sh -a yes"
echo -e "   b. If you wanted to restore existing most recent platform and spin up the platform; then use, ./deployer.sh -r yes\n"


while getopts d:a:r: option
do
 case "${option}"
 in
 d) dns=${OPTARG};;
 a) automated=${OPTARG};;
 r) restore=${OPTARG};;
 *) : ;;
 esac
done

ROOT_DIR=$(pwd)
USER_NAME=${USER}


if [[ ! -z ${dns} ]]; then
    # Install docker & docker-compose
    echo -e "\n"
    echo -e "********* PROTON DEPLOYER INITIALIZED *********\n"

    echo -e "Preparing Infrastructure..."
    echo -e "[Step - 1] Installing Docker & Docker-Compose\n"

    sudo apt-get update
    sudo apt-get install -y docker # needs to be tested
    sudo apt-get install -y docker-compose # Needs to be tested
    echo -e "\n"

    # Enable $USER to run docker
    echo -e "[Step -1a] Enabling ${USER_NAME} to run docker\n"
    sudo groupadd docker
    sudo usermod -aG docker ${USER_NAME}
    echo -e "\n"

    # Install nginx and http reverse proxy to PROTON
    echo -e "[Step - 2] Installing NGINX and configuring HTTP reverse proxy to PROTON\n"
    sudo apt-get update
    sudo apt-get install -y nginx
    sudo unlink /etc/nginx/sites-enabled/default
    cd /etc/nginx/sites-available
    sudo bash -c "cat <<EOT > reverse-proxy.conf
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
"
    sudo ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf
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
    cd ${ROOT_DIR}
    sudo chmod 777 -R ./
    echo -e "\n"

    echo -e "Infrastructure prep completed for PROTON\n"
    sudo newgrp docker
fi

if [[ ${automated} == 'yes' ]]; then
    echo -e "DEPLOYER is proceeding in AUTOMATED mode\n"
    echo -e "Generating platform config here - ${ROOT_DIR}\n"

    # Assumption - Before this section, ./deployer -a <dns> is presumed to have run. This would have changed user to root.
    NON_ROOT_USER=`echo ${SUDO_USER:-${USER}}`

    # Volume mounts to live in ORIGINAL user's home directory.
    cd /home/${NON_ROOT_USER}
    mkdir -p proton_db
    cd proton_db
    echo -e "Generating mount paths for proton databases here - $(pwd)"
    AUTOMATED_PROTON_DB_PATH=$(pwd)
    rm -rf ./*

    mkdir -p pg
    mkdir -p sqlite
    mkdir -p redis

    echo -e "Granting permissions for Proton databases."
    cd ..
    sudo chmod 777 -R ./

    echo -e "Generating PROTONs core .env"
    cd ${ROOT_DIR}

    cat << EOF > .env
# PS: ANY CHANGES HERE WILL AFFECT BUILD PROCESS.
# PS: DO NOT DELETE ANY VARIABLES OR RENAME THEM. PROTON'S CONTAINERS RELY ON THESE VARIABLES.
APP_NAME=ProtonDerivative
APP_SUPPORT_EMAIL=pruthvikumar.123@gmail.com
PG_USERNAME=$(openssl rand -base64 12)
PG_PASSWORD=$(openssl rand -base64 12)
PG_TARGET_DB=proton
PG_TARGET_PORT=5432
REDIS_TARGET_PORT=6379
PROTON_BIND_ADDRESS=0.0.0.0
PROTON_TARGET_PORT=3000
PROTON_SQLITE_VOLUME_MOUNT=${AUTOMATED_PROTON_DB_PATH}/sqlite
PROTON_POSTGRES_VOLUME_MOUNT=${AUTOMATED_PROTON_DB_PATH}/pg
PROTON_REDIS_VOLUME_MOUNT=${AUTOMATED_PROTON_DB_PATH}/redis
SENDGRID_API_KEY=NA
EOF
    sudo chown ${NON_ROOT_USER}:${NON_ROOT_USER} ./*
    sudo chmod 777 -R ./
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
    echo -e "4. Deployer has structured your PROTON DB's to be mounted here - ${AUTOMATED_PROTON_DB_PATH}"
    echo -e "5. The automated mode doesn't enable PROTON's ability to send email notifications on both successful and failed login'. You may enable this feature by providing your sendgrid key to .env file\n"

fi
if [[ ${restore} == 'yes' ]]; then
    echo -e "Deployer is instantiating PROTON Restore. Restoration is an interactive process. Please help with valid inputs."
    echo -e "********* PS: Please only use this mount path for PROTON restoration: /tmp/proton_restore *********\n"

    sudo apt-get install -y python-pip
    pip install dropbox

    cd /tmp
    mkdir -p proton_restore
    cd proton_restore
    PROTON_RESTORE_LOCATION=$(pwd)

    cd ${ROOT_DIR}
    cd ./backup/scripts/

    ./proton_restore.sh

    cd ${ROOT_DIR}
    mv -f ${PROTON_RESTORE_LOCATION}/.env ./

     # Assumption - Before this section, ./deployer -a <dns> is presumed to have run. This would have changed user to root.
    NON_ROOT_USER=`echo ${SUDO_USER:-${USER}}`

    cd /home/${NON_ROOT_USER}
    mkdir -p proton_db
    cd proton_db
    rm -rf ./*

    mv -f ${PROTON_RESTORE_LOCATION}/pg ./
    mv -f ${PROTON_RESTORE_LOCATION}/redis ./
    mv -f ${PROTON_RESTORE_LOCATION}/sqlite ./
    cd ..
    sudo chmod -R 777 ./*

    cd ${ROOT_DIR}

    eval "$(grep ^APP_NAME= .env)"
    eval "$(grep ^APP_SUPPORT_EMAIL= .env)"
    eval "$(grep ^PG_USERNAME= .env)"
    eval "$(grep ^PG_PASSWORD= .env)"
    eval "$(grep ^PG_TARGET_DB= .env)"
    eval "$(grep ^PG_TARGET_PORT= .env)"
    eval "$(grep ^REDIS_TARGET_PORT= .env)"
    eval "$(grep ^PROTON_BIND_ADDRESS= .env)"
    eval "$(grep ^PROTON_TARGET_PORT= .env)"
    eval "$(grep ^SENDGRID_API_KEY= .env)"

    rm -rf ./.env

    PROTON_SQLITE_VOLUME_MOUNT=/home/${NON_ROOT_USER}/proton_db/sqlite
    PROTON_POSTGRES_VOLUME_MOUNT=/home/${NON_ROOT_USER}/proton_db/pg
    PROTON_REDIS_VOLUME_MOUNT=/home/${NON_ROOT_USER}/proton_db/redis

    cat << EOF > .env
# PS: ANY CHANGES HERE WILL AFFECT BUILD PROCESS.
# PS: DO NOT DELETE ANY VARIABLES OR RENAME THEM. PROTON'S CONTAINERS RELY ON THESE VARIABLES.
APP_NAME=${APP_NAME}
APP_SUPPORT_EMAIL=${APP_SUPPORT_EMAIL}
PG_USERNAME=${PG_USERNAME}
PG_PASSWORD=${PG_PASSWORD}
PG_TARGET_DB=${PG_TARGET_DB}
PG_TARGET_PORT=${PG_TARGET_PORT}
REDIS_TARGET_PORT=${REDIS_TARGET_PORT}
PROTON_BIND_ADDRESS=${PROTON_BIND_ADDRESS}
PROTON_TARGET_PORT=${PROTON_TARGET_PORT}
PROTON_SQLITE_VOLUME_MOUNT=${PROTON_SQLITE_VOLUME_MOUNT}
PROTON_POSTGRES_VOLUME_MOUNT=${PROTON_POSTGRES_VOLUME_MOUNT}
PROTON_REDIS_VOLUME_MOUNT=${PROTON_REDIS_VOLUME_MOUNT}
SENDGRID_API_KEY=${SENDGRID_API_KEY}
EOF

    ./cproton.sh -U yes
fi
if [[ -z ${dns} ]] || [[ -z ${automated} ]] || [[ -z ${restore} ]]; then
    echo -e "\n"
    echo -e "PS:"
    echo -e "1. Deployer can prepare infrastructure for PROTON via - ./deployer.sh -d <your-api-server-dns>.com"
    echo -e "2. Deployer can initialize PROTON stack in automated mode via - ./deployer.sh -a yes"
    echo -e "3. Deployer can restore your production PROTON stack and revive in your current server via - ./deployer.sh -r yes"
    echo -e "Any other command to deployer will go unrecognized\n"
fi


