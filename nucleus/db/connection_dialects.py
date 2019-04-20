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

from configparser import ConfigParser
from configuration import ProtonConfig
from nucleus.generics.log_utilities import LogUtilities

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class ConnectionDialects(ProtonConfig, LogUtilities):
    """
    One stop shop to get connectivity to any RDMBS for models.
    Current implementation covers:
    1. SQLite
    2. Postgres
    3. MySql
    4. SQL Server

    To add more support, add supporting config parameters into databaseConfig.ini file.

    NOTE: ConnectionDialect is reliant on databaseConfig.ini to establish valid connection. Please ensure
    you don't delete any existing config parameters.
    """
    logger = LogUtilities().get_logger(log_file_name='connection_dialects_logs',
                                       log_file_path='{}/trace/connection_dialects_logs.log'.format(
                                                                                             ProtonConfig.ROOT_DIR))

    @classmethod
    def dialect_store(cls):
        """
        Parse config file and prepare dialects for db supported by PROTON.
        By default PROTON ships with support for sqlite, postgresql, mysql and sqlserver.
        :return: db Dialect
        """
        supported_databases = ['postgresql', ]
        parser = ConfigParser()
        config_file = '{}/databaseConfig.ini'.format(ProtonConfig.ROOT_DIR)
        db = {}
        parser.read(config_file)

        def get_parsed_parameters(db_dialect, section):
            """
            Parser for databaseConfig.ini
            :param db_dialect: supported db dialects by PROTON.
            :param section: supported db name.
            :return: db dialect
            """

            if parser.has_section(section):
                db_dialect[section] = {}
                params = parser.items(section)
                for param in params:
                    db_dialect[section][param[0]] = param[1]
            else:
                cls.logger.exception('[ConnectionDialects]: Section {} is not found in "databaseConfig.ini" '
                                     'file.'.format(section))
                raise Exception('[ConnectionDialects]: Section {} is not found in "databaseConfig.ini" '
                                'file.'.format(section))
            return db_dialect

        list(map(lambda sdb: get_parsed_parameters(db, sdb), supported_databases))
        return db


if __name__ == '__main__':
    cdl = ConnectionDialects()
    print(cdl.dialect_store())
