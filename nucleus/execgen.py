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

from jinja2 import Environment, FileSystemLoader
from nucleus.db.cache_manager import CacheManager

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class ExecGen(CacheManager):
    """
    Execution files generator for PROTON stack.
    """

    def __init__(self):
        super(ExecGen, self).__init__()
        self.logger = self.get_logger(log_file_name='execGen_logs',
                                      log_file_path='{}/trace/execGen_logs.log'.format(self.ROOT_DIR))
        self.__jinja_env = Environment(loader=FileSystemLoader('{}/nucleus/templates/'.format(self.ROOT_DIR)))
        self.__iface_controllers_root = '{}/mic/iface/controllers'.format(self.ROOT_DIR)
        self.__iface_controllers_template = self.__jinja_env.get_template('iface_controller_template.py')
        self.__executor_template = self.__jinja_env.get_template('executor_template.py')

        self.generate_executor = self.__generate_executor

    def __generate_executor(self, port):
        """

        :return:
        """
        try:

            # Generate API layer based on methods available within generated controller.
            # 1. generate istore from methodExtractorTemplate for current micStack (i_method_fetch.py)
            # 2. from iextractor (which inherits from i_method_fetch.py), get all keys from current controller
            # for current micStack
            from nucleus.iextractorgen import IextractorGen
            ieg = IextractorGen()
            ieg.i_extractor()

            # Generate INTERFACE layer & Generate MAIN from all methods available for each controller in MIC Stack.
            from nucleus.iextractor import IExtractor
            iface_controllers = []
            routes = []
            iface_methods_in_proton_stack = IExtractor().keys_per_controller_in_proton_stack

            for mic_stacks in iface_methods_in_proton_stack:
                iface_controller_methods_hash = []
                for mic in mic_stacks:
                    for ix, method in enumerate(mic_stacks[mic]['restMethodsPerExposedMethod']):
                        iface_controller_methods_hash.append({'fileName': mic_stacks[mic]['fileName'],
                                                              'micName': mic_stacks[mic]['micName'],
                                                              'controllerName': mic_stacks[mic]['controllerName'],
                                                              'iControllerName': list(method.keys())[0],
                                                              'exposedRESTmethods': method[list(method.keys())[0]]})

                        for method_type in method[list(method.keys())[0]]:
                            method_controller_name = 'Ictrl_{}_{}_{}'.format(method_type, mic_stacks[mic]['micName'],
                                                                             list(method.keys())[0])
                            iface_controllers.append({'fileName': 'iface_ctrl_' + mic_stacks[mic]['micName'],
                                                      'controllerName': method_controller_name})
                            routes.append({'controllerName': method_controller_name,
                                           'routeName': method_type+'_{}_{}'.format(mic, list(method.keys())[0])})

                for mic in mic_stacks:
                    # Generate Interface Controller. The I of MIC stack per mic entry in PROTON stack.
                    with open(self.__iface_controllers_root + '/iface_ctrl_{}.py'.format(mic), 'w+') as icf:
                        icf.write(self.__iface_controllers_template.render(iCtrlHash=iface_controller_methods_hash))

            # Generate MAIN
            with open('{}/main.py'.format(self.ROOT_DIR), 'w+') as mf:
                mf.write(self.__executor_template.render(ifaceControllers=iface_controllers, routes=routes, port=port))

        except Exception as e:
            self.logger.exception('[ExecGen] - Exception while generating MAIN for {} MIC stack. '
                                  'Details: {}'.format(self.ROOT_DIR, str(e)))
