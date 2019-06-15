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
# Neither the name of the copyright h"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"er nor the names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT H"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"ERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT H"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"ER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## @Author: Pruthvi Kumar
## @Email: pruthvikumar.123@gmail.com
## @Desc: Update, downgrade or install specific version of PROTON.

while getopts t:c: option
do
 case "${option}"
 in
 t) tag=${OPTARG};;
 c) commit=${OPTARG};;
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

action_version_control(){

    current_year=$(date +"%Y")
    current_month=$(date +"%m")
    todays_date=$(date +"%d")
    current_hour=$(date +"%H")
    current_minute=$(date +"%M")
    current_second=$(date +"%S")

    cd "$current_proton_location"
    mv ./grafana /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./mic/iface/middlewares/iface_watch.py /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./mic/iface/middlewares/proton_prometheus.py /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./mic/iface/middlewares/token_authenticator.py /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./nucleus /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./prometheus /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./test /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./.dockerignore /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./.gitignore /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./.travis.yml /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./CI_Dockerfile /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./CODE_OF_CONDUCT.md /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./configuration.py /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./CONTRIBUTING.md /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./cproton.sh /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./docker-compose.yaml /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./docker-compose-test.yaml /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./Dockerfile /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./init-proton.sh /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./LICENSE /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./proton.sh /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./protongen.py /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./protonkill.py /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./readme.md /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./requirements.txt /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/
    mv ./test-env-gen.sh /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"/

    cd /tmp/proton_ver_ctrl/PROTON
    mv ./grafana "$current_proton_location"
    mv ./mic/iface/middlewares/iface_watch.py "$current_proton_location"/mic/iface/middlewares/iface_watch.py
    mv ./mic/iface/middlewares/proton_prometheus.py "$current_proton_location"/mic/iface/middlewares/proton_prometheus.py
    mv ./mic/iface/middlewares/token_authenticator.py "$current_proton_location"/mic/iface/middlewares/token_authenticator.py
    mv ./nucleus "$current_proton_location"
    mv ./prometheus "$current_proton_location"
    mv ./test "$current_proton_location"
    mv ./.dockerignore "$current_proton_location"
    mv ./.gitignore "$current_proton_location"
    mv ./.travis.yml "$current_proton_location"
    mv ./CI_Dockerfile "$current_proton_location"
    mv ./CODE_OF_CONDUCT.md "$current_proton_location"
    mv ./configuration.py "$current_proton_location"
    mv ./CONTRIBUTING.md "$current_proton_location"
    mv ./cproton.sh "$current_proton_location"
    mv ./docker-compose.yaml "$current_proton_location"
    mv ./docker-compose-test.yaml "$current_proton_location"
    mv ./Dockerfile "$current_proton_location"
    mv ./init-proton.sh "$current_proton_location"
    mv ./LICENSE "$current_proton_location"
    mv ./proton.sh "$current_proton_location"
    mv ./protongen.py "$current_proton_location"
    mv ./protonkill.py "$current_proton_location"
    mv ./readme.md "$current_proton_location"
    mv ./requirements.txt "$current_proton_location"
    mv ./test-env-gen.sh "$current_proton_location"

    cd /tmp/proton_ver_ctrl
    rm -rf ./PROTON
}

current_proton_location=$(pwd)
mkdir -p /tmp/proton_ver_ctrl
mkdir -p /tmp/proton_ver_ctrl/"$current_year"_"$current_month"_"$todays_date"_"$current_hour"_"$current_minute"_"$current_second"

if [[ -z "$tag" && -z "$commit" ]]; then
    echo "PROTON will update itself to most latest version"
    cd /tmp/proton_ver_ctrl
    git clone https://github.com/PruthviKumarBK/PROTON.git
    action_version_control
    echo "PROTON is successfully updated to latest version."
    echo "PS: If you wanted your old files for some reason, they are available here: /tmp/proton_ver_ctrl/${current_year}_${current_month}_${todays_date}_${current_hour}_${current_minute}_${current_second}"

elif [[ ! -z "$tag" || ! -z "$commit" ]]; then
    echo "WARNING: Downgrading PROTON to significantly older tags/commits might break code base beyond repair."
    confirm_tagged_upgrade_or_downgrade=""
    while [[ "$confirm_tagged_upgrade_or_downgrade" != "YES" || "$confirm_tagged_upgrade_or_downgrade" != "NO" ]]
    do
        if [[ -z "$commit" ]]; then
            read -p "Do you still want to proceed replacing your current PROTON version to ${tag} ?[YES/NO]" confirm_tagged_upgrade_or_downgrade
        else
            read -p "Do you still want to proceed replacing your current PROTON version to ${commit} ?[YES/NO]" confirm_tagged_upgrade_or_downgrade
        fi
    done

    if [[ "$confirm_tagged_upgrade_or_downgrade" == "YES" ]]; then

        cd /tmp/proton_ver_ctrl
        git clone https://github.com/PruthviKumarBK/PROTON.git
        cd PROTON

        if [[ -z "$commit" ]]; then
            rebase_code="tag"
            rebase_pointer="$tag"
            echo "PROTON will rebase itself to tagged release of v${tag}"
            git checkout tags/"$tag"
            rebase_exit_code=$?
        else
            rebase_code="commit"
            rebase_pointer="$commit"
            echo "PROTON will rebase itself to this commit - ${commit}"
            git checkout "$commit"
            rebase_exit_code=$?
        fi

        if [[ "$rebase_exit_code" == 0 ]]; then
            cd /tmp/proton_ver_ctrl
            action_version_control
            echo "PROTON is successfully updated to specified ${rebase_code} - ${rebase_pointer}"
            echo "PS: If you wanted your old files for some reason, they are available here: /tmp/proton_ver_ctrl/${current_year}_${current_month}_${todays_date}_${current_hour}_${current_minute}_${current_second}"
        else
            echo "Could not checkout to specified ${rebase_code} - ${rebase_pointer}. Please verify appropriate tags or commits here - https://github.com/PruthviKumarBK/PROTON/tags"
            echo "PROTON will not be able to continue due to errors checking out to specified ${rebase_code}"
        fi

    elif [[ "$confirm_tagged_upgrade_or_downgrade" == "NO" ]]; then
        echo "PROTON will discontinue any further update/downgrade actions"
        echo "Your existing codebase remains unaltered"

    else
        echo "Sorry, That is an invalid option. You have to answer that question by either a YES/NO"
    fi
else
    :
fi
