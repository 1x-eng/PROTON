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

import os
import json
import numpy as np
import pandas as pd
import time
from colorama import Fore
from colorama import Style
from configuration import ProtonConfig
from nucleus.generics.parallel_programming import Parallel_Programming
from nucleus.generics.contained_requests import ContainedRequests
from mic.controller_levers.create_{{ modelName }}_lever import Creator
from mic.controller_levers.read_{{ modelName }}_lever import Reader
from mic.controller_levers.update_{{ modelName }}_lever import Updater
from mic.controller_levers.delete_{{ modelName }}_lever import Deleter

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class Ctrl_{{ controllerName }}(Creator, Reader, Updater, Deleter, Parallel_Programming, ContainedRequests):

    def __init__(self):
        super( Ctrl_{{ controllerName }}, self ).__init__()

        self.controller_processor = self.__processor
        self.ctrl_{{ controllerName }}_logger = self.get_logger(log_file_name='{{ controllerName }}',
                                                                log_file_path='{}/trace/{{ controllerName }}.log'.format(self.ROOT_DIR))
        self.target_db_table = self.__targetTable()

    def __targetTable(self):
        target_table_for_mic = ''
        try:
            with open('{}/proton_vars/target_table_for_{}.txt'.format(self.ROOT_DIR, '{{ modelName }}')) as f:
                target_table_for_mic = f.read().replace('\n', '')

            return target_table_for_mic
        except Exception as e:
            self.ctrl_{{ controllerName }}_logger.exception('[{{ controllerName }}] - Exception while getting target table for {{ modelName }}. '
                                                            'Details: {}'.format(str(e)))
        finally:
            return target_table_for_mic

    def __processor(self):
        """
        All methods in controller will have access to getters and transaction methods from its respective models.

        Here, developer could choose to process data obtained from DB and prepare it(serialize it) for transmission.

        ###########################
        # Method Definition Index
        ###########################
        # Get   : self.getter["get_model_data"](db_flavour, example_sql, binding_params)
        # Insert: self.transaction['insert'](db_flavour, db_name, table_name, input_payload)
        # Update: self.transaction['update'](db_flavour, sql, binding_params)
        # Delete: self.transaction['update'](db_flavour, sql, binding_params)
        # To learn more, do dir(self.getter) and dir(self.transaction).

        ####################################
        # Concurrent Method Definition Index
        ####################################
        # HTTP Operations    : self.concurrency_wrapper('http', target_function, arguments) # PS: arguments[0] must be
        # a list of URLS / Endpoints.
        # Non HTTP Operations: self.concurrency_wrapper('non-http', target_function, arguments)
        # To learn more, do dir(self.concurrency_wrapper)

        :return: serialized response ready for transmission to Interface.
        """

        def proton_reader_default_get(db_flavour, *args):
            return self.proton_default_get(db_flavour, self.ctrl_{{ controllerName }}_logger, *args)

        def proton_creator_default_post(db_flavour, db_name, schema_name, table_name, input_payload):

            expected_metadata = {
                'id': int,
                'firstName': str,
                'lastName': str,
                'age': float
            }

            return json.dumps(self.proton_{{ modelName }}_creator(db_flavour, db_name, schema_name,
                                                                  table_name, input_payload, expected_metadata,
                                                                  self.ctrl_{{ controllerName }}_logger))

        def proton_multi_threaded_http_op(*args):
            """
            Example method to demonstrate concurrent HTTP with PROTON.
            :return: A list containing resolution of concurrent HTTP requests.
            """

            ########################################################################################################
            # Multi Threading Example. [PS: Use Multi Threading only on IO heavy ops; Not CPU intense]
            ########################################################################################################

            url1 = 'https://jsonplaceholder.typicode.com/comments'
            url2 = 'https://jsonplaceholder.typicode.com/albums'
            url3 = 'https://jsonplaceholder.typicode.com/users'
            url4 = 'https://jsonplaceholder.typicode.com/posts'

            url_list = [url1, url2, url3, url4]

            # Target function for a thread to execute.
            def get_call_resolver(url, *args):
                """

                :param url: Target URL to perform HTTP GET on.
                :param args: This is a mandatory param. If the function needs any other args, that will flow in through
                this tuple.
                :return: GET resolution.
                """
                try:

                    # PS: Do not import requests globally for this controller. There is a lot happening in
                    # terms of Greenlets and Inheritance before we get to this method. For all multi-threaded
                    # ops, use similar format (`from nucleus.generics.contained_requests import ContainedRequests`)
                    # to get best results.

                    requests_session = self.session_factory()

                    with requests_session as rs:
                        get_results = rs.get(url)
                    return get_results.json()

                except Exception as e:
                    self.ctrl_{{ controllerName }}_logger.exception(
                        '[{{ controllerName }}] - Error making a requests GET call to {}. '
                        'Stack trace to follow'.format(url))
                    self.ctrl_{{ controllerName }}_logger.exception(str(e))

            default_concurrency_response = {'message': 'This is default response for Multi-threaded'
                                                       ' HTTP operation using PROTON. The following'
                                                       'result is a combination from multiple'
                                                       ' GET requests to a FAKE online REST API. '
                                                       'Do not try to make sense of the response; but,'
                                                       'you can use this concurrency feature in '
                                                       'PROTON with minimum effort. Hurrayyy!!!'}

            concurrent_results = self.concurrency_wrapper('http', get_call_resolver, url_list)
            default_concurrency_response.update(concurrent_results)
            return json.dumps(default_concurrency_response)

        return {
            "default": {'get': proton_reader_default_get, 'post': proton_creator_default_post},  # Supported methods are 'get', 'post'.
            "default_http_concurrency": {'get': proton_multi_threaded_http_op}
            # Similar to above, add more processor methods according to developer's convenience.
        }

