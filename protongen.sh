#!/bin/bash
## @Author: Pruthvi Kumar
## @Email: pruthvikumar.123@gmail.com
## @Desc: Script to initialize proton stack, execute gunicorn server at desired port and write swagger specs!

## usage <Generate MIC  Stack>: ./protongen.sh -p <micName> -d <targetDbTable> -p <port>
## usage <Execute Proton without instantiating MIC Stack> ./protongen.sh -s

while getopts n:p:d:s: option
do
 case "${option}"
 in
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

if [[ -z "$micName" ]]
    then
    if [[ -z "$forceStart" ]]
        then
        echo -e "----------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m micName not provided!, ProtonGen will try to invoke Gunicorn with available routes @ port 3000! \e[0m"
        echo -e "----------------------------------------------------------------------------------------------------------"
        pkill gunicorn
        gunicorn -b localhost:3000 main:app --reload
     else
        echo -e "-------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m Starting PROTON with updated Interface Layer on existing iFace Stack! \e[0m"
        echo -e "------------------------------------------------------------------------------------------------------"
        python protongen.py --forceStart y
        pkill gunicorn
        gunicorn -b localhost:3000 main:app --reload
    fi

else
    if [[ -z "$port" ]]
    then
        port=3000
        echo -e "------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m port not provided; Defaulting to: \e[0m"$port
        echo -e "------------------------------------------------------------------------------------------------------"

    else
        port=$port
        echo -e "------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m Instantiating PROTON stack for micName: \e[0m"$micName "\e[33m  @ port: \e[0m"$port
        echo -e "------------------------------------------------------------------------------------------------------"
    fi

    if [[ -z "$targetDbTable" ]]
    then
        echo -e "------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m Target table not specified. PROTON will rely on default table for this MIC stack. \e[0m"
        echo -e "------------------------------------------------------------------------------------------------------"
        echo $micName
        export "PROTON_target_table_for_$micName=default"

    else
        echo -e "------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m Target table for $micName MIC stack will be set to $targetDbTable. \e[0m"
        echo -e "------------------------------------------------------------------------------------------------------"
        export "PROTON_target_table_for_$micName=$targetDbTable"

    fi

    mkdir -p trace
    python protongen.py --mic_name $micName --port $port
    pkill gunicorn
    gunicorn -b localhost:$port main:app --reload
fi

