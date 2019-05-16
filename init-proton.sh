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
## @Desc: Script to check and set all vitals required by proton platform.!

echo -e "-------------------------------------------------------------------------------------------------------------------"
echo -e "\e[33m Validating PROTON vitals... \e[0m"
echo -e "-------------------------------------------------------------------------------------------------------------------"

if [[ -f .env ]]; then
    # check if env contains all required variables.
    eval "$(grep ^PG_USERNAME= .env)"
    eval "$(grep ^PG_PASSWORD= .env)"
    eval "$(grep ^PG_TARGET_DB= .env)"
    eval "$(grep ^PG_TARGET_PORT= .env)"
    eval "$(grep ^REDIS_TARGET_PORT= .env)"
    eval "$(grep ^PROTON_BIND_ADDRESS= .env)"
    eval "$(grep ^PROTON_TARGET_PORT= .env)"
    eval "$(grep ^PROTON_SQLITE_VOLUME_MOUNT= .env)"
    eval "$(grep ^PROTON_POSTGRES_VOLUME_MOUNT= .env)"
    eval "$(grep ^PROTON_REDIS_VOLUME_MOUNT= .env)"

    if [[ -z "$PG_USERNAME" ]]; then
        while [[ -z "$PG_USERNAME" ]]
        do
            read -p "PROTON is missing key environment var - PG_USERNAME. \
By default, PROTON ships with support for postgres. \
PG_USERNAME is the username that PROTON's postgres will use for login purposes.\
Please enter username for PROTON's postgres: " PG_USERNAME
        done
    fi

    if [[ -z "$PG_PASSWORD" ]]; then
        while [[ -z "$PG_PASSWORD" ]]
        do
            read -p "PROTON is missing key environment var - PG_PASSWORD. \
By default, PROTON ships with support for postgres. \
PG_PASSWORD is the password that PROTON's postgres will use for login purposes.\
Please enter password for PROTON's postgres: " PG_PASSWORD
        done
    fi

    if [[ -z "$PG_TARGET_DB" ]]; then
        PG_TARGET_DB=proton
    fi

    if [[ -z "$PG_TARGET_PORT" ]]; then
        PG_TARGET_PORT=5432
    fi

    if [[ -z "$REDIS_TARGET_PORT" ]]; then
        REDIS_TARGET_PORT=6379
    fi

    if [[ -z "$PROTON_BIND_ADDRESS" ]]; then
        PROTON_BIND_ADDRESS=0.0.0.0
    fi

    if [[ -z "$PROTON_TARGET_PORT" ]]; then
        PROTON_TARGET_PORT=3000
    fi

    if [[ -z "$PROTON_SQLITE_VOLUME_MOUNT" ]]; then
#        while [[ -z "$PROTON_SQLITE_VOLUME_MOUNT" ]]
#        do
#            read -p "PROTON is missing key environment var - PROTON_SQLITE_VOLUME_MOUNT. \
#By default, PROTON ships with support for sqlite. \
#PROTON_SQLITE_VOLUME_MOUNT is the location that PROTON's sqlite file will mount onto.\
#Please enter the absolute location where PROTON's sqlite can mount onto: " PROTON_SQLITE_VOLUME_MOUNT
#        done
        PROTON_SQLITE_VOLUME_MOUNT='/home/PROTON/proton-db/proton-sqlite.db'
    fi

    if [[ -z "$PROTON_POSTGRES_VOLUME_MOUNT" ]]; then
        while [[ -z "$PROTON_POSTGRES_VOLUME_MOUNT" ]]
        do
            read -p "PROTON is missing key environment var - PROTON_POSTGRES_VOLUME_MOUNT. \
By default, PROTON ships with support for postgres. \
PROTON_POSTGRES_VOLUME_MOUNT is the location that PROTON's postgres container will mount onto.\
Please enter the absolute location where PROTON's postgres can mount onto: " PROTON_POSTGRES_VOLUME_MOUNT
        done
    fi

    if [[ -z "$PROTON_REDIS_VOLUME_MOUNT" ]]; then
        while [[ -z "$PROTON_REDIS_VOLUME_MOUNT" ]]
        do
            read -p "PROTON is missing key environment var - PROTON_REDIS_VOLUME_MOUNT. \
By default, PROTON ships with cache support by incorporating Redis. \
PROTON_REDIS_VOLUME_MOUNT is the location that PROTON's redis container will mount onto.\
Please enter the absolute location where PROTON's redis can mount onto: " PROTON_REDIS_VOLUME_MOUNT
        done
    fi

else

    touch .env

    PG_TARGET_DB=proton
    PG_TARGET_PORT=5432
    REDIS_TARGET_PORT=6379
    PROTON_BIND_ADDRESS=0.0.0.0
    PROTON_TARGET_PORT=3000
    PROTON_SQLITE_VOLUME_MOUNT='/home/PROTON/proton-db/proton-sqlite.db'

    while [[ -z "$PG_USERNAME" ]]
        do
            read -p "By default, PROTON ships with support for postgres.\
PG_USERNAME is the username that PROTON's postgres will use for login purposes.\
Please enter username for PROTON's postgres: " PG_USERNAME
        done

    while [[ -z "$PG_PASSWORD" ]]
        do
            read -p "By default, PROTON ships with support for postgres. \
PG_PASSWORD is the password that PROTON's postgres will use for login purposes.\
Please enter password for PROTON's postgres: " PG_PASSWORD
        done

#    while [[ -z "$PROTON_SQLITE_VOLUME_MOUNT" ]]
#        do
#            read -p "By default, PROTON ships with support for sqlite. \
#PROTON_SQLITE_VOLUME_MOUNT is the location that PROTON's sqlite file will mount onto.\
#Please enter the absolute location where PROTON's sqlite can mount onto: " PROTON_SQLITE_VOLUME_MOUNT
#        done

    while [[ -z "$PROTON_POSTGRES_VOLUME_MOUNT" ]]
        do
            read -p "By default, PROTON ships with support for postgres. \
PROTON_POSTGRES_VOLUME_MOUNT is the location that PROTON's postgres container will mount onto.\
Please enter the absolute location where PROTON's postgres can mount onto: " PROTON_POSTGRES_VOLUME_MOUNT
        done

    while [[ -z "$PROTON_REDIS_VOLUME_MOUNT" ]]
        do
            read -p "By default, PROTON ships with cache support by incorporating Redis. \
PROTON_REDIS_VOLUME_MOUNT is the location that PROTON's redis container will mount onto.\
Please enter the absolute location where PROTON's redis can mount onto: " PROTON_REDIS_VOLUME_MOUNT
        done

fi

    cat << EOF > .env
# PS: ANY CHANGES HERE WILL AFFECT BUILD PROCESS.
# PS: DO NOT DELETE ANY VARIABLES OR RENAME THEM. PROTON'S CONTAINERS RELY ON THESE VARIABLES.
PG_USERNAME=$PG_USERNAME
PG_PASSWORD=$PG_PASSWORD
PG_TARGET_DB=$PG_TARGET_DB
PG_TARGET_PORT=$PG_TARGET_PORT
REDIS_TARGET_PORT=$REDIS_TARGET_PORT
PROTON_BIND_ADDRESS=$PROTON_BIND_ADDRESS
PROTON_TARGET_PORT=$PROTON_TARGET_PORT
PROTON_SQLITE_VOLUME_MOUNT=$PROTON_SQLITE_VOLUME_MOUNT
PROTON_POSTGRES_VOLUME_MOUNT=$PROTON_POSTGRES_VOLUME_MOUNT
PROTON_REDIS_VOLUME_MOUNT=$PROTON_REDIS_VOLUME_MOUNT
EOF

# configuring mount path for SQLITE
# TODO: This needs refactor to read from env directly instead of file.
mkdir -p ./proton_vars
rm -f ./proton_vars/proton_sqlite_config.txt
touch ./proton_vars/proton_sqlite_config.txt
echo $PROTON_SQLITE_VOLUME_MOUNT >> ./proton_vars/proton_sqlite_config.txt

echo -e "-------------------------------------------------------------------------------------------------------------------"
echo -e "\e[33m PROTON has all vitals checked and set. \e[0m"
echo -e "-------------------------------------------------------------------------------------------------------------------"

