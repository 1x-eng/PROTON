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


class Reader(Model_{{ modelName }}):

    def __init__(self):
        super(Reader, self).__init__()

    def proton_default_get(self, db_flavour, log_head, *args):
        """

        ####################################
        # How to write SQL?
        ####################################

        {% raw %}

                SELECT
                employeeName, employeeAddress
                FROM
                employee
                WHERE
                employeeId = {{employeeId}}
                { % if projectId %}
                AND
                projectId = {{projectId}}
                { % endif %}

        {% endraw %}

        data = {
                "employeeId": 123,
                "projectId": u"proton"
            }


        results = self.getter["get_model_data"](db_flavour, example_sql, binding_params)

        :param db_flavour: Target database.
        :param args: All other arguments packed into a tuple.
        :return: serialized response.
        """

        req_params_dict = args[0]  # Any/All query params passed to this route is packaged into this dictionary.

        if ProtonConfig.TARGET_DB == 'sqlite':
            target_table = 'PROTON_default'

            example_sql = """
            SELECT * from {} ORDER BY id DESC LIMIT 10
            """.format(target_table)
            binding_params = {}

        elif ProtonConfig.TARGET_DB == 'postgresql':

            example_sql = """
            SELECT table_schema, table_name
            FROM information_schema.tables
            ORDER BY table_schema,table_name;
            """

            binding_params = {}
        else:
            example_sql = """
            """
            binding_params = {}

        try:
            results = self.getter["get_model_data"](db_flavour, example_sql, binding_params)
            return results
        except Exception as e:
            log_head.exception('[{{ modelName }}] - Exception while getting model data. '
                              'Details: {}'.format(str(e)))

    def proton_{{ modelName }}_reader(self, db_flavour, log_head, *args):

        try:
            query_params = args[0]

            ###################################################
            # {{ modelName }} specific GET logic goes below
            ###################################################
            pass

        except Exception as e:
            log_head.exception('[{{modelName}} - Exception while getting data. Details: {}'.format(str(e)))


