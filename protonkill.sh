#!/bin/bash
## @Author: Pruthvi Kumar
## @Email: pruthvikumar.123@gmail.com
## @Desc: Script to kill proton stack across MIC stack.

## usage: ./protonkill.sh -k <micName>


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

while getopts k: option
do
 case "${option}"
 in
 k) micNameToKill=${OPTARG};;
 esac
done

if [[ -z "$micNameToKill" ]]
    then
    echo -e "----------------------------------------------------------------------------------------------------------"
    echo -e "\e[33m micName not provided! ProtonKill needs a valid existing MIC in PROTON stack to function! Leaving Gunicorn functional in PROTON's current state @ PORT 3000! \e[0m"
    echo -e "----------------------------------------------------------------------------------------------------------"

else
    echo -e "----------------------------------------------------------------------------------------------------------"
    echo -e "\e[33m Killing PROTON stack for micName: \e[0m"$micNameToKill
    python protonkill.py --micNameToKill $micNameToKill
    rm -r ./proton_vars/target_table_for_$micNameToKill.txt
    echo -e "\e[33m Restarting Gunicorn with remaining PROTON stack \e[0m"
fi

./protongen.sh -s y