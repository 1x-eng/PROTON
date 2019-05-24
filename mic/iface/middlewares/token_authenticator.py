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

from configuration import ProtonConfig
from nucleus.iam.jwt_manager import JWTManager
from nucleus.generics.log_utilities import LogUtilities
import falcon
import time

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class TokenAuthenticator(LogUtilities, ProtonConfig, JWTManager):

    def __init__(self):
        super(TokenAuthenticator, self).__init__()
        self.logger = self.get_logger(log_file_name='token_authenticator',
                                      log_file_path='{}/trace/token_authenticator.log'.format(self.ROOT_DIR))

    def process_request(self, req, resp):
        """

        :param req:
        :param resp:
        :return:
        """
        # TODO: Validate JWT Token and on success, bind to req object.
        if (req.path in ['/',
                         '/fast-serve',
                         '/signup',
                         '/login',
                         '/metrics']):
            if req.path == '/metrics':
                setattr(req.context, 'start_time', time.time())
            pass
        else:
            setattr(req.context, 'cache_ready', False)
            challenges = ['Token type="Fernet"']
            token = req.get_header('Authorization')
            if token is None:
                self.logger.exception('[Token Authenticator]: Request to {}[{}] is missing '
                                      'authentication token.'.format(req.path, req.uri))
                raise falcon.HTTPUnauthorized('Auth token required.', 'Please provide an auth token via Authorization '
                                                                      'header; as part of the request.', challenges)
            else:
                if not self.authenticate(token)['status']:
                    self.logger.exception('[Token Authenticator]: Request to {}[{}] has failed '
                                          'authentication. Token - [] is expired/invalid'.format(req.path, req.uri,
                                                                                                 token))
                    raise falcon.HTTPUnauthorized('Authentication required.', 'Token is invalid. Either expired or '
                                                                              'invalid.', challenges)
                else:
                    setattr(req.context, 'cache_ready', True)
                    self.logger.info('[Token Authenticator]: Request to {}[{}] is valid.'.format(req.path, req.uri))

