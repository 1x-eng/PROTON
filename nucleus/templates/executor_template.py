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

import json
import falcon
from apispec import APISpec
from configuration import ProtonConfig
from falcon_apispec import FalconPlugin
from falcon_cors import CORS
from falcon_prometheus import PrometheusMiddleware
from mic.iface.middlewares.token_authenticator import TokenAuthenticator
from mic.iface.middlewares.iface_watch import Iface_watch
from nucleus.iam.login import IctrlProtonLogin
from nucleus.iam.signup import IctrlProtonSignup
{% for ifaceController in ifaceControllers %}
from mic.iface.controllers.{{ ifaceController.fileName }} import {{ ifaceController.controllerName }}
{% endfor %}

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"

"""
PROTON executor: Point WSGI server to this file and reach out to available routes!
"""


class DefaultRouteHandler(object):
    """
    PROTON's default route handler.
    """
    def __init__(self):
        super(DefaultRouteHandler, self).__init__()

    def on_get(self, req, resp):
        response = {
            'message': 'PROTON is successfully initialized!',
            'availableRoutes': []
        }
        response['availableRoutes'].append('/login')
        response['availableRoutes'].append('/signup')
        {%for route in routes %}
        response['availableRoutes'].append('/{{ route.routeName }}')
        {% endfor %}
        resp.body = json.dumps(response)
        resp.status = falcon.HTTP_200


class FastServe(object):
    """
    This is a sink to service dynamically routed entries from cache!
    """

    def __init__(self):
        super(FastServe, self).__init__()

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200


prometheus = PrometheusMiddleware()
cors = CORS(allow_all_origins=['http://localhost:{{ port }}'])
app = falcon.API(middleware=[TokenAuthenticator(), cors.middleware, Iface_watch(), prometheus])

app.add_route('/', DefaultRouteHandler())
app.add_route('/fast-serve', FastServe())
app.add_route('/login', IctrlProtonLogin())
app.add_route('/signup', IctrlProtonSignup())
app.add_route('/prom-metrics', prometheus)

{% for route in routes %}
rc_{{ route.controllerName }} =  {{ route.controllerName }}()
{% endfor %}

{% for route in routes %}
app.add_route('/{{ route.routeName }}', rc_{{ route.controllerName }})
{% endfor %}

# Open API Specs
spec = APISpec(
    title='PROTON STACK',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FalconPlugin(app),
    ],
)

{% for route in routes %}
spec.add_path(resource= rc_{{ route.controllerName }})
{% endfor %}

# OPEN API specs will be generated during runtime.
with open('{}/mic/iface/openApi/specs.json'.format(ProtonConfig().ROOT_DIR), 'w+') as sjf:
    sjf.write(json.dumps(spec.to_dict()))

with open('{}/mic/iface/openApi/specs.yaml'.format(ProtonConfig().ROOT_DIR), 'w+') as syf:
    syf.write(spec.to_yaml())
