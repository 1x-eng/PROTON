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
## @Desc: Script to initiate and orchestrate proton stack restoration from remote dropbox locations.
## Pre-requisites: Please get your access token(s) to remote dropbox location(s) before you initiate this script.

proton_backup_env_token=''
proton_backup_pg_token=''
proton_backup_redis_token=''
proton_backup_sqlite_token=''

env_mount_path=''
pg_mount_path=''
sqlite_mount_path=''
redis_mount_path=''

echo -e "********* PROTON Restoration Initialized *********\n"
echo -e "Please enter access token's to remote location(s) where PROTON's config and DB are stored\n"

while [[ ${proton_backup_env_token} == '' ]] || [[ ${proton_backup_pg_token} == '' ]] || [[ ${proton_backup_redis_token} == '' ]] || [[ ${proton_backup_sqlite_token} == '' ]]
do
    if [[ ${proton_backup_env_token} == '' ]]; then
        read -p "Please enter/paste token to access remote folder where PROTON's platform config is supposed to live: " proton_backup_env_token
    fi
    if [[ ${proton_backup_pg_token} == '' ]]; then
        read -p "Please enter/paste token to access remote folder where PROTON's PG DB is supposed to live: " proton_backup_pg_token
    fi
    if [[ ${proton_backup_redis_token} == '' ]]; then
        read -p "Please enter/paste token to access remote folder where PROTON's Redis DB is supposed to live: " proton_backup_redis_token
    fi
    if [[ ${proton_backup_sqlite_token} == '' ]]; then
        read -p "Please enter/paste token to access remote folder where PROTON's Sqlite DB is supposed to live: " proton_backup_sqlite_token
    fi
done

echo -e "Thank you for providing access token details. Now, please help with mount path(s) for restore job to download remote contents \n"

while [[ ${env_mount_path} == '' ]] || [[ ${pg_mount_path} == '' ]] || [[ ${sqlite_mount_path} == '' ]] || [[ ${redis_mount_path}  == '' ]]
do
    if [[ ${env_mount_path} == '' ]]; then
        read -p "Enter mount path for PROTON's platform config restoration: " env_mount_path
    fi
    if [[ ${pg_mount_path} == '' ]]; then
        read -p "Enter mount path for PROTON's PG restoration: " pg_mount_path
    fi

    if [[ ${sqlite_mount_path} == '' ]]; then
        read -p "Enter mount path for PROTON's Redis restoration: " redis_mount_path
    fi

    if [[ ${redis_mount_path} == '' ]]; then
        read -p "Enter mount path for PROTON's Sqlite restoration: " sqlite_mount_path
    fi
done

echo -e "Thank you for providing mount path(s). Restoration will be attempted from most recent folder in remote location\n"

cd ../

python proton_restore.py --proton_backup_env_token ${proton_backup_env_token} \
    --proton_backup_pg_token ${proton_backup_pg_token} \
    --proton_backup_redis_token ${proton_backup_redis_token} \
    --proton_backup_sqlite_token ${proton_backup_sqlite_token} \
    --env_mount_path ${env_mount_path} \
    --pg_mount_path ${pg_mount_path} \
    --sqlite_mount_path ${sqlite_mount_path} \
    --redis_mount_path ${redis_mount_path}

echo -e "********* PROTON Restoration Completed *********\n"