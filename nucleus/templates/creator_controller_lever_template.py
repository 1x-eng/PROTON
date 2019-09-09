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
from mic.models.{{ modelName }}.model_{{ modelName }} import Model_{{modelName}}

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class Creator(Model_{{ modelName }}):

    def __init__(self):
        super(Creator, self).__init__()

    def proton_{{ modelName }}_creator(self, db_flavour, db_name, schema_name, table_name, input_payload,
                                       expected_metadata, log_head):

        try:
            if len(input_payload) > 0:
                validation_results = list(map(lambda p: self.validate_proton_payload_type(expected_metadata),
                                              input_payload))

                if all(r['status'] for r in validation_results):
                    self.transaction['insert'](db_flavour, db_name, schema_name, table_name, input_payload)
                    return {
                        'message': 'Insert operation to {}.{} table in {} database under {} '
                                   'is successful'.format(schema_name, table_name, db_name, db_flavour),
                        'status': True
                    }
                else:
                    return {
                        'message': 'Insert operation to {}.{} table in {} database under {} was '
                                   'unsuccessful'.format(schema_name, table_name, db_name, db_flavour),
                        'reason': validation_results,
                        'status': False
                    }
            else:
                return {
                    'message': 'Insert operation to {}.{} table in {} database under {} was '
                               'unsuccessful'.format(schema_name, table_name, db_name, db_flavour),
                    'reason': 'Cannot insert nothing! Please provide valid input payload that complies with '
                              'expected datatypes of sparkle sections table. '
                              'Expected types: {}'.format(str(expected_metadata)),
                    'status': False
                }

        except Exception as e:
            log_head.exception('[{{modelName}}] - Exception while inserting data. '
                             'Details: {}'.format(str(e)))




