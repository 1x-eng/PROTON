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
## @Desc: Base PROTON Container with default sqlite and postgres config.

FROM python:3.7.3-stretch

RUN echo "********* ENV variables creation phase *********\n"
ARG sendgrid_api_key
ARG app_name
ARG app_support_email
ENV SENDGRID_API_KEY=${sendgrid_api_key}
ENV APP_NAME=${app_name}
ENV APP_SUPPORT_EMAIL=${app_support_email}
RUN echo "\n"

RUN echo "********* PROTON dependencies installation phase *********\n"
RUN apt-get update
RUN apt-get install bash
RUN apt-get install -y gcc g++ unixodbc-dev
RUN echo "\n"

RUN echo "********* PROTON folder structure creation phase *********\n"
RUN mkdir -p /PROTON
RUN mkdir -p /PROTON/proton-db
RUN mkdir -p /PROTON/trace
RUN echo "\n"

RUN echo "********* PROTON user group & user creation phase *********\n"
RUN groupadd proton_user_group
RUN useradd -G proton_user_group default_proton_user
RUN echo "\n"

RUN echo "********* PROTON source code injection phase *********\n"
WORKDIR /PROTON
COPY . /PROTON
RUN echo "\n"

RUN echo "********* PROTONs PY dependencies installation phase *********\n"
RUN python3 -m pip install -r requirements.txt --no-cache-dir
RUN echo "\n"

RUN echo "********* PROTON user ownership and restriction phase *********\n"
RUN chown -R default_proton_user:proton_user_group /PROTON/*
RUN chmod 777 -R /PROTON/*
USER default_proton_user
RUN echo "\n"

RUN echo "********* PROTON port expose phase *********\n"
EXPOSE 3000/tcp