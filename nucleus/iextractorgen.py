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
from jinja2 import Environment, FileSystemLoader
from configuration import ProtonConfig
from nucleus.generics.log_utilities import LogUtilities

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class IextractorGen(LogUtilities, ProtonConfig):

    def __init__(self):
        super(IextractorGen, self).__init__()
        self.logger = self.get_logger(log_file_name='iextractor_logs',
                                      log_file_path='{}/trace/iextractor_logs.log'.format(self.ROOT_DIR))
        self.__iface_store_root = '{}/nucleus/istore'.format(self.ROOT_DIR)
        self.__jinja_env = Environment(loader=FileSystemLoader('{}/nucleus/templates/'.format(self.ROOT_DIR)))
        self.__iface_extractor_template = self.__jinja_env.get_template('iface_method_extractor_template.py')

    def i_extractor(self):

        # Need all controller file and controller class Named within mic Stack.
        controllers = []
        for root, dirs, files in os.walk("{}/mic/controllers/".format(self.ROOT_DIR)):
            for filename in files:
                if '__init__' in filename or 'cpython' in filename:
                    pass
                else:
                    file_name_contents = (filename.split('.py')[0].split('_'))
                    desired_name = '_'.join(file_name_contents[1:])
                    file_name = filename.split('.py')[0]
                    self.logger.info('i_extractor updated i_method_fetch.py with mic_name {}'.format(desired_name))
                    controllers.append({'micName': desired_name, 'fileName': file_name,
                                        'controllerName': 'Ctrl_{}'.format(desired_name)})

        with open(self.__iface_store_root + '/i_method_fetch.py', 'w+') as isf:
            isf.write(self.__iface_extractor_template.render(controllers=controllers))
