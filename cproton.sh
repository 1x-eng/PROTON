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
## @Desc: Script to initiate containerised proton. Hence the name cproton.

while getopts U:D:: option
do
 case "${option}"
 in
 U) up=${OPTARG};;
 D) down=${OPTARG};;
 *) echo "Arguments is/are not cproton specific. cproton shall forward these to PROTON." ;;
 esac
done


if [[ -x "$(command -v docker)" && -x "$(command -v docker-compose)" ]]; then

    # Validate existance of key environment variables.
    ./init-proton.sh

    if [[ "$(docker images -q proton_stretch:latest 2> /dev/null)" == "" ]]; then

        eval "$(grep ^SENDGRID_API_KEY= .env)"
        eval "$(grep ^APP_NAME= .env)"
        eval "$(grep ^APP_SUPPORT_EMAIL= .env)"

        docker build \
        --build-arg sendgrid_api_key=${SENDGRID_API_KEY} \
        --build-arg app_name=${APP_NAME} \
        --build-arg app_support_email=${APP_SUPPORT_EMAIL} \
        -t proton_stretch:latest .

    fi

    if [[ -z "$up" && -z "$down" ]]; then
        if [[ -z "$(docker-compose ps -q proton)" ]]; then
            echo "FATAL: PROTON container do not seem to be running. cproton cannot orchestrate this command - proton $@"
            echo "PS: Platform needs to be started using cproton.sh -U yes before issuing any other PROTON specific commands"
            echo "PS: cproton will now start the platform in a pragmatic way."
            docker-compose down && docker-compose up --force-recreate -d

            eval "$(grep ^PROTON_BIND_ADDRESS= .env)"
            eval "$(grep ^PROTON_TARGET_PORT= .env)"

            echo "PROTON started and available @ http://${PROTON_BIND_ADDRESS}:${PROTON_TARGET_PORT}"
        else
            docker-compose stop proton | grep "No such service" && docker stop proton
            docker-compose rm -f proton | grep "No stopped containers" && docker rm -f proton && docker image prune -f
            docker-compose run -d --name proton --service-ports --rm proton "$@"

            eval "$(grep ^PROTON_BIND_ADDRESS= .env)"
            eval "$(grep ^PROTON_TARGET_PORT= .env)"

            echo "PROTON updated and available @ http://${PROTON_BIND_ADDRESS}:${PROTON_TARGET_PORT}"
        fi
    elif [[ -z "$down" ]]; then
        case "$up" in
            [yY][eE][sS]|[yY])

            docker-compose down && docker-compose up --force-recreate -d
            eval "$(grep ^PROTON_BIND_ADDRESS= .env)"
            eval "$(grep ^PROTON_TARGET_PORT= .env)"

            echo "PROTON initiated and available @ http://${PROTON_BIND_ADDRESS}:${PROTON_TARGET_PORT}"
            ;;
            *)
            echo "To bring up PROTON platform, valid command is: ./cproton.sh -U yes"
            ;;
        esac
    else
        case "$down" in
            [yY][eE][sS]|[yY])

            docker-compose down
            echo "PROTON platform is gracefully shut down."
            ;;
            *)
            echo "To shut down PROTON platform, valid command is: ./cproton.sh -D yes"
        esac
    fi

else
    echo -e "--------------------------------------------------------------------------------------------------------------"
    echo -e "\e[33m Cproton relies on docker & docker-compose. Please install Docker & docker-compose and try again. \e[0m"
    echo -e "--------------------------------------------------------------------------------------------------------------"
fi
