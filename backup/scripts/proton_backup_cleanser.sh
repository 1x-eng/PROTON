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
## @Desc: Script to initiate and orchestrate proton's backups to be cleaned in remote dropbox location.
## Pre-requisites: Please get your access token(s) to remote dropbox location(s) before you initiate this script.

while getopts e:p:r:s: option
do
 case "${option}"
 in
 e) token_for_remote_env=${OPTARG};;
 p) token_for_remote_pg=${OPTARG};;
 r) token_for_remote_redis=${OPTARG};;
 s) token_for_remote_sqlite=${OPTARG};;
 *) : ;;
 esac
done

if [[ -z ${token_for_remote_env} ]] || [[ -z ${token_for_remote_pg} ]] || [[ -z ${token_for_remote_redis} ]] || [[ -z ${token_for_remote_sqlite} ]]; then
    echo -e "[MISSING KEY ARGS] PROTON backup cleanup cannot continue unless valid tokens to access remote folders are provided.\n"
else
    dt_td=$(date -u +"%Y-%m-%d")
    tm_nw=$(date -u +"%H:%M:%S")

    cd ../

    python proton_backup_cleanser.py --proton_backup_env_token ${token_for_remote_env} \
    --proton_backup_pg_token ${token_for_remote_pg} \
    --proton_backup_redis_token ${token_for_remote_redis} \
    --proton_backup_sqlite_token ${token_for_remote_sqlite} \
    --date $dt_td \
    --time $tm_nw
fi