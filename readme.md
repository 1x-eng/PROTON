![PROTON Logo](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON-logo.png)
# PROTON 
![PROTON_build](https://travis-ci.org/PruthviKumarBK/PROTON.svg?branch=master)

**The MIC stack genesis!**

Proton is a high-level Python framework that facilitates rapid server-side development with clean & pragmatic design. 
Thanks for checking it out!

- Proton aims at easing server-side development for all Python enthusiasts. 
- Proton bootstraps templated backend by relying on code generating code with minimum dev effort. 
- A few CLI commands to setup production ready server side stack with managed DB connections <small>(Proton ships with postgresql)</small>, 
managed caching <small>(Proton ships with redis)</small>, managed JWT authenticated routes, descriptive logging, 
managed monitoring (Prometheus & Grafana) and auto-generated openAPI specs.
- Automates `signup` & `login` with necessaary validations.
- All of this, **containerised**

# Anatomy
![PROTON tech stack anatomy](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/ProtonStackAnatomy.png)

# Getting Started
- Install latest version of docker on your development machine/server. 
    - Linux - https://docs.docker.com/install/linux/docker-ce/ubuntu/
    - Mac - https://docs.docker.com/docker-for-mac/install/
    - Windows - https://docs.docker.com/docker-for-windows/install/
- Install latest version of docker-compose on your development machine/server (https://docs.docker.com/compose/install/)
- Clone `git clone https://github.com/1x-eng/PROTON.git & Change directory `cd ~/PROTON/`
- `./cproton.sh -U yes`, please comply to CLI prompts(Use absolute address; not relative for file paths)
- Wait for the platform to bootstrap; once **done**, visit `http://localhost:3000`. 
- Congratulations. you've got your server-side setup!

![PROTON init platform instructions](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON-platform-init.gif)

# Features
- Proton comes with out-of-box support for `Signup` and `Login`. 
- Use `/signup` route to sign up users to platform.
![PROTON_postgres_signup](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_postgres_signup.gif)
- Did you want to use `sqlite` instead of postgres for a quick POC? No worries, just change the `db_flavour` in POST payload to 
'sqlite' and you're taken care of!
-`signup` and `login` routes validations for free. For example - What happens if 
someone tries to signup with same email / username?
![PROTON_postgres_signup_validation](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_signup_validation.png)
- Use '/login' route to login after successful signup. 
![PROTON_postgres_login](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_postgres_login.gif)
- Did you observe the `token` post successful login? That one command to setup the platform has prepared JWT Token 
Authentication with minimum dev effort.
- `login` validation for free.
![PROTON_postgres_login_validation_invalid_username](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_login_invalid_username.png)
![PROTON_postgres_login_validation_invalid_password](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_login_invalid_password.png)
- Prometheus & grafana leveraged for monitoring purposes 
![PROTON_Prom_Grafana](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_Home_Prom_Graf.png)
![Proton_Prometheus](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_Prom.png)
- Ships with a fgew grafana dashboards out-of-the-box. Visit `localhost:3000/proton-grafana` in your 
favourite browser and login with default credentials:
    - username: admin
    - password: admin
    - You'll be prompted to change and choose your own strong password on first login.
    - `Proton Monitor`
    ![PROTON_Grafana_Monitor](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_grafana_monitor.png)
    - `Proton Stack - Holistic Monitor`
    ![PROTON_Grafana_Cadvisor](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_grafana_container_monitor.png)

# The MIC stack - What, why & how?

Proton facilitates rapid API development (the <b>M</b>odel<b>I</b>nterface<b>C</b>ontroller stack) with templated code generated with a few CLI commands. 

Why do we need this despite many zillion frameworks? Potentially, helps get away from some of these boring tasks:

- writing; rather, re-writing same boiler plate code everytime you wanted to generate a new API using 
the framework of your choice
- managing database connectivity and dealing with connectivity issues everytime you touch codebase
- cacheing & performance tuning
- logging & monitoring
- authentication & authorization
- container ready backend

# Getting Started

- Generate new API (you can do all CRUD ops on that API) by issuing one command `./cproton.sh -n myNewApi`
![PROTON_new_mic](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_new_mic.gif)

    - what you see above is an API endpoint auto-generated for the MIC name you provided.
    - a `get` route, `post` route and `concurrency` route.
    - <i>GET call:</i> 
    - ![PROTON_get_call](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_new_mic_get_call.gif)
    - <i>POST call:</i>
    - ![PROTON_post_call](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_post_postgres.gif)
    - And, if you wanted to target sqlite, just change `db_flavour` of your POST `JSON` payload to 'sqlite'.
    - ![PROTON_sqlite_post](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_post_sqlite.png)
    - <i>GET call involving Concurrency / Multi-threading</i>
    - ![PROTON_multi_threading](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_concurrency_route.gif)
        - Notice how first call took about 1 second (if not for multi-threading, this takes about 5 seconds) and subsequent
        calls took only 25~35ms. Thanks for cacheing.

- For every new MIC stack that you generate (via `cproton.sh -s <your_api_name>`), PROTON generates a dedicated controller and 
which deals with CRUD ops:
    - Example: ![PROTON_Controller_Levers](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/NewApiControllerLevers.png)
    
- Deploy using `./cproton.sh -s yes`
 ![PROTON_cproton_update](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_cproton_update_command.png)
 ![PROTON_new_method_route](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_new_method_api.png) 
 ![PROTON_new_method_api_response](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_new_method_api_response.png)
    - Notice how the route considers `id` as a query parameter and results comply to this query parameter.
    - Results from this route also automatically get the best of PROTON in terms of cache support, logging etc.,

- Deleting made easy, while separating concerns.
 ![PROTON_safe_destruction](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_safe_destroy_mic.png)
 ![PROTON_post_safe_destroy](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_post_safe_destroy.png)
    - Notice how `login` and `signup` routes remain unaffected. Similarly, if there were other MIC stacks and you destroyed one of them, 
    all others remain as is; unaffected.

- Access logs here - `./PROTON/trace`
    ![PROTON_logs](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_logs.png)

- OpenAPI specs out-of-the-box
 ![PROTON_swagger_json](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_swagger_json.png)
 ![PROTON_swagger_yaml](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_swagger_yaml.png)

# Miscellaneous

## Automated Backup & Restoration
- Proton also ships with an ability to backup vitals (secrets + db volume mounts) to cold storage(Dropbox)
- To initiate backup, 
    - Create a dropbox account for yourself and create an app - https://www.dropbox.com/developers/apps
        - An example would be:
            - API type - Dropbox API
            - Type of data access as "App folder - Access to a single folder created specifically for your app"
            - App name as "PROTON Backup"
            - Create App & then click on "Generate access token". You'll need this token later.
    - With your access token handy, now navigate to `backup` folder in Proton home directory.
    - Initiate backup using `./scripts/proton_backup_orchestrator.sh`
    - Comply with command line prompts and provide access token when asked for.
    - There is an audit trail just in case. You may `cat` those reports available under `backup/reports` folder.
    
- Similar to backups, Proton also ships with ability to restore from remote dropbox location to your local machine or remote server.
- In order to initiate restoration, ensure you have the access token handy for your remote backup folder and navigate to `backup` folder.
    - Initiate restoration using `./scripts/proton_restore.sh`
    

## PROTON Remote Deployment Instructions - (Considering base machine of Ubuntu-18.04LTS)
- If you have a pre-configured DNS handy, use ` ./deployer.sh -d <your_dns>`
- If you wanted to run the platform for the first time and ok to proceed with defaults; then use: `./deployer.sh -a yes`
- If you were using Proton's backup services, to kickstart restoration use this: `./deployer.sh -r yes`

- ** Prefer manual approach? This could help: **

- [Step - 1] Install Docker and Docker-Compose
```bash
    sudo apt-get update
    sudo apt-get install -y docker
    sudo apt-get install -y docker-compose
```
- [Step - 2] Enable USER to run docker
```bash
    sudo groupadd -e docker
    sudo gpasswd -a ${USER} docker
    newgrp docker
```
- [Step - 3] Install NGINX and configure HTTP reverse proxy
```bash
    sudo apt-get update
    sudo apt-get install -y nginx
    unlink /etc/nginx/sites-enabled/default
    cd /etc/nginx/sites-available
    cat <<EOT > reverse-proxy.conf
    server {
                    listen 80;
                    listen [::]:80;
                    server_name <dns here>;
    
                    access_log /var/log/nginx/reverse-access.log;
                    error_log /var/log/nginx/reverse-error.log;
    
                    location / {
                                proxy_pass http://127.0.0.1:3000;
                }
            }
    EOT
    ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf
    sudo nginx -t
    sudo service nginx restart
```
- [Step - 4] Configure HTTPS in NGINX reverse proxy
```bash
    sudo apt-get update
    sudo apt-get install -y software-properties-common
    sudo add-apt-repository ppa:certbot/certbot -y
    sudo apt-get update
    sudo apt-get install -y python-certbot-nginx
    sudo certbot --nginx --non-interactive --agree-tos -m <email> -d <dns eg. temp.com here>
```
- [Step - 5] Grant permission to PROTON Stack
```bash
    cd ~/PROTON
    sudo chmod 777 -R ./
```
- Start Proton stack using - `./cproton.sh -U yes`


# Credits
![Adroit-Logo](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/AdroitLogo.png)

PROTON is a product of Adroit Software Corporation (ABN 426 3819 0066) (https://adroitcorp.com.au)

# License

BSD 3-Clause License

Copyright (c) 2018, Pruthvi Kumar & Adroit Software Corporation (https://www.adroitcorp.com.au)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
