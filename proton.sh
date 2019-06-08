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
## @Desc: Script to initialize proton stack, execute gunicorn server at desired port and write swagger specs!

## usage <Generate MIC  Stack>: ./proton.sh -p <micName> -d <targetDbTable> -p <port> -t <numberOfThreads>
## usage <Execute Proton without instantiating MIC Stack> ./proton.sh -s
## usage <Kill a MIC stack with Proton> ./proton.sh -k <targetMicName>

while getopts c:n:p:t:d:s:k:e:T: option
do
 case "${option}"
 in
 c) config=${OPTARG};;
 n) micName=${OPTARG};;
 p) port=${OPTARG};;
 t) numberOfThreads=${OPTARG};;
 d) targetDbTable=${OPTARG};;
 s) forceStart=${OPTARG};;
 k) micNameToKill=${OPTARG};;
 e) environment=${OPTARG};;
 T) protonTest=${OPTARG};;
 esac
done

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

echo "Granting PROTON necessary permissions"
echo "I am $(whoami)"
echo "working directory is: $(pwd)"
ls -lart

if [[ "$protonTest" == 'yes' ]]; then
    echo "Acknowledging test request for PROTON"
    echo "****************** Starting Pytest for PROTON ******************"
    python -m pytest -s ./test/ -m preview
    echo "****************** Pytest completed for PROTON ******************"

else

    if [[ -z "$environment" || "$environment" != 'test' ||  "$protonTest" != 'yes' ]]; then
        # Default environment = production

        echo "Instantiating PROTON in production environment"

        # Validate existance of key environment variables.
        ./init-proton.sh

        # Parse .env and get binding params.
        eval "$(grep ^PROTON_BIND_ADDRESS= .env)"
        eval "$(grep ^PROTON_TARGET_PORT= .env)"

        # Interpolate values from .env to databaseConfig.ini
        eval "$(grep ^PG_TARGET_DB= .env)"
        eval "$(grep ^PG_USERNAME= .env)"
        eval "$(grep ^PG_PASSWORD= .env)"
        eval "$(grep ^PG_TARGET_PORT= .env)"

    elif [[ "$environment" == 'test' ||  "$protonTest" == 'yes' ]]; then

        # Parse .test-env and get binding params.
        eval "$(grep ^PROTON_BIND_ADDRESS= .test-env)"
        eval "$(grep ^PROTON_TARGET_PORT= .test-env)"

        # Interpolate values from .env to databaseConfig.ini
        eval "$(grep ^PG_TARGET_DB= .test-env)"
        eval "$(grep ^PG_USERNAME= .test-env)"
        eval "$(grep ^PG_PASSWORD= .test-env)"
        eval "$(grep ^PG_TARGET_PORT= .test-env)"

    else
        :
    fi

    cat << EOF > ./databaseConfig.ini
# PS: DO NOT MAKE ANY CHANGES HERE. THIS FILE IS DYNAMICALLY GENERATED.
# PS: CHANGING CONFIG VALUE HERE MANUALLY SHALL FAIL BUILD PROCESS.
[postgresql]
host=pg
database=$PG_TARGET_DB
user=$PG_USERNAME
password=$PG_PASSWORD
port=$PG_TARGET_PORT
EOF

    # Generate PROTON JWT Secret if it doesn't already exist.
    if [[ ! -e nucleus/iam/secrets/PROTON_JWT_SECRET.txt ]]; then
        mkdir -p nucleus/iam/secrets
        touch nucleus/iam/secrets/PROTON_JWT_SECRET.txt
        echo "PROTON_JWT_SECRET" >> nucleus/iam/secrets/PROTON_JWT_SECRET.txt
    fi

    if [[ -z "$config" ]]
    then
        echo -e "-------------------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m Not config step. PROTON will continue with rest of the process flow \e[0m"
        echo -e "-------------------------------------------------------------------------------------------------------------------"
    else
        echo -e "-------------------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m Welcome to PROTON configuration \e[0m"
        echo -e "-------------------------------------------------------------------------------------------------------------------"

        read -p "Please confirm default PATH (absolute path) for PROTON to install SQLite database is: $config [y/n] " "default_sqlite_path"

        mkdir -p proton_vars
        rm -f ./proton_vars/proton_sqlite_config.txt
        touch ./proton_vars/proton_sqlite_config.txt

        if [[ $default_sqlite_path == y ]]
        then
            echo "Default path confirmed is $config"
            echo $config >> ./proton_vars/proton_sqlite_config.txt
        elif [[ $default_sqlite_path == n ]]
        then
            read -p "Please enter the PATH (absolute path) for PROTON to install SQLite database: " "new_sqlite_path"
            echo "Confirmed path is $new_sqlite_path"
            echo "$new_sqlite_path/proton-sqlite.db" >> ./proton_vars/proton_sqlite_config.txt
        else
            echo "Default path not provided. PROTON will not continue unless this is sorted."
        fi
    fi

    if [[ -z "$micNameToKill" ]]
        then
        :
    else

        echo -e "\e[31m

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

        echo -e "----------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m Killing PROTON stack for micName: \e[0m"$micNameToKill
        python protonkill.py --micNameToKill $micNameToKill
        rm -r ./proton_vars/target_table_for_$micNameToKill.txt
        echo -e "\e[33m Restarting Gunicorn with remaining PROTON stack \e[0m"
        pkill gunicorn

        echo -e "----------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m PROTON restarting @ port $PROTON_TARGET_PORT! \e[0m"
        echo -e "----------------------------------------------------------------------------------------------------------"

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
        python protongen.py --forceStart y
        pkill gunicorn
        gunicorn -b $PROTON_BIND_ADDRESS:$PROTON_TARGET_PORT main:app --reload

    fi

    if [[ -z "$micName" ]]
    then
        if [ -s "./proton_vars/proton_sqlite_config.txt" ];
        then
            if [[ -z "$forceStart" ]]
            then
                echo -e "-------------------------------------------------------------------------------------------------------------------"
                echo -e "\e[33m micName not provided!, ProtonGen will try to invoke Gunicorn with available routes @ port 3000! \e[0m"
                echo -e "-------------------------------------------------------------------------------------------------------------------"
                pkill gunicorn
                python protongen.py
                if [[ -z $numberOfThreads ]]
                then
                    gunicorn -b $PROTON_BIND_ADDRESS:$PROTON_TARGET_PORT main:app --reload
                else
                    echo -e "-------------------------------------------------------------------------------------------------------------------"
                    echo -e "\e[33m PROTON starting with $numberOfThreads worker threads. \e[0m"
                    echo -e "-------------------------------------------------------------------------------------------------------------------"
                    gunicorn -b $PROTON_BIND_ADDRESS:$PROTON_TARGET_PORT main:app --threads $numberOfThreads --reload
                fi
             else
                echo -e "-------------------------------------------------------------------------------------------------------------------"
                echo -e "\e[33m Starting PROTON with updated Interface Layer on existing iFace Stack! \e[0m"
                echo -e "-------------------------------------------------------------------------------------------------------------------"
                python protongen.py --forceStart y
                pkill gunicorn
                if [[ -z $numberOfThreads ]]
                then
                    gunicorn -b $PROTON_BIND_ADDRESS:$PROTON_TARGET_PORT main:app --reload
                else
                    echo -e "-------------------------------------------------------------------------------------------------------------------"
                    echo -e "\e[33m PROTON starting with $numberOfThreads worker threads. \e[0m"
                    echo -e "-------------------------------------------------------------------------------------------------------------------"
                    gunicorn -b $PROTON_BIND_ADDRESS:$PROTON_TARGET_PORT main:app --threads $numberOfThreads --reload
                fi
            fi
        else
            echo -e "-------------------------------------------------------------------------------------------------------------------"
            echo -e "\e[33m PROTON is not configured. Please configure using proton.sh -c PATH and then try starting PROTON. \e[0m"
            echo -e "-------------------------------------------------------------------------------------------------------------------"
        fi

    else

        if [ -s "./proton_vars/proton_sqlite_config.txt" ];
        then

            if [[ -z "$port" ]]
            then
                port=3000
                echo -e "-------------------------------------------------------------------------------------------------------------------"
                echo -e "\e[33m port not provided; Defaulting to: \e[0m"$port
                echo -e "-------------------------------------------------------------------------------------------------------------------"

            else
                port=$port
                echo -e "-------------------------------------------------------------------------------------------------------------------"
                echo -e "\e[33m Instantiating PROTON stack for micName: \e[0m"$micName "\e[33m  @ port: \e[0m"$port
                echo -e "-------------------------------------------------------------------------------------------------------------------"
            fi

            if [[ -z "$targetDbTable" ]]
            then
                echo -e "-------------------------------------------------------------------------------------------------------------------"
                echo -e "\e[33m Target table not specified. PROTON will rely on default table for this MIC stack. \e[0m"
                echo -e "-------------------------------------------------------------------------------------------------------------------"

                mkdir -p proton_vars
                touch ./proton_vars/target_table_for_$micName.txt
                echo "PROTON_default" >> ./proton_vars/target_table_for_$micName.txt

            else
                echo -e "-------------------------------------------------------------------------------------------------------------------"
                echo -e "\e[33m Target table for $micName MIC stack will be set to $targetDbTable. \e[0m"
                echo -e "-------------------------------------------------------------------------------------------------------------------"

                mkdir -p proton_vars
                touch ./proton_vars/target_table_for_$micName.txt
                echo $targetDbTable >> ./proton_vars/target_table_for_$micName.txt

            fi

            mkdir -p trace
            python protongen.py --mic_name $micName --port $port
            pkill gunicorn
            if [[ -z $numberOfThreads ]]
            then
                gunicorn -b $PROTON_BIND_ADDRESS:$PROTON_TARGET_PORT main:app --reload
            else
                echo -e "-------------------------------------------------------------------------------------------------------------------"
                echo -e "\e[33m PROTON starting with $numberOfThreads worker threads. \e[0m"
                echo -e "-------------------------------------------------------------------------------------------------------------------"
                gunicorn -b $PROTON_BIND_ADDRESS:$PROTON_TARGET_PORT main:app --threads $numberOfThreads --reload
            fi

        else

            echo -e "-------------------------------------------------------------------------------------------------------------------"
            echo -e "\e[33m PROTON is not configured. Please configure using proton.sh -c PATH and then try creating MIC stack. \e[0m"
            echo -e "-------------------------------------------------------------------------------------------------------------------"

        fi
    fi
fi
