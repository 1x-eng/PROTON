#!/bin/bash
## @Author: Pruthvi Kumar
## @Email: pruthvikumar.123@gmail.com
## @Desc: Script to initialize proton stack, execute gunicorn server at desired port and write swagger specs!

## usage <Generate MIC  Stack>: ./protongen.sh -p <micName> -d <targetDbTable> -p <port>
## usage <Execute Proton without instantiating MIC Stack> ./protongen.sh -s

while getopts c:n:p:d:s: option
do
 case "${option}"
 in
 c) config=${OPTARG};;
 n) micName=${OPTARG};;
 p) port=${OPTARG};;
 d) targetDbTable=${OPTARG};;
 s) forceStart=${OPTARG};;
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
            gunicorn -b localhost:3000 main:app --reload
         else
            echo -e "-------------------------------------------------------------------------------------------------------------------"
            echo -e "\e[33m Starting PROTON with updated Interface Layer on existing iFace Stack! \e[0m"
            echo -e "-------------------------------------------------------------------------------------------------------------------"
            python protongen.py --forceStart y
            pkill gunicorn
            gunicorn -b localhost:3000 main:app --reload
        fi
    else
        echo -e "-------------------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m PROTON is not configured. Please configure using protongen.sh -c PATH and then try starting PROTON. \e[0m"
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
        gunicorn -b localhost:$port main:app --reload

    else

        echo -e "-------------------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m PROTON is not configured. Please configure using protongen.sh -c PATH and then try creating MIC stack. \e[0m"
        echo -e "-------------------------------------------------------------------------------------------------------------------"

    fi
fi

