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
from nucleus.db.connection_manager import ConnectionManager
from nucleus.email.email import ProtonEmail
from nucleus.generics.utilities import MyUtilities
from nucleus.iam.password_manager import PasswordManager
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import Table

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class ProtonUserReset(ConnectionManager, PasswordManager, ProtonEmail, MyUtilities):

    def __init__(self):
        super(ProtonUserReset, self).__init__()
        self.__alchemy_engine = self.alchemy_engine()
        self.iam_user_reset_logger = self.get_logger(log_file_name='iam_user_reset_logs.log',
                                                     log_file_path='{}/trace/iam_user_reset_logs.log'.format(
                                                         self.ROOT_DIR))

    def proton_reset_user(self, db_flavour, schema_name, reset_payload):
        try:
            if isinstance(reset_payload, dict):
                reset_password_metadata = {
                    'user_name': str,
                    'email': str,
                    'password': str
                }
                validation_results = self.validate_proton_payload_type(reset_password_metadata, reset_payload)

                if validation_results['status'] and db_flavour == 'postgresql':

                    schema_status = self.__alchemy_engine[db_flavour].dialect.has_schema(
                        self.__alchemy_engine[db_flavour], schema_name)
                    metadata = MetaData(self.__alchemy_engine[db_flavour], reflect=True, schema=schema_name)
                    metadata.reflect(self.__alchemy_engine[db_flavour])
                    connection = self.__alchemy_engine[db_flavour].connect()

                    with connection.begin() as transaction:
                        if schema_status:
                            user_registry_table = Table('PROTON_user_registry', metadata)
                            query_user_id = select([user_registry_table.c.id]).where(
                                user_registry_table.c.email == reset_payload['email'])
                            user_id = (connection.execute(query_user_id)).fetchall()

                            if len(user_id) == 0:
                                return json.dumps({
                                    'message': 'Unable to reset password.',
                                    'reason': {
                                        'message': 'Invalid Email. There is no registered user with that email.'
                                    },
                                    'status': False
                                })
                            else:
                                login_registry_table = Table('PROTON_login_registry', metadata)
                                query_user_existence = select([login_registry_table.c.user_registry_id]).where(
                                    login_registry_table.c.user_name == reset_payload['user_name'])
                                user_existence = (connection.execute(query_user_existence)).fetchall()

                                if len(user_existence) == 0:
                                    return json.dumps({
                                        'message': 'Unable to reset password.',
                                        'reason': {
                                            'message': 'Invalid Username. Please enter the username and '
                                                       'email as provided during signup.'
                                        },
                                        'status': False
                                    })
                                else:
                                    if user_id[0][0] != user_existence[0][0]:
                                        return json.dumps({
                                            'message': 'Unable to reset password.',
                                            'reason': {
                                                'message': 'Given email and username do not match. Please enter the '
                                                           'username and email as provided during signup.'
                                            },
                                            'status': False
                                        })
                                    else:
                                        password_update_query = login_registry_table.update().where(login_registry_table.c.user_registry_id==user_existence[0][0]).values(password=self.hash_password(reset_payload['password']))
                                        password_update_results = (connection.execute(password_update_query))

                                        if self.iam_user_reset_logger.info(password_update_results.rowcount) != 0:
                                            return json.dumps({
                                                'message': 'Password reset successful.',
                                                'status': True,
                                            })
                                        else:
                                            return json.dumps({
                                                'message': 'Password reset unsuccessful due to server side error.',
                                                'status': False,
                                            })

                else:
                    return json.dumps({
                        'message': 'Unable to reset password.',
                        'reason': {
                            'message': 'Required payload for password reset is: {}'.format(str(reset_password_metadata))
                        },
                        'status': False
                    })
            return json.dumps({
                'message': 'Unable to reset password.',
                'reason': {
                    'message': """POST payload for /reset route must be:
                    {
                        "db_flavour": "postgresql",
                        "reset_payload": { 
                            "user_name": "<username>",
                            "email": "<email@email.com>",
                            "password": "<your new password>"
                        }
                    }
                    """
                },
                'status': False
            })

        except Exception as e:
            self.iam_user_reset_logger.exception('[Proton IAM] - Exception while resetting PROTON user password. '
                                                 'Details: {}'.format(str(e)))


class IctrlProtonPasswordReset(ProtonUserReset):

    def __init__(self):
        super(IctrlProtonPasswordReset, self).__init__()

    def on_get(self, req, resp):

        resp.status = falcon.HTTP_SERVICE_UNAVAILABLE

    def on_post(self, req, resp):
        try:
            post_payload = json.loads(req.stream.read())
            results = self.proton_reset_user(post_payload['db_flavour'],
                                             'iam',
                                             post_payload['reset_payload'])

            resp.body = results
            resp.status = falcon.HTTP_201
        except Exception as e:
            resp.body = json.dumps({
                'message': "POST request must contain 'db_flavour'[PROTON supports `sqlite` or `postgresql`] "
                           "and 'reset_payload'"
            })
            resp.status = falcon.HTTP_403
