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

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import os
import json
import numpy as np
import pandas as pd
from colorama import Fore
from colorama import Style
from configuration import ProtonConfig
from mic.models.{{ modelName }}.model_{{ modelName }} import Model_{{modelName}}

class Ctrl_{{ controllerName }}(Model_{{ modelName }}):

    def __init__(self):
        super( Ctrl_{{ controllerName }}, self ).__init__()
        self.target_db_table = self.__targetTable()
        self.logger = self.get_logger(log_file_name='{{ controllerName }}',
                                      log_file_path='{}/trace/{{ controllerName }}.log'.format(self.ROOT_DIR))
        self.controller_processor = self.__processor



    def __targetTable(self):
        target_table_for_mic = ''
        try:
            with open('{}/proton_vars/target_table_for_{}.txt'.format(self.ROOT_DIR, '{{ modelName }}')) as f:
                target_table_for_mic = f.read().replace('\n', '')

            return target_table_for_mic
        except Exception as e:
            self.logger.exception('[{{ controllerName }}] - Exception while getting target table for {{ modelName }}. '
                                  'Details: {}'.format(str(e)))
        finally:
            return target_table_for_mic

    def __processor(self):
        """
        All methods in controller will have access to getters and transaction methods from its respective models.

        Here, developer could choose to process data obtained from DB and prepare it(serialize it) for transmission.

        :return: serialized response ready for transmission to Interface.
        """

        def proton_default_get(db_flavour):

            if ProtonConfig.TARGET_DB == 'sqlite':
                target_table = 'PROTON_default'

                example_sql = """
                SELECT * from {} ORDER BY id DESC LIMIT 10
                """.format(target_table)
                binding_params = {}

            elif ProtonConfig.TARGET_DB == 'postgresql':

                example_sql = """
                SELECT table_schema, table_name
                FROM information_schema.tables
                ORDER BY table_schema,table_name;
                """

                binding_params = {}
            else:
                example_sql = """
                """
                binding_params = {}

            try:
                # to use getter methods, use self.getter; to use transaction methods, use self.transaction.
                # to learn more, do dir(self.getter) and dir(self.transaction).

                ###########################
                # Method Definition Index
                ###########################

                # Insert: self.transaction['insert'](db_flavour, db_name, table_name, input_payload)
                # Update: self.transaction['update'](db_flavour, sql, binding_params)
                # Delete: self.transaction['update'](db_flavour, sql, binding_params)

                results = self.getter["get_model_data"](db_flavour, example_sql, binding_params)
                return results
            except Exception as e:
                self.logger.exception('[{{ controllerName }}] - Exception while getting model data. '
                                      'Details: {}'.format(str(e)))
                raise Fore.LIGHTRED_EX + '[{{ controllerName }}] - Exception while getting model data. ' \
                                         'Details: {}'.format(str(e)) + Style.RESET_ALL

        def proton_default_post(db_flavour, db_name, schema_name, table_name, input_payload):
            try:
                self.transaction['insert'](db_flavour, db_name, schema_name, table_name, input_payload)
                return json.dumps({
                    'Message': 'Insert operation to {}.{} table in {} database under {} is successful'.format(schema_name,
                                                                                                           table_name,
                                                                                                           db_name,
                                                                                                           db_flavour)})
            except Exception as e:
                self.logger.exception('[{{ controllerName }}] - Exception while inserting data. '
                                      'Details: {}'.format(str(e)))
                raise Fore.LIGHTRED_EX + '[{{ controllerName }}] - Exception while inserting data. ' \
                                         'Details: {}'.format(str(e)) + Style.RESET_ALL

        return {
            "default": {'get': proton_default_get, 'post': proton_default_post}, # Supported methods are 'get', 'post'.
            # Similar to above, add more processor methods according to developer's convenience.
        }



