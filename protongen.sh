#!/bin/bash
## @Author: Pruthvi Kumar
## @Email: pruthvikumar.123@gmail.com
## @Desc: Script to initialize proton stack, execute gunicorn server at desired port and write swagger specs!

## usage <Generate MIC  Stack>: ./protongen.sh -p <micName> -p <port>
## usage <Execute Proton without instantiating MIC Stack> ./protongen.sh -s

while getopts n:p:s: option
do
 case "${option}"
 in
 n) micName=${OPTARG};;
 p) port=${OPTARG};;
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
        pkill gunicorn
        gunicorn -b localhost:3000 main:app --reload
     else
        echo -e "----------------------------------------------------------------------------------------------------------"
        echo -e "\e[33m Starting PROTON with updated Interface Layer on existing iFace Stack! \e[0m"
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

    else
        port=$port
        echo -e "\e[33m Instantiating PROTON stack for micName: \e[0m"$micName "\e[33m  @ port: \e[0m"$port
        echo -e "------------------------------------------------------------------------------------------------------"
    fi
    mkdir -p trace
    python protongen.py --mic_name $micName --port $port
    pkill gunicorn
    gunicorn -b localhost:$port main:app --reload
fi

