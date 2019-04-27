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

# Generate PROTON JWT Secret if it doesn't already exist.
if [[ ! -e nucleus/iam/secrets/PROTON_JWT_SECRET.txt ]]; then
    mkdir -p nucleus/iam/secrets
    touch nucleus/iam/secrets/PROTON_JWT_SECRET.txt
    echo "PROTON_JWT_SECRET" >> nucleus/iam/secrets/PROTON_JWT_SECRET.txt
fi

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