#!/usr/bin/env python

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

import argparse
import os
import shutil
from colorama import Fore, Style
from nucleus.db.cache_manager import CacheManager

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class ProtonKill(CacheManager):
    """
    ProtonKill.py will kill existence of given mic_name across PROTON stack. However, protonKill is not taking care of
    re-generating or altering created dependency for deleted mic from main.py. This will have to be accounted for in
    execgen.py
    """
    def __init__(self):
        super(ProtonKill, self).__init__()
        self.logger = self.get_logger(log_file_name='proton_kill_logs',
                                      log_file_path='{}/trace/proton_kill_logs.log'.format(self.ROOT_DIR))
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--micNameToKill')
        self.proton_args = self.parser.parse_args()

        if self.proton_args.micNameToKill is None:
            print(Fore.LIGHTRED_EX + '[Proton kill] - Please provide a valid MIC Name. A name that exists in PROTON '
                                     'stack! Use --micNameToKill option' + Style.RESET_ALL)
        else:
            self.destroy_mic_stack(self.proton_args.micNameToKill)

    def destroy_mic_stack(self, mic_name):

        try:
            # Delete cache entry for all methods of micStack intended for deletion
            cache_instance = self.cache_processor()['init_cache']()
            from nucleus.iextractor import IExtractor
            iface_methods_in_proton_stack = IExtractor(mic_name).keys_of_requested_controller

            for method in iface_methods_in_proton_stack:
                self.cache_processor()['delete_from_cache'](cache_instance, 'c_{}_{}'.format(mic_name, method))
                self.cache_processor()['delete_from_cache'](cache_instance, 'c_setTime_{}_{}'.format(mic_name, method))
                self.logger.info('Cache entry for mic stack of "{}" is deleted successfully!'.format(mic_name))

            model_path = '{}/mic/models/{}'.format(self.ROOT_DIR, mic_name)
            controller_path = '{}/mic/controllers/controller_{}.py'.format(self.ROOT_DIR, mic_name)
            iface_controller_path = '{}/mic/iface/controllers/iface_ctrl_{}.py'.format(self.ROOT_DIR, mic_name)
            model_existance = os.path.isdir(model_path)

            if model_existance:
                shutil.rmtree(model_path, ignore_errors=True)
                os.remove(controller_path)
                os.remove(iface_controller_path)
                self.logger.info('PROTON MIC for {} is killed successfully!'.format(mic_name))
                print(Fore.YELLOW + 'PROTON MIC for {} is killed successfully!'.format(mic_name) + Style.RESET_ALL)

        except Exception as e:
            self.logger.exception('PROTON MIC destruction for mic_name {} is unsuccessful. '
                                  'Details: {}'.format(mic_name, str(e)))


if __name__ == '__main__':
    ProtonKill()



