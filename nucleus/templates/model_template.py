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

import json
import pandas as pd
from colorama import Fore
from colorama import Style
from jinjasql import JinjaSql
from nucleus.db.connection_manager import ConnectionManager
from nucleus.generics.utilities import MyUtilities

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class Model_{{ modelName }}(ConnectionManager, MyUtilities):
    """
    We will have models dedicated to each new PROTON MIC instantiation. Reason- maintaining separate connectionPool
    for MIC stack respectively. This way, there will be no race condition between models.
    """
    def __init__(self):
        super(Model_{{ modelName }}, self).__init__()

        self.__db_flavour_to_cursor_generator_map = {
            'sqlite': self.sqlite_connection_generator,
            'postgresql': self.pg_cursor_generator,
            # TODO: Add cursorGenerators for MYSQL and SQL Server when they are available within ConnectionManager.
        }
        self.__j_sql = JinjaSql(param_style='named')
        self.__cursor_engine = self.connection_store()
        self.__alchemy_engine = self.alchemy_engine()

        self.model_{{ modelName }}_logger = self.get_logger(log_file_name='{{ modelName }}',
                                                            log_file_path='{}/trace/{{ modelName }}.log'.format(self.ROOT_DIR))

        self.getter = self.__getter()
        self.transaction = self.__transaction()

    def generate_sql_template(self, sql):
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
        def get_data_for_model(db_flavour, sql, binding_params):
            """

            :param sql: Template:

                {% raw %}

                SELECT employeeName, employeeAddress
                FROM employee
                WHERE employeeId = {{ employeeId }}
                {% if projectId %}
                AND projectId = {{ projectId }}
                {% endif %}

                {% endraw %}

            :param binding_params: Template:

                data = {
                    "employeeId": 123,
                    "projectId": u"proton"
                }

            :return:
            """
            if db_flavour == 'sqlite':
                # lite database
                try:
                    connection = self.sqlite_connection_generator()
                    cursor = connection.cursor()
                    query, bind_params = self.__j_sql.prepare_query(self.generate_sql_template(sql), binding_params)
                    cursor.execute(query, binding_params)
                    results = cursor.fetchall()
                    results_df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
                    return results_df.to_json(orient='records')
                except Exception as e:
                    connection.rollback()
                    self.model_{{ modelName }}_logger.exception('[{{modelName}}] - Exception during GETTER. Details: {}'.format(str(e)))
                    print(Fore.LIGHTRED_EX + '[{{modelName}}] - Exception during GETTER. '
                                             'Details: {}'.format(str(e)) + Style.RESET_ALL)
                finally:
                    connection.close()
            else:
                # Prodgrade databases
                try:
                    with self.__db_flavour_to_cursor_generator_map[db_flavour](self.__cursor_engine) as cursor:
                        query, bind_params = self.__j_sql.prepare_query(self.generate_sql_template(sql), binding_params)
                        cursor.execute(query, bind_params)
                        results_headers= [x[0] for x in cursor.description]
                        results = cursor.fetchall()
                        json_response = []
                        for r in results:
                            json_response.append(dict(zip(results_headers, r)))
                        return json.dumps(json_response)

                except Exception as e:
                    self.model_{{ modelName }}_logger.exception('[{{modelName}}] - Exception during GETTER. Details: {}'.format(str(e)))
                    print(Fore.LIGHTRED_EX + '[{{modelName}}] - Exception during GETTER. '
                                             'Details: {}'.format(str(e)) + Style.RESET_ALL)

        return {
            "get_model_data": get_data_for_model,
            # For other getters, create respective closures and extend this dictionary accordingly to your convenience.
        }

    def __transaction(self):
        """
        Safe Setter!
        TODO: Specify DB Flavour; Make Transactions work for all flavours supported by PROTON.
        :return:
        """

        def perform_insert_operation(db_flavour, db_name, schema_name, table_name, input_payload):
            """
            Closure for Insert Operation!
            This is also a proxy for CREATE operation. If table does not exist, SQL Alchemy will create one.
            The newly created table will have best matching data type for each column.

            :param input_payload: A dictionary which is Pandas Ready.
                eg. [{'column-1': value, 'column-2: value, column-3: value },
                {'column-1': value, 'column-2: value, column-3: value }]
            :param db_flavour: One of the supported versions. Must have an entry in dataBaseConfig.ini
            :param db_name: Name of target Database
            :param table_name: table_name into which the given payload is to be uploaded.
            :return: A boolean indicating success/failure of Insert Operation.
            """
            # Do this with SQL Alchemy and Pandas.
            consistency_of_keys = self.validate_list_of_dicts_consistency(input_payload)
            if consistency_of_keys:
                try:
                    data_to_be_inserted = pd.DataFrame(input_payload)
                    connection = self.__alchemy_engine[db_flavour].connect()
                    with connection.begin() as transaction:
                        if db_flavour == 'sqlite':
                            data_to_be_inserted.to_sql(table_name, self.__alchemy_engine[db_flavour], index=False,
                                                       if_exists='append')
                        else:
                            # check if schema exists & create one if not.
                            schema_status = self.pg_schema_generator(self.__alchemy_engine[db_flavour], schema_name)
                            if schema_status:
                                data_to_be_inserted.to_sql(table_name, self.__alchemy_engine[db_flavour], index=False,
                                                           if_exists='append', schema=schema_name)
                            else:
                                self.model_{{ modelName }}_logger.info('[{{modelName}}]: Schema specified not found. Insert operation could '
                                                 'not be completed. Check connectionManager logs for stack trace.')
                        transaction.commit()
                    connection.close()
                except Exception as e:
                    self.model_{{ modelName }}_logger.exception('[{{modelName}}]: {}'.format(str(e)))
                    print(Fore.LIGHTRED_EX + '[{{modelName}}]: {}'.format(str(e)) + Style.RESET_ALL)
                    if connection:
                        connection.close()
                finally:
                    if connection:
                        connection.close()
            else:
                        self.model_{{ modelName }}_logger.exception('[{{modelName}}]: To perform successful INSERT operation, ensure the input list '
                                              'of dictionaries is consistent in terms of `keys`.')
                        print(Fore.LIGHTRED_EX + '[{{modelName}}]: To perform successful INSERT operation, ensure the input '
                              'list of dictionaries is consistent in terms of `keys`.' + Style.RESET_ALL)

        def perform_update_or_delete_operation(sql, binding_params):
            """

            :param sql: Template:

                {% raw %}

                UPDATE tableName
                SET column_1 = {{column_1_value}}, column_2 = {{column_2_value}}
                WHERE column_3 = {{ column_3_value }}
                {% if projectId %}
                AND projectId = {{ projectId }}
                {% endif %}

                {% endraw %}


            :param binding_params: Template:

                data = {
                    "column_1_value": 123,
                    "column_2_value": 'dfb',
                    "projectId": u"proton"
                }

            :return:
            """

            try:
                with self.pg_cursor_generator(self.__cursor_engine) as cursor:
                    query, bind_params = self.__j_sql.prepare_query(self.generate_sql_template(sql), binding_params)
                    cursor.execute(query, bind_params)
                    cursor.commit()
                    return True
            except Exception as e:
                self.model_{{ modelName }}_logger.exception('[{{modelName}} - Exception during UPDATE operation. Details: {}]'.format(str(e)))
                print(Fore.LIGHTRED_EX + '[{{modelName}} -  Exception during UPDATE operation. Details: '
                      '{}]'.format(str(e)) + Style.RESET_ALL)

        return {
            'insert': perform_insert_operation,
            'update': perform_update_or_delete_operation,
            'delete': perform_update_or_delete_operation
        }

