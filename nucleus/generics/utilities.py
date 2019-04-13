__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import copy
from functools import reduce

class MyUtilities(object):
    """
    Generic utility functions for PROTON stack
    """

    @staticmethod
    def validate_list_of_dicts_consistency(list_of_dicts):
        """
        Validate id all the key value pairs in a list of dictionaries contain same keys.
        eg.  [{'category':2012,'column-1':10},{'category':2013,'column-1':11}] is valid
             [{'category':2012,'column-1':10},{'category':2013,'column-2':11}] is in-valid
        :param list_of_dicts: A list of dictionaries
        :return: A boolean indicating consistency
        """
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
