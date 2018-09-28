__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import json

import pandas as pd
from colorama import Fore
from colorama import Style
from jinjasql import JinjaSql
from nucleus.db.connectionManager import ConnectionManager
from nucleus.generics.utilities import MyUtilities


class Model_{{ modelName }}(ConnectionManager, MyUtilities):
    """
    We will have models dedicated to each new PROTON MIC instantiation. Reason- maintaining separate connectionPool
    for MIC stack respectively. This way, there will be no race condition between models.
    """
    def __init__(self):
        super(Model_{{ modelName }}, self).__init__()

        self.__dbFlavourToCursorGeneratorMap = {
            'postgresql': self.pgCursorGenerator,
            #TODO: Add cursorGenerators for MYSQL and SQL Server when they are available within ConnectionManager.
        }
        self.__jSql = JinjaSql()
        self.__cursorEngine = self.connectionStore()
        self.__alchemyEngine = self.alchemyEngine()

        self.logger = self.getLogger(logFileName='{{ modelName }}',
                                     logFilePath='{}/trace/{{ modelName }}.log'.format(self.ROOT_DIR))

        self.getter = self.__getter()
        self.transaction = self.__transaction()

    def generateSqlTemplate(self, sql):
        """
        Generate Template for JinjaSql to act upon.
        :return:
        """
        template = """
            {}
        """.format(sql)
        return template

    def __getter(self):
        """
        Safe getter.
        TODO: SPECIFY DB Flavour. Make getter work for all supported flavours of PROTON.
        :return:
        """
        def getDataForModel(dbFlavour, sql, bindingParams):
            """

            :param sql: Template:

                SELECT employeeName, employeeAddress
                FROM employee
                WHERE employeeId = {{ employeeId }}
                {% if projectId %}
                AND projectId = {{ projectId }}
                {% endif %}

            :param bindingData: Template:

                data = {
                    "employeeId": 123,
                    "projectId": u"proton"
                }

            :return:
            """
            try:
                with self.__dbFlavourToCursorGeneratorMap[dbFlavour](self.__cursorEngine) as cursor:
                    query, bindParams = self.__jSql.prepare_query(self.generateSqlTemplate(sql), bindingParams)
                    cursor.execute(query, bindParams)
                    results = cursor.fetchall()
                    return json.dumps(results)

            except Exception as e:
                self.logger.exception('[{{modelName}}] - Exception during GETTER. Details: {}'.format(str(e)))
                raise Fore.LIGHTRED_EX + '[{{modelName}}] - Exception during GETTER. ' \
                                         'Details: {}'.format(str(e)) + Style.RESET_ALL


        return {
            "getModelData": getDataForModel,
            # For other getters, create respective closures and extend this dictionary accordingly as per your convenience.
        }

    def __transaction(self):
        """
        Safe Setter!
        TODO: Specify DB Flavour; Make Transactions work for all flavours supported by PROTON.
        :return:
        """

        def performInsertOperation(inputPayload, dbFlavour, dbName, tableName):
            """
            Closure for Insert Operation!
            This is also a proxy for CREATE operation. If table does not exist, SQL Alchemy will create one.
            The newly created table will have best matching datatype for each column.

            :param inputPayload: A dictionary which is Pandas Ready.
                eg. [{'column-1': value, 'column-2: value, column-3: value },
                {'column-1': value, 'column-2: value, column-3: value }]
            :param dbFlavour: One of the supported versions. Must have an entry in dataBaseConfig.ini
            :param dbName: Name of target Database
            :param tableName: tableName into which the given payload is to be uploaded.
            :return: A boolean indicating success/failure of Insert Operation.
            """
            # Do this with SQL Alchemy and Pandas.
            consistencyOfKeys = self.validateListOfDictsConsistency(inputPayload)
            if consistencyOfKeys:
                try:
                    dataToBeInserted = pd.DataFrame(inputPayload)
                    self.__alchemyEngine[dbFlavour].execute('USE {}'.format(dbName))
                    dataToBeInserted.to_sql(tableName, self.__alchemyEngine[dbFlavour], index=False, if_exists='append')
                except Exception as e:
                    self.logger.exception('[{{modelName}}]: {}'.format(str(e)))
                    raise (Fore.LIGHTRED_EX + '[{{modelName}}]: {}'.format(str(e)) + Style.RESET_ALL)
            else:
                self.logger.exception('[{{modelName}}]: To perform successful INSERT operation, ensure the input list of '
                      'dictionaries is consistent in terms of `keys`.')
                raise(Fore.LIGHTRED_EX + '[{{modelName}}]: To perform successful INSERT operation, ensure the input list of '
                      'dictionaries is consistent in terms of `keys`.' + Style.RESET_ALL)


        def performUpdateOrDeleteOperation(sql, bindingParams):
            """

            :param sql: Template:

                UPDATE tableName
                SET column_1 = {{column_1_value}}, column_2 = {{column_2_value}}
                WHERE column_3 = {{ column_3_value }}
                {% if projectId %}
                AND projectId = {{ projectId }}
                {% endif %}


            :param bindingData: Template:

                data = {
                    "column_1_value": 123,
                    "column_2_value": 'dfb',
                    "projectId": u"proton"
                }

            :return:
            """

            try:
                with self.pgCursorGenerator(self.__cursorEngine) as cursor:
                    query, bindParams = self.__jSql.prepare_query(self.generateSqlTemplate(sql), bindingParams)
                    cursor.execute(query, bindParams)
                    cursor.commit()
                    return True
            except Exception as e:
                self.logger.exception('[{{modelName}} -  Exception during UPDATE operation. Details: {}]'.format(str(e)))
                raise (Fore.LIGHTRED_EX + '[{{modelName}} -  Exception during UPDATE operation. Details: '
                                          '{}]'.format(str(e)) + Style.RESET_ALL)



        return {
            'insert': performInsertOperation,
            'update': performUpdateOrDeleteOperation,
            'delete': performUpdateOrDeleteOperation
        }
