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
from nucleus.generics.log_utilities import LogUtilities
from nucleus.istore.i_method_fetch import IFetch

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class IExtractor(ProtonConfig, LogUtilities, IFetch):

    def __init__(self, mic_name=None):
        super(IExtractor, self).__init__()
        self.logger = self.get_logger(log_file_name='iextractor_logs',
                                      log_file_path='{}/trace/iextractor_logs.log'.format(self.ROOT_DIR))

        self.logger.info('Extracting available controller methods using IFetch!')
        self.keys_per_controller_in_proton_stack = []
        self.keys_of_requested_controller = []
        if mic_name is not None:
            controller_methods_in_mic_stack = self.extract_controller_methods()
            for index in range(len(controller_methods_in_mic_stack)):
                for key in controller_methods_in_mic_stack[index]:
                    if key == mic_name:
                        self.keys_of_requested_controller = controller_methods_in_mic_stack[index][key][
                            'exposedMethodsInController']
        else:
            self.keys_per_controller_in_proton_stack = self.extract_controller_methods()
