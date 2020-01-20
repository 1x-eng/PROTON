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

import copy
from functools import reduce

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class MyUtilities(object):
    """
    Generic utility functions for PROTON stack
    """

    @staticmethod
    def type_validator(*types):

        def validate_acceptance(f):
            assert len(types) == f.__code__.co_argcount

            def new_f(*args, **kwargs):
                for (a, t) in zip(args, types):
                    assert isinstance(a, t), "arg {} does not match {}".format(a, t)
                return f(*args, **kwargs)

            new_f.__name__ = f.__name__
            return new_f

        return validate_acceptance

    @staticmethod
    def validate_list_of_dicts_consistency(list_of_dicts):
        """
        Validate id all the key value pairs in a list of dictionaries contain same keys.
        eg.  [{'category':2012,'column-1':10},{'category':2013,'column-1':11}] is valid
             [{'category':2012,'column-1':10},{'category':2013,'column-2':11}] is in-valid
        :param list_of_dicts: A list of dictionaries
        :return: A boolean indicating consistency
        """
        if type(list_of_dicts) is not list:
            return False
        else:
            if len(list_of_dicts) < 1:
                return False
            else:
                if not all(map(lambda d: True if type(d) is dict else False, list_of_dicts)):
                    return False
                else:
                    c_rd = copy.deepcopy(list_of_dicts)
                    return any(reduce(lambda i1, i2: i1 if i1 == i2 else [], map(lambda rd: list(rd.keys()), c_rd)))

    @staticmethod
    def validate_proton_post_payload(post_payload):
        """
        Validate if PROTON post payload is in the right format and contains all required fields.
        :param post_payload: a dict. Essentially, falcon post payload.
        :return: A boolean indicating validity
        """
        proton_post_payload = copy.deepcopy(post_payload)
        if type(proton_post_payload) is not dict:
            return False
        required_keys = ['db_flavour', 'db_name', 'schema_name', 'table_name', 'payload']
        actual_keys = list(proton_post_payload.keys())
        if set(required_keys) == set(actual_keys):
            if MyUtilities.validate_list_of_dicts_consistency(proton_post_payload['payload']):
                return True
        return False

    @staticmethod
    def validate_proton_payload_type(base_type_map, actual_payload):
        """
        Validate datatype of a PROTON payload. This is a pre-requisite for all CUD ops. Essentially, this is
        inducing type safety for all db transactions that either creates or modifies existing data.
        :param base_type_map: A dictionary whose key is the actual payload key and value is the expected data type
        for that respective entry.
        :param actual_payload: Actual PROTON payload.
        :return: A dictionary with status of boolean indicating concurrence and a message indicating reason (str)
        """

        if isinstance(base_type_map, dict) and isinstance(actual_payload, dict):
            if base_type_map.keys() == actual_payload.keys():
                if all(elem in actual_payload for elem in base_type_map.keys()):
                    if all(list(isinstance(actual_payload[elem], base_type_map[elem]) for elem in base_type_map)):
                        return {
                            'status': True,
                            'message': 'Payload complies with expected types.'
                        }
                    else:
                        return {
                            'status': False,
                            'message': 'Given payload does not match with expected types. '
                                       'Expected types are: {}'.format(str(base_type_map))
                        }
                else:
                    return {
                        'status': False,
                        'message': 'Given payload does not contain all expected columns. '
                                   'Expected columns and types are: {}'.format(str(base_type_map))
                    }
            else:
                return {
                    'status': False,
                    'message': 'Given payload is not in agreement with required metadata for PROTON transaction.'
                               ' Expected metadata: {}'.format(str(base_type_map))
                }
        else:
            return {
                'status': False,
                'message': 'Validation not possible unless actual payload(dict) and type map(dict) are provided.'
            }
