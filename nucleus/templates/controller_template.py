__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import json
import numpy as np
import pandas as pd
from colorama import Fore
from colorama import Style
from mic.models.{{ modelName }}.model_{{ modelName }} import Model_{{modelName}}

class Ctrl_{{ controllerName }}(Model_{{ modelName }}):

    def __init__(self):
        super( Ctrl_{{ controllerName }}, self ).__init__()
        self.logger = self.getLogger(logFileName='{{ controllerName }}',
                                     logFilePath='{}/trace/{{ controllerName }}.log'.format(self.ROOT_DIR))
        self.controllerProcessor = self.__processor


    def __processor(self):
        """
        All methods in controller will have access to getters and transaction methods from its respective models.

        Here, developer could choose to process data obtained from DB and prepare it(serialize it) for transmission.

        :return: serialized response ready for transmission to Interface.
        """

        def schemaInformation(dbFlavour):

            # This SQL is an example to list all tables in the current database.
            example_sql = """
            SELECT table_schema, table_name
            FROM information_schema.tables
            ORDER BY table_schema,table_name;
            """
            binding_params = {}
            try:
                # to use getter methods, use self.getter; to use transaction methods, use self.transaction.
                # to learn more, do dir(self.getter) and dir(self.transaction).

                results = self.getter["getModelData"](dbFlavour, example_sql, binding_params)
                return results
            except Exception as e:
                self.logger.exception('[{{ controllerName }}] - Exception while getting model data. '
                                      'Details: {}'.format(str(e)))
                raise Fore.LIGHTRED_EX + '[{{ controllerName }}] - Exception while getting model data. ' \
                                         'Details: {}'.format(str(e)) + Style.RESET_ALL


        return {
            "schemaInformation": schemaInformation,
            # Similar to above, add more processor methods according to developer's convenience.
        }



