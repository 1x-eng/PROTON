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
import os
from datetime import datetime
from nucleus.db.connection_manager import ConnectionManager
from nucleus.email.email import ProtonEmail
from nucleus.iam.jwt_manager import JWTManager
from nucleus.iam.password_manager import PasswordManager
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import Table

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class ProtonLogin(ConnectionManager, PasswordManager, JWTManager, ProtonEmail):

    def __init__(self):
        super(ProtonLogin, self).__init__()
        self.__alchemy_engine = self.alchemy_engine()
        self.iam_login_logger = self.get_logger(log_file_name='iam_login_logs.log',
                                                log_file_path='{}/trace/iam_login_logs.log'.format(self.ROOT_DIR))

    def login(self, db_flavour, login_payload, db_name='proton', schema_name='iam', table_name='PROTON_login_registry'):
        """
        Logs in valid PROTON users.

        :param db_flavour: One of the supported versions. Must have an entry in dataBaseConfig.ini
        :param db_name: Name of target Database. Default: Proton
        :param schema_name: Name of target schema. Default: iam
        :param table_name: Name of target table. Default: PROTON_user_registry
        :param login_payload: Payload of users login details.
        :return: A dictionary containing login status, message & JWT token is successful.
        """

        def validate_login_payload(payload):

            def validate_payload_contents(payload):
                """
                Validates that payload contains atleast one character. More stringent form validation
                must be a client side operation.
                :param payload: login payload
                :return: Boolean
                """
                validity_store = []
                for k, v in payload.items():
                    if len(str(v)) > 0:
                        validity_store.append(True)
                    else:
                        validity_store.append(False)
                if all(validity_store):
                    return True
                return False

            if type(payload) is not dict:
                return False
            required_keys = ['user_name', 'password']

            actual_keys = list(payload.keys())
            if set(required_keys) == set(actual_keys):
                return validate_payload_contents(payload)
            return False

        if validate_login_payload(login_payload):
            try:
                login_payload.update({'last_login_date_time': datetime.now()})

                connection = self.__alchemy_engine[db_flavour].connect()

                with connection.begin() as transaction:
                    if db_flavour == 'sqlite':
                        metadata = MetaData(self.__alchemy_engine[db_flavour], reflect=True)
                        table = metadata.tables[table_name]

                        # Check if user exists:
                        query_existence = select([table.c.id]).where(table.c.user_name == login_payload['user_name'])
                        existence_results = (connection.execute(query_existence)).fetchall()

                        if len(existence_results) == 0:
                            self.iam_login_logger.info(
                                '[ProtonLogin]:[SQLite] Invalid user_name. Proton denies login for '
                                '{}'.format(login_payload['user_name']))
                            return {
                                'status': False,
                                'message': 'Invalid user_name. Please try again with valid credentials.',
                                'token': None
                            }
                        else:
                            # Check if password matches.
                            query_stored_password = select([table.c.password]).where(
                                table.c.user_name == login_payload['user_name'])
                            stored_password = (connection.execute(query_stored_password)).fetchall()[0][0]
                            password_match = self.verify_password(stored_password, login_payload['password'])

                            # Get registered email to notify upon login.
                            user_registry_table = metadata.tables['PROTON_user_registry']
                            query_user_registry_id = select([table.c.user_registry_id]).where(
                                table.c.user_name == login_payload['user_name'])
                            user_registry_id = (connection.execute(query_user_registry_id)).fetchall()[0][0]
                            query_registered_email = select([user_registry_table.c.email]).where(
                                user_registry_table.c.id == user_registry_id)
                            registered_email = (connection.execute(query_registered_email)).fetchall()[0][0]

                            if not password_match:
                                self.iam_login_logger.info(
                                    '[ProtonLogin]:[SQLite] Invalid password. Proton denies login for '
                                    '{}'.format(login_payload['user_name']))
                                self.send_email(registered_email,
                                                '{} - Invalid Login Attempt'.format(
                                                    os.environ.get('APP_NAME')),
                                                '<span>Hi {},<br /><br />'
                                                'Someone (hopefully you) '
                                                'tried to login to {} with'
                                                'invalid credentials. If '
                                                'you did not make this '
                                                'attempt, please contact '
                                                '{} immediately.<br /><br />'
                                                '<i>We strongly advise '
                                                'to choose strong password '
                                                'to {} app. Examples of '
                                                'strong password - https://1password.com/password-generator/'
                                                '</i>'.format(login_payload['user_name'],
                                                              os.environ.get('APP_NAME'),
                                                              os.environ.get('APP_SUPPORT_EMAIL'),
                                                              os.environ.get('APP_NAME')))
                                return {
                                    'status': False,
                                    'message': 'Invalid password. Please try again with valid credentials',
                                    'token': None
                                }
                            else:
                                self.iam_login_logger.info(
                                    '[ProtonLogin]:[SQLite] Valid login. Proton login successful for '
                                    '{}'.format(login_payload['user_name']))
                                token = self.generate_token(login_payload['user_name'])
                                self.send_email(registered_email,
                                                '{} - Successful Login'.format(
                                                    os.environ.get('APP_NAME')),
                                                '<span>Hi {},<br /><br />'
                                                'Someone (hopefully you) '
                                                'has successfully logged in to {}.<br/><br />'
                                                'If '
                                                'you did not make this '
                                                'attempt, please contact '
                                                '{} immediately.<br /><br />'
                                                '<i>We strongly advise '
                                                'to choose strong password '
                                                'to {} app. Examples of '
                                                'strong password - '
                                                'https://1password.com/password-generator/'
                                                '</i>'.format(login_payload['user_name'],
                                                              os.environ.get('APP_NAME'),
                                                              os.environ.get('APP_SUPPORT_EMAIL'),
                                                              os.environ.get('APP_NAME')))
                                return {
                                    'status': True,
                                    'message': 'Successful Login',
                                    'token': token
                                }
                    elif db_flavour == 'postgresql':
                        schema_status = self.__alchemy_engine[db_flavour].dialect.has_schema(
                            self.__alchemy_engine[db_flavour], schema_name)
                        metadata = MetaData(self.__alchemy_engine[db_flavour], reflect=True, schema=schema_name)
                        metadata.reflect(self.__alchemy_engine[db_flavour])

                        if schema_status:
                            # Check if user exists:
                            login_registry_table = Table('PROTON_login_registry', metadata)
                            query_existence = select([login_registry_table.c.id]).where(
                                login_registry_table.c.user_name == login_payload['user_name'])
                            existence_results = (connection.execute(query_existence)).fetchall()

                            if len(existence_results) == 0:
                                self.iam_login_logger.info(
                                    '[ProtonLogin]:[Postgresql] Invalid user_name. Proton denies login '
                                    'for {}'.format(login_payload['user_name']))
                                return {
                                    'status': False,
                                    'message': 'Invalid user_name. Please try again with valid credentials.',
                                    'token': None
                                }
                            else:
                                # Check if password matches.
                                query_stored_password = select([login_registry_table.c.password]).where(
                                    login_registry_table.c.user_name == login_payload['user_name'])
                                stored_password = (connection.execute(query_stored_password)).fetchall()[0][0]
                                password_match = self.verify_password(stored_password, login_payload['password'])

                                # Get registered email to notify upon login.
                                user_registry_table = Table('PROTON_user_registry', metadata)
                                query_user_registry_id = select([login_registry_table.c.user_registry_id]).where(
                                    login_registry_table.c.user_name == login_payload['user_name'])
                                user_registry_id = (connection.execute(query_user_registry_id)).fetchall()[0][0]
                                query_registered_email = select([user_registry_table.c.email]).where(
                                    user_registry_table.c.id == user_registry_id)
                                registered_email = (connection.execute(query_registered_email)).fetchall()[0][0]

                                if not password_match:
                                    self.iam_login_logger.info(
                                        '[ProtonLogin]:[Postgresql] Invalid password. Proton denies login for '
                                        '{}'.format(login_payload['user_name']))
                                    self.send_email(registered_email,
                                                    '{} - Invalid Login Attempt'.format(
                                                        os.environ.get('APP_NAME')),
                                                    '<span>Hi {},<br /><br />'
                                                    'Someone (hopefully you) '
                                                    'tried to login to {} with'
                                                    'invalid credentials. If '
                                                    'you did not make this '
                                                    'attempt, please contact '
                                                    '{} immediately.<br /><br />'
                                                    '<i>We strongly advise '
                                                    'to choose strong password '
                                                    'to {} app. Examples of '
                                                    'strong password - https://1password.com/password-generator/'
                                                    '</i>'.format(login_payload['user_name'],
                                                                  os.environ.get('APP_NAME'),
                                                                  os.environ.get('APP_SUPPORT_EMAIL'),
                                                                  os.environ.get('APP_NAME')))
                                    return {
                                        'status': False,
                                        'message': 'Invalid password. Please try again with valid credentials.',
                                        'token': None
                                    }
                                else:
                                    self.iam_login_logger.info(
                                        '[ProtonLogin]:[Postgresql] Valid login. Proton login successful for '
                                        '{}'.format(login_payload['user_name']))
                                    token = self.generate_token(login_payload['user_name'])
                                    self.send_email(registered_email,
                                                    '{} - Successful Login'.format(
                                                        os.environ.get('APP_NAME')),
                                                    '<span>Hi {},<br /><br />'
                                                    'Someone (hopefully you) '
                                                    'has successfully logged in to {}.<br/><br />'
                                                    'If '
                                                    'you did not make this '
                                                    'attempt, please contact '
                                                    '{} immediately.<br /><br />'
                                                    '<i>We strongly advise '
                                                    'to choose strong password '
                                                    'to {} app. Examples of '
                                                    'strong password - '
                                                    'https://1password.com/password-generator/'
                                                    '</i>'.format(login_payload['user_name'],
                                                                  os.environ.get('APP_NAME'),
                                                                  os.environ.get('APP_SUPPORT_EMAIL'),
                                                                  os.environ.get('APP_NAME')))
                                    return {
                                        'status': True,
                                        'message': 'Successful Login',
                                        'token': token,
                                        'id': existence_results[0][0]
                                    }
                        else:
                            self.iam_login_logger.info(
                                '[ProtonLogin]:[Postgresql] {} schema does not exist. Proton denies login '
                                'for {}'.format(schema_name, login_payload['user_name']))
                            return {
                                'status': False,
                                'message': 'Login not possible due to server side error. Please try again in sometime.',
                                'token': None
                            }
                    else:
                        self.iam_login_logger.info(
                            '[ProtonLogin]: New Login is unsuccessful due to unsupported db_flavour. Proton '
                            'was asked for {} to login; by, {}'.format(db_flavour,
                                                                       login_payload['user_name']))
                        return {
                            'status': False,
                            'message': 'PROTON only supports SQLite and Postgresql atm. Do you have valid db_flavour '
                                       'in your payload?',
                            'token': None
                        }
                    transaction.commit()
                connection.close()

            except Exception as e:
                self.iam_login_logger.info('[ProtonLogin]: Exception while loggin in User. Stack trace to follow')
                self.iam_login_logger.exception(str(e))

            finally:
                if connection:
                    connection.close()


class IctrlProtonLogin(ProtonLogin):

    def __init__(self):
        super(IctrlProtonLogin, self).__init__()

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_SERVICE_UNAVAILABLE

    def on_post(self, req, resp):
        try:
            post_payload = json.loads(req.stream.read())
            results = self.login(post_payload['db_flavour'], post_payload['login_payload'])

            resp.body = json.dumps(results)
            resp.status = falcon.HTTP_200

        except Exception as e:
            resp.body = json.dumps({
                'message': "POST request must contain 'db_flavour'[PROTON supports `sqlite` or `postgresql`] and "
                           "'login_payload'."
            })
            resp.status = falcon.HTTP_403
