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
## @Desc: Script to generate .test-env required by CI to test cproton.

touch .test-env
mkdir -p /tmp/proton_test/sqlite
mkdir -p /tmp/proton_test/postgres
mkdir -p /tmp/proton_test/redis
mkdir -p /tmp/proton_test/test/sqlite

cat << EOF > .test-env
# PS: THIS IS ONLY TO BE USED FOR TEST AND BY CI ONLY.
# PS: ANY CHANGES HERE WILL AFFECT BUILD PROCESS.
# PS: DO NOT DELETE ANY VARIABLES OR RENAME THEM. PROTON'S CONTAINERS RELY ON THESE VARIABLES.
PG_USERNAME=proton_postgres_test
PG_PASSWORD=proton_postgres_test_password
PG_TARGET_DB=proton
PG_TARGET_PORT=5432
REDIS_TARGET_PORT=6379
PROTON_BIND_ADDRESS=0.0.0.0
PROTON_TARGET_PORT=3000
PROTON_SQLITE_VOLUME_MOUNT=/tmp/proton_test/sqlite
PROTON_POSTGRES_VOLUME_MOUNT=/tmp/proton_test/postgres
PROTON_REDIS_VOLUME_MOUNT=/tmp/proton_test/redis
PROTON_TESTER_SQLITE_VOLUME_MOUNT=/tmp/proton_test/test/sqlite
EOF

mkdir -p ./proton_vars
rm -f ./proton_vars/proton_sqlite_config.txt
touch ./proton_vars/proton_sqlite_config.txt
echo "/home/PROTON/proton-db/proton-sqlite.db" >> ./proton_vars/proton_sqlite_config.txt

set -a && source .test-env