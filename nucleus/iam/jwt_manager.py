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

import datetime
import jwt

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class JWTManager:
    from configuration import ProtonConfig
    from nucleus.generics.log_utilities import LogUtilities
    from nucleus.iam.password_manager import PasswordManager
    lg = LogUtilities()
    pm = PasswordManager()

    token_authenticator_logger = lg.get_logger(log_file_name='token_authenticator',
                                               log_file_path='{}/trace/token_authenticator.log'.format(
                                                   ProtonConfig.ROOT_DIR))

    # In proton remote deployment, this must be k8s secret.
    with open('{}/nucleus/iam/secrets/PROTON_JWT_SECRET.txt'.format(ProtonConfig.ROOT_DIR), 'r') as proton_secret:
        app_secret = proton_secret.read().replace('\n', '')
        encoded_app_secret = pm.hash_password(app_secret)

    @classmethod
    def generate_token(cls, encode_value):
        """
        Generate JWT Token which PROTON auth middleware will use to authenticate all protected routes.
        :param encode_value: value that must be considered for JWT encode
        :return: JWT Token
        """

        token = jwt.encode({'encode_value': encode_value, 'exp': datetime.datetime.utcnow() +
                                                                 datetime.timedelta(minutes=30)
                            }, cls.app_secret)  # hashing with encoded, secret, decode fails
        return token.decode('UTF-8')

    @classmethod
    def authenticate(cls, jwt_token):
        """
        Validates if JWT Token still stands True.
        :param jwt_token: JWT Token issued by generate_token method
        :return: A dict containing status and payload on success
        """

        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, cls.app_secret)
            except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
                cls.token_authenticator_logger.exception(
                    '[JWT Manager]: Authentication failed due to : {}'.format(str(e)))
                return {
                    'status': False,
                    'message': 'Token invalid {}'.format(str(e)),
                    'encode_value': None
                }
            cls.token_authenticator_logger.info('[JWT Manager]: Authentication succeded.')
            return {
                'status': True,
                'message': 'Token valid',
                'encode_value': payload['encode_value']
            }
