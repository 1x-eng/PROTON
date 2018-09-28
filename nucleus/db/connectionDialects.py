__author__ = "Pruthvi Kumar"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

from configparser import ConfigParser
from configuration import ProtonConfig
from nucleus.generics.logUtilities import LogUtilities


class ConnectionDialects(ProtonConfig, LogUtilities):
    """
    One stop shop to get connectivity to any RDMBS for models.
    Current implementation covers:
    1. Postgres
    2. MySql
    3. SQL Server

    To add more support, add supporting config parameters into databaseConfig.ini file.

    NOTE: ConnectionDialect is reliant on databaseConfig.ini to establish valid connection. Please ensure
    you don't delete any existing config parameters.
    """
    def __init__(self):
        super(ConnectionDialects, self).__init__()
        self.logger = self.getLogger(logFileName='connectionDialects_logs',
                                     logFilePath='{}/trace/connectionDialects_logs.log'.format(self.ROOT_DIR))
        self.dialectStore = self._configStoreParser

    def _configStoreParser(self):
        # By default pyReady ships with support for postgresql, mysql and sqlserver.
        supportedDatabases = ['postgresql',]
        parser = ConfigParser()
        configFile = '{}/databaseConfig.ini'.format(self.ROOT_DIR)
        db = {}
        parser.read(configFile)

        def getParsedParameters(db, section):

            if parser.has_section(section):
                db[section] = {}
                params = parser.items(section)
                for param in params:
                    db[section][param[0]] = param[1]
            else:
                self.logger.exception('[ConnectionDialects]: Section {} is not found in "databaseConfig.ini" '
                                 'file.'.format(section))
                raise Exception('[ConnectionDialects]: Section {} is not found in "databaseConfig.ini" '
                                'file.'.format(section))
            return db

        list(map(lambda sdb: getParsedParameters(db, sdb), supportedDatabases))
        return db

if __name__ == '__main__':
    cdl = ConnectionDialects()
    print(cdl.dialectStore())