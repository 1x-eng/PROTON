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

import os
import argparse
from colorama import Fore, Style
from nucleus.execgen import ExecGen
from nucleus.metagen import MetaGen

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class ProtonGen(MetaGen, ExecGen):

    def __init__(self):
        super(ProtonGen, self).__init__()
        self.logger = self.get_logger(log_file_name='proton_gen_logs',
                                      log_file_path='{}/trace/proton_gen_logs.log'.format(self.ROOT_DIR))
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--mic_name', help='MIC stands for Model Interface & Controller. Proton spins up'
                                 'the MIC stack for you; when provided with a name.')
        self.parser.add_argument('--port', help='Port for PROTON to launch the interface onto. Defaults to 3000.')
        self.parser.add_argument('--forceStart', help='Do not create a new MIC Stack; but, executes PROTON stack '
                                                      'by re-generating main with existing iFace!')
        self.proton_args = self.parser.parse_args()

        if self.proton_args.mic_name is None:
            if self.proton_args.forceStart is not None:
                self.bootstrap_sqlite()
                self.generate_executor(port=3000)
                print(Fore.GREEN + 'PROTON initialized with existing iFace stack! Starting service '
                                   '@ 3000' + Style.RESET_ALL)
                self.logger.info('PROTON initialized with existing iFace stack! Starting service @ 3000')
            else:
                raise (Fore.LIGHTRED_EX + '[PROTON-GEN] - There is no name provided for Proton to initiate. '
                                          'Please provide a valid mic_name using --mic_name argument' + Style.RESET_ALL)
        else:
            if self.proton_args.port is None:
                self.proton_args.port = 8000
            self.__creator(self.proton_args.mic_name, self.proton_args.port)

    def __creator(self, mic_name, port):

        try:

            with open('{}/proton_vars/target_table_for_{}.txt'.format(self.ROOT_DIR,  mic_name)) as f:
                target_table_for_mic = f.read().replace('\n', '')

            self.new_mic(mic_name=mic_name)
            self.generate_executor(port=port)
            print(Fore.GREEN + 'PROTON initialized for {}. Starting service @ {} & target table for this MIC '
                  'stack is - {}'.format(mic_name, port, target_table_for_mic) + Style.RESET_ALL)
            self.logger.info('[ProtonGen] Proton initialized for mic_name - {} @ port {} & target table for '
                             'this MIC stack is -{}'.format(mic_name, port, target_table_for_mic))
        except Exception as e:
            self.logger.exception('[ProtonGen] Error during protonGen initialization for mic_name '
                                  '{}. Details: {}'.format(mic_name, str(e)))
            raise (Fore.LIGHTRED_EX + '[ProtonGen] Error during protonGen initialization for mic_name '
                   '{}. Details: {}'.format(mic_name, str(e)) + Style.RESET_ALL)

if __name__ == '__main__':
    pg = ProtonGen()


