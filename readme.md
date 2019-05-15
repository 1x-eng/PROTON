![PROTON Logo](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON-logo.png)
# PROTON
**The MIC stack genesis!**

PROTON is a high-level Python framework that facilitates rapid server-side development with clean & pragmatic design. 
Thanks for checking it out!

- PROTON aims at easing server-side development for all Python enthusiasts. 
- With PROTON, as a developer you issue **one command**; 
one command, to spin up auto generated code with pragmatic separation of Model, Controller and Interface 
<small>(Hence the name, MIC stack)</small>! 
- One command to setup a production ready server side stack with managed DB connections <small>(PROTON ships with postgresql)</small>, 
managed caching <small>(PROTON ships with redis)</small>, managed JWT authenticated routes, descriptive logging and 
auto-generated openAPI specs.
- PROTON also ships with `signup` and `login` routes to on-board & login users onto platform.
- All of this, **containerised**!

# Getting Started
- Install docker on your development machine. 
    - Linux - https://docs.docker.com/install/linux/docker-ce/ubuntu/
    - Mac - https://docs.docker.com/docker-for-mac/install/
    - Windows - https://docs.docker.com/docker-for-windows/install/
- Clone PROTON to your desired location `git clone https://github.com/PruthviKumarBK/PROTON.git`
- Change directory to PROTON `cd ~/PROTON/`
- `./cproton.sh -U yes` PROTON will ask your input for few key environment variables.
- Wait for the platform to bootstrap; once **done**, visit `http://localhost:3000`. 
- Congratulations. you've got your server-side setup!

![PROTON init platform instructions](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON-platform-init.gif)

# Features
- PROTON comes with out-of-box support for `Signup` and `Login`. 
- Use `/signup` route to sign up users to platform.
![PROTON_postgres_signup](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_postgres_signup.gif)
- Did you want to use `sqlite` instead of postgres for a quick POC? No worries, just change the `db_flavour` in POST payload to 
'sqlite' and you're taken care of!
- PROTON also ships with support for edge conditions on these `signup` and `login` routes. For example - What happens if 
someone tries to signup with same email / username?
![PROTON_postgres_signup_validation](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_signup_validation.png)
- Use '/login' route to login after successful signup. 
![PROTON_postgres_login](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_postgres_login.gif)
- Did you observe the `token` post successful login? That one command to setup the platform has prepared JWT Token 
Authentication! Reckon that is pretty cool!
- And, if you did not already expect, PROTON ships with login validation. Of course!
![PROTON_postgres_login_validation_invalid_username](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_login_invalid_username.png)
![PROTON_postgres_login_validation_invalid_password](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_login_invalid_password.png)

# The MIC stack - What, why & how?

We all know about classic MVC don't we. What happens when we substitute the 'V' <view> in 'MVC' with an 'I' 
<Application Program **Interface**> ? - We get a **MIC** stack! PROTON is a platform that facilitates rapid API 
development (the MIC stack) backed by auto-generated code and good object-oriented programming principles. 

Why do we need this despite many zillion frameworks?

- Do you enjoy writing; rather, re-writing same boiler plate code everytime you wanted to generate a new API using 
the framework of your choice?
- Do you enjoy managing database connectivity and dealing with connectivity issues everytime you touch codebase?
- Do you enjoy learning from an expert that your server side needs performance tuning and miss cache?
- Do you enjoy not having an organized logging mechanism in your server-side code?
- Do you enjoy not having authentication mandated for your server-side codebase?
- Do you enjoy being stressed about converting your codebase to be container ready?
- Do you enjoy being paranoid about steep learning curve associated with Kubernetes?

I've been coding for a living since the last 10 years and for each question above, ** I answer NO even in my dreams**.
Do you agree? Did you want a framework that rather managed all these for you so you could worry only about building 
interesting software rather worry about these classic elements?

I hear screaming **YES**!

PROTON is your answer! One command, all your above problems sorted and managed for you! 
With PROTON, you're a step closer to be that **unicorn** or **10x** developer or whatever else you call that!

Working on a quick prototype to impress or thinking of production deployments - do check out PROTON.

Now that you are interested, see how you get PROTON to work for you:

- Generate new API (you can do all CRUD ops on that API) by issuing one command `./cproton.sh -n myNewApi`
![PROTON_new_mic](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_new_mic.gif)

    - what you see above is an API endpoint auto-generated for the MIC name you provided.
    - a `get` route, `post` route and `concurrency` route. Each demonstrating that same functionality as in their names, respectively.
    - <i>GET call:</i> 
    - ![PROTON_get_call](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_new_mic_get_call.gif)
    - <i>POST call:</i>
    - ![PROTON_post_call](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_post_postgres.gif)
    - And, if you wanted to target sqlite, just change `db_flavour` of your POST `JSON` payload to 'sqlite'.
    - ![PROTON_sqlite_post](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_post_sqlite.png)
    - <i>GET call involving Concurrency / Multi-threading</i>
    - ![PROTON_multi_threading](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_concurrency_route.gif)
        - Notice how first call took about 1 second (if not for multi-threading, this takes about 5 seconds) and subsequent
        calls took only 25~35ms. This is because of cache supporting all subsequent calls.

- Your next question should be, how to generate new API's to my heart's content?
- Find `controller` for your respective MIC where you want new method and just define a new function encapsulating your 
business logic
 ![PROTON_new_custom_method](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_new_method_code.png)
    - Look into lines 230-270. This is where you define your new methods.
    - Line 275 is where you include your new method. 
    - Did you notice how the query parameter is passed into your SQL? That is **SQL Injection Safe** by the way!
- Done coding? You have now tell PROTON to include your method and generate API route. Do that by issuing this 
command: `./cproton.sh -s yes`
 ![PROTON_cproton_update](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_cproton_update_command.png)
- Time to check your shiny new route!
 ![PROTON_new_method_route](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_new_method_api.png) 
 ![PROTON_new_method_api_response](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_new_method_api_response.png)
    - Notice how the route considers `id` as a query parameter and results comply to this query parameter.
    - Results from this route also automatically get the best of PROTON in terms of cache support, logging etc.,

- Did you want to safe destroy a MIC and leave everything else untouched? Use PROTON's safe destruction mechanism
 ![PROTON_safe_destruction](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_safe_destroy_mic.png)
 ![PROTON_post_safe_destroy](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_post_safe_destroy.png)
    - Notice how `login` and `signup` routes remain unaffected. Similarly, if there were other MIC stacks and you destroyed one of them, 
    all others remain as is; unaffected.
    - Always destroy using PROTON's safe destruction mechanism. If otherwise, you will disturb the platform in its 
    sensitive nerves which brings the house down. Also, by using safe destruction, all associated code attached to that 
    respective MIC and cache entries will be pragmatically cleaned.

- Stuck on a problem? Want to debug?
    - Did you want to view logs collectively? Go to `./PROTON/trace` directory.
    ![PROTON_logs](https://github.com/PruthviKumarBK/PROTON-Screengrabs/blob/master/PROTON_logs.png)
    - Note that you can also view real time logs on the container level by issuing this command - `docker logs -f proton`

- Also, PROTON ships with ability to automagically generate OpenAPI specs!

Generate a new MIC stack named **testMic** :
`
 ./protongen.sh -n testMic -p 3000
`

![PROTON MIC stack for testMic](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_testMic.png)

Your code base will now include, dynamically generated content for **testMic** all the way from Model, Controller & Interface!

![PROTON MIC stack for testMic](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_stack_testMic.png)

PROTON will dynamically generate an API for every method defined in the controller for **testMic**. Right now, there is a method named `schemaInformation` within `controller_testMic.py` for **testMic**. Convention for generated route will be <get_micName_controllerMethod>. Go to, `localhost:3000/get_testMic_schemaInformation`; you will see the schema information for connected database in postgresql! This is the default code auto-generated by PROTON for every new MicStack

![PROTON MIC stack API](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_API_testMic.png)

![PROTON MIC stack API for testMic](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_testMic_schemaInformation.png)

For every auto generated route, cache will steer PROTON on steroids for subsequent get calls! Each entry in cache will live upto a day! You can change this lifespan by editing `CACHE_LIFESPAN` within PROTON's `configuration.py`

![PROTON MIC stack API Cache](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_testMic_cacheSet.png)

![PROTON MIC stack Cache](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_cacheService.png)

Now, when you want to add a new method/expose newer APIs within **testMic**, all you should be doing is write SQL and create a method within PROTON's respective MIC stack.

![PROTON MIC Adding Newer Methods](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_newerMethodsToController.png)

With newer method now in place, to generate API, all you do is issue this one command:
` ./protongen.sh -s yes`

![PROTON MIC NewMethod API](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_updatedWithNewerMethods.png)

Newly generated route will also get cache settled!

![PROTON MIC NewMethod at root](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_newerMethodsOnRoot.png)

![PROTON MIC Cache for NewMethod](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_cacheForNewMethod.png)

![PROTON MIC Cache for NewMethod](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_activeCacheForNewMethod.png)

Generating a new MIC stack will leave existing stack unaltered.

![PROTON MIC generating new stack](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_newMicStack.png)

![PROTON MIC NewMethod at root](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_rootAfterNewMic.png)

Trace for PROTON stack will be enabled throughout. Checkout `./trace/` directory.

![PROTON Trace](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_traceDirectory.png)

![PROTON Trace Logs](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_TraceExample.png)

PROTON also ships with ability to automagically generate OpenAPI specs!

![PROTON OpenAPI](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_OpenApi_directory.png)

![PROTON OpenAPI](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_swagger.yaml.png)

Should you want to delete from existing PROTON MIC stack, you stand one command away! Like Generator, PROTON also ships with Destroyer which pragmatically clears the desired MIC from PROTON stack. (This will also clean the Cache entries automagically; only for mic that is targeted to be killed.)

`./protonkill.sh -k <micName>`

![PROTON destroyer](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_afterKilling_testMic.png)

PROTON will continue to perform/live with remaining MIC stack after destroyer completing its job!

![PROTON After destruction of testMic](https://github.com/PruthviKumarBK/PROTON/blob/master/screenshots/PROTON_stackAfterKillingTestMic.png)



NOTE: PROTON uses Gunicorn as High Performance Server. Gunicorn is built to utilize kernel features of Unix/Linux machines. Hence, PROTON will be seamless on Unix/Linux platforms. On Windows, PROTON will require fallback to another WSGI server which is Work In Progress at this moment.

# Features in active development:
- Support for MySql, SqlLite and SqlServer relational databases.
- Pipelines to transfer form and to datawarehouse to database. Support for GCP's bigQuery and AWS's RedShift in progress.
- containerization of PROTON. Docker build and Kubernetes deployable PROTON!
- Auto generated Swagger UI from PROTON generated openAPI specs.

# Support
For any  feedback or issues write to Pruthvi @ pruthvikumar.123@gmail.com. Ensure to have a valid subject line, detailed message with appropriate stack trace to expect prompt/quick response.

# Tags
0.0.1 - PROTON confirms to PEP8 standards.

0.0.2 - Cache is unique not only per route but to query params per route.
# License

BSD 3-Clause License

Copyright (c) 2018, Pruthvi Kumar
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