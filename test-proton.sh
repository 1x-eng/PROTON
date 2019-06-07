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
## @Desc: Script to test proton stack

while getopts i:t: option
do
 case "${option}"
 in
 i) initialize=${OPTARG};;
 n) test=${OPTARG};;
 esac
done

if [[ ! -z $initialize ]]; then
    echo -e "\e[36m

===============================================================
=       ===       =====    ====        ====    ====  =======  =
=  ====  ==  ====  ===  ==  ======  ======  ==  ===   ======  =
=  ====  ==  ====  ==  ====  =====  =====  ====  ==    =====  =
=  ====  ==  ===   ==  ====  =====  =====  ====  ==  ==  ===  =
=       ===      ====  ====  =====  =====  ====  ==  ===  ==  =
=  ========  ====  ==  ====  =====  =====  ====  ==  ====  =  =
=  ========  ====  ==  ====  =====  =====  ====  ==  =====    =
=  ========  ====  ===  ==  ======  ======  ==  ===  ======   =
=  ========  ====  ====    =======  =======    ====  =======  =
===============================================================

\e[0m"

    rm ./.env
    touch .env

    mkdir -p /tmp/proton_test/sqlite
    mkdir -p /tmp/proton_test/postgres
    mkdir -p /tmp/proton_test/redis
    mkdir -p /tmp/proton_test/test/sqlite

    PG_TARGET_DB=proton
    PG_TARGET_PORT=5432
    REDIS_TARGET_PORT=6379
    PROTON_BIND_ADDRESS=0.0.0.0
    PROTON_TARGET_PORT=3001
    PG_USERNAME=proton_postgres_test
    PG_PASSWORD=proton_postgres_test
    PROTON_SQLITE_VOLUME_MOUNT=/tmp/proton_test/sqlite
    PROTON_POSTGRES_VOLUME_MOUNT=/tmp/proton_test/postgres
    PROTON_REDIS_VOLUME_MOUNT=/tmp/proton_test/redis
    PROTON_TESTER_SQLITE_VOLUME_MOUNT=/tmp/proton_test/test/sqlite

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
PROTON_TESTER_SQLITE_VOLUME_MOUNT=$PROTON_TESTER_SQLITE_VOLUME_MOUNT
EOF

    # configuring SQLITE mount path for the PROTON container.
    mkdir -p ./proton_vars
    rm -f ./proton_vars/proton_sqlite_config.txt
    touch ./proton_vars/proton_sqlite_config.txt
    echo "/home/PROTON/proton-db/proton-sqlite.db" >> ./proton_vars/proton_sqlite_config.txt

    docker-compose down && docker-compose up --force-recreate -d

    echo "PROTON test container is initialized"
elif [[ ! -z $test ]]; then

    echo "PROTON test container will initialize tests"
    docker exec proton_test -t $test

else
    echo "PROTON test container has received an invalid argument. No action will be taken."
fi