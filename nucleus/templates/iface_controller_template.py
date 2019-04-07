__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import falcon
import json
from colorama import Fore
from colorama import Style
from configuration import ProtonConfig
from nucleus.generics.utilities import MyUtilities
{% for controller in iCtrlHash %}
from mic.controllers.{{ controller.fileName }} import {{ controller.controllerName }}
{% endfor %}

{% for controller in iCtrlHash %}

{% for methodName in controller.exposedRESTmethods %}

{% if methodName == 'get' %}

class Ictrl_get_{{controller.micName}}_{{controller.iControllerName}} ({{controller.controllerName}}, ProtonConfig):

    def __init__(self):
        super(Ictrl_get_{{controller.micName}}_{{controller.iControllerName}}, self).__init__()
        self.logger = self.get_logger(log_file_name='{{ controller.iControllerName }}',
                                      log_file_path='{}/trace/{{ controller.iControllerName }}.log'.format(self.ROOT_DIR))

    def on_get(self, req, resp):
        """
        This is recipient of REST GET request.

        Extract query params, use req.get_param(<queryParamId>)

        ---
            description: GET call for {{ iControllerName }} leveraging Ctrl_{{ controllerName }} of PROTON MIC
            responses:
                200:
                    description: <Add description relevant to GET. This will be picked by Swagger generator>
                    schema: <Schema of Response>
        """
        try:
            # If you have newer methods available under Controller, reference that below as per your convenience.
            print(Fore.BLUE + 'Request for route {} is being serviced by conventional db service of '
                              'PROTON stack'.format(req) + Style.RESET_ALL)
            response = json.dumps(self.controller_processor()['{{ controller.iControllerName }}']['{{ methodName }}'](self.TARGET_DB))
            status = falcon.HTTP_200
        except Exception as e:
            response = json.dumps({'message': 'Server has failed to service this request.',
                                   'stackTrace': str(e)})
            status = falcon.HTTP_500
            print(Fore.LIGHTRED_EX + '[Ictrl_{{ controller.iControllerName }}]: GET is unsuccessful. '
                                     'InterfaceController has returned HTTP 500 to client. '
                                     'Exception Details: {}'.format(str(e)) + Style.RESET_ALL)
        finally:
            resp.body = response
            resp.status = status

{% elif methodName == 'post' %}


class Ictrl_post_{{controller.micName}}_{{controller.iControllerName}} ({{controller.controllerName}}, ProtonConfig):

    def __init__(self):
        super(Ictrl_post_{{controller.micName}}_{{controller.iControllerName}}, self).__init__()
        self.logger = self.get_logger(log_file_name='{{ controller.iControllerName }}',
                                     log_file_path='{}/trace/{{ controller.iControllerName }}.log'.format(self.ROOT_DIR))

    def on_post(self, req, resp):
        """
        This is recipient of REST POST request.

        Extract POST payload using json.loads(req.stream.read())

        ---
            description: POST call for {{ iControllerName }} leveraging Ctrl_{{ controllerName }} of PROTON MIC
            responses:
                201:
                    description: <Add description relevant to POST. This will be picked by Swagger generator>
                    schema: <Schema of Response>
        """
        try:

            ##############################
            # POST payload format
            ##############################
            # {
            #     'db_flavour': '', # sqlite or postgres
            #     'db_name': '', # target db name, either it should already exist, if not, this will be created
            #     'table_name': '', # target table name.
            #     'payload': [{'column-1': 'value', 'column-2': 'value', 'column-3': 'value' },
            #                 {'column-1': 'value', 'column-2': 'value', 'column-3': 'value' }]
            # }

            from nucleus.generics.utilities import MyUtilities

            post_payload = json.loads(req.stream.read())
            validity = MyUtilities.validate_proton_post_payload(post_payload)
            print('validity: {}'.format(validity))

            if validity:
                post_response = self.controller_processor()['{{ controller.iControllerName }}']['{{ methodName }}'](post_payload['db_flavour'], post_payload['db_name'], post_payload['table_name'], post_payload['payload'])
                print('post response: {}'.format(post_response))
                response = json.dumps(post_response)
                status = falcon.HTTP_201
            else:
                response = json.dumps({
                    'Message': 'POST Payload invalid. Please input payload in PROTON standard format.',
                    'Sample Format': {
                                'db_flavour': 'sqlite or postgres',
                                'db_name': 'target db name, either it should already exist, if not, this will be created',
                                'table_name': 'target table name',
                                'payload': [{'column-1': 'value', 'column-2': 'value', 'column-3': 'value' },
                                            {'column-1': 'value', 'column-2': 'value', 'column-3': 'value' }]
                    }
                })
                status = falcon.HTTP_400

        except Exception as e:
            response = json.dumps({'Message': 'Server has failed to service this request.',
                                   'stackTrace': str(e)})
            status = falcon.HTTP_500
            print(
                Fore.LIGHTRED_EX + '[Ictrl_{{ controller.iControllerName }}]: POST is unsuccessful. InterfaceController has returned HTTP 500'
                                   ' to client. Exception Details: {}'.format(str(e)) + Style.RESET_ALL)

        finally:
            resp.body = response
            resp.status = status

{% endif %}

{% endfor %}

{% endfor %}