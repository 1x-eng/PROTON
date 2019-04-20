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

import falcon
import json
import pandas as pd
from colorama import Fore
from colorama import Style
from datetime import datetime
from nucleus.db.connection_manager import ConnectionManager
from sqlalchemy import MetaData
from sqlalchemy import select

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class ProtonSignup(ConnectionManager):

    def __init__(self):
        super(ProtonSignup, self).__init__()
        self.__alchemy_engine = self.alchemy_engine()
        self.logger = self.get_logger(log_file_name='iam_signup_logs.log',
                                      log_file_path='{}/trace/iam_signup_logs.log'.format(self.ROOT_DIR))


    def signup(self, db_flavour, input_payload, db_name='proton', schema_name='iam', table_name='PROTON_user_registry'):
        """
        Signs up users to PROTON.

        :param db_flavour: One of the supported versions. Must have an entry in dataBaseConfig.ini
        :param db_name: Name of target Database. Default: Proton
        :param schema_name: Name of target schema. Default: iam
        :param table_name: Name of target table. Default: PROTON_user_registry
        :param input_payload: Paylod of user details.
        :return: A dictionary containig signup status and message.
        """

        def validate_signup_payload(payload):

            def validate_payload_contents(payload):
                """
                Validates that payload contains atleast one character. Most stringent form validation
                must be a client side operation.
                :param payload: signup payload
                :return: Boolean
                """
                validity_store = []
                for k,v in payload.items():
                    if len(str(v)) > 0:
                        validity_store.append(True)
                    else:
                        validity_store.append(False)
                if all(validity_store):
                    return True
                return False

            if type(payload) is not dict:
                return False
            required_keys = ['first_name', 'last_name', 'email', 'creation_date_time',
                             'user_name', 'password']
            payload.update({'creation_date_time': datetime.now()})

            actual_keys = list(payload.keys())
            if set(required_keys) == set(actual_keys):
                return validate_payload_contents(payload)
            return False

        if validate_signup_payload(input_payload):
            try:
                signup_payload = {
                    'first_name': input_payload['first_name'],
                    'last_name': input_payload['last_name'],
                    'email': input_payload['email'],
                    'creation_date_time': input_payload['creation_date_time']
                }

                login_payload = {
                    'user_name': input_payload['user_name'],
                    'password': input_payload['password']
                }

                connection = self.__alchemy_engine[db_flavour].connect()
                metadata = MetaData(self.__alchemy_engine[db_flavour], reflect=True)
                table = metadata.tables[table_name]

                with connection.begin() as transaction:
                    if db_flavour == 'sqlite':

                        # Check if user already exists:
                        query_pre_existance = select([table.c.id]).where(table.c.email == signup_payload['email'])
                        pre_existance_details = (connection.execute(query_pre_existance)).fetchall()

                        if len(pre_existance_details) == 0:
                            df_signup_payload = pd.DataFrame(signup_payload, index=[0])
                            df_signup_payload.to_sql(table_name, self.__alchemy_engine[db_flavour], index=False,
                                                     if_exists='append')

                            query_user_registry_id = select([table.c.id]).where(table.c.email == signup_payload['email'])
                            user_registry_id = (connection.execute(query_user_registry_id)).fetchall()[0][0]
                            login_payload.update({'user_registry_id': user_registry_id})

                            df_login_payload = pd.DataFrame(login_payload, index=[0])
                            df_login_payload.to_sql('PROTON_login_registry', self.__alchemy_engine[db_flavour],
                                                    index=False, if_exists='append')
                            return {
                                'status': True,
                                'message': 'Signup is successful! Please try login.'
                            }
                        else:
                            return {
                                'status': False,
                                'message': 'User with email {} already exist. Please try '
                                           'login.'.format(signup_payload['email'])
                            }

                    else:
                        # check if schema exists & create one if not.
                        # schema_status = self.pg_schema_generator(self.__alchemy_engine[db_flavour], schema_name)
                        # if schema_status:
                        #     signup_payload.to_sql(table_name, self.__alchemy_engine[db_flavour], index=False,
                        #                           if_exists='append', schema=schema_name)
                        # else:
                        #     self.logger.info('[Signup Controller]: Schema specified not found. Insert operation could '
                        #                      'not be completed. Check connectionManager logs for stack trace.')
                        pass
                    transaction.commit()
                connection.close()
                return True

            except Exception as e:
                self.logger.exception('[Signup Controller]: SignUP payload is incomplete.')
                print(Fore.LIGHTRED_EX + '[Signup Controller]: To perform successful INSERT operation, ensure the input'
                                         ' payload/signup payload is complete.' + Style.RESET_ALL)
                return False
        return False


class IctrlProtonSignup(ProtonSignup):

    def __init__(self):
        super(IctrlProtonSignup, self).__init__()

    def on_get(self, req, resp):

        resp.status = falcon.HTTP_SERVICE_UNAVAILABLE

    def on_post(self, req, resp):
        post_payload = json.loads(req.stream.read())
        results = self.signup(post_payload['db_flavour'], post_payload['signup_payload'])

        resp.body = json.dumps(results)
        resp.status = falcon.HTTP_201






