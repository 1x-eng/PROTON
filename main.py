__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

"""
PROTON executor: Point WSGI server to this file and reach out to available routes!
"""

import json
import falcon
from apispec import APISpec
from falcon_apispec import FalconPlugin
from falcon_cors import CORS
from configuration import ProtonConfig
from mic.iface.middlewares.iface_watch import Iface_watch



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


cors = CORS(allow_all_origins=['http://localhost:3000'])
app = falcon.API(middleware=[cors.middleware, Iface_watch()])

app.add_route('/', DefaultRouteHandler())
app.add_route('/fast-serve', FastServe())





# Open API Specs
spec = APISpec(
    title='PROTON STACK',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FalconPlugin(app),
    ],
)



# OPEN API specs will be generated during runtime.
with open('{}/mic/iface/openApi/specs.json'.format(ProtonConfig().ROOT_DIR), 'w+') as sjf:
    sjf.write(json.dumps(spec.to_dict()))

with open('{}/mic/iface/openApi/specs.yaml'.format(ProtonConfig().ROOT_DIR), 'w+') as syf :
    syf.write(spec.to_yaml())