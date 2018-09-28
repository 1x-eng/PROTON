__author__ = "Pruthvi Kumar"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool
from sqlalchemy import create_engine
from nucleus.db.connectionDialects import ConnectionDialects


class ConnectionManager(ConnectionDialects):
    """
    Based on C3 MRO, ConnectionManager will have access to all parents of ConnectionDialects.

    ConnectionDialects inherit from LogUtilities and ProtonGen. So, those methods can be used in ConnectionManager.
    """

    def __init__(self):
        super(ConnectionManager, self).__init__()
        self.__connectionDialects = self.dialectStore()
        self.logger = self.getLogger(logFileName='connectionManager_logs',
                                     logFilePath='{}/trace/connectionManager_logs.log'.format(self.ROOT_DIR))
        self.connectionStore = self.__connectionStore
        self.pgCursorGenerator = self.__pgCursorGenerator
        self.alchemyEngine = self.__alchemyEngine

    def __pgPool(self):
        """
        ConnectionPool for Postgres governed by psycopg2.
        :return:
        """
        connectionDialect = self.__connectionDialects['postgresql']
        dsn = "dbname='{}' user='{}' host='{}' password='{}' port='{}'".format(connectionDialect['database'],
                                                                               connectionDialect['user'],
                                                                               connectionDialect['host'],
                                                                               connectionDialect['password'],
                                                                               connectionDialect['port'])
        # connectionPool with 10 live connections. Tweak this according to convenience.
        connectionPool = SimpleConnectionPool(1, 10, dsn=dsn)
        return connectionPool

    @contextmanager
    def __pgCursor(self, connectionPool):
        connection = connectionPool.getconn()
        try:
            yield connection.cursor()
        finally:
            connectionPool.putconn(connection)

    def __connectionStore(self):
        pgConnectionPool = self.__pgPool()
        connectionManager = {
            'postgresql': {
                'getCursor': self.__pgCursor,
                'pool': pgConnectionPool
            },
            'mysql': None,
            'sqlServer': None
        }
        return connectionManager

    def __pgCursorGenerator(self, connectionStore):
        """
        a simple wrapper on top of __connectionStore to help users easily generate cursors without typing much!
        :return:
        """
        if 'postgresql' in connectionStore:
            return connectionStore['postgresql']['getCursor'](connectionStore['postgresql']['pool'])
        else:
            raise Exception('[ConnectionManager]: Connection Store does not contain an entry for postgresql.'
                            'Check/Debug __connectionStore in ConnectionManager.')

    #TODO: cursorGenerators for MySql and SQL Server.


    def __alchemyEngine(self):
        """
        Returns Engine required by SQL Alchemy ORM.
        :return:
        """
        alchemyConnectionStrings = {}
        alchemyEngineStore = {}
        for dialect in self.__connectionDialects:
            alchemyConnectionStrings[dialect] = '{}://{}:{}@{}:{}'.format(dialect,
                                                                          self.__connectionDialects[dialect]['user'],
                                                                          self.__connectionDialects[dialect]['password'],
                                                                          self.__connectionDialects[dialect]['host'],
                                                                          self.__connectionDialects[dialect]['port'])

        for connection in alchemyConnectionStrings:
            alchemyEngineStore[connection] = create_engine(alchemyConnectionStrings[connection])

        return alchemyEngineStore


if __name__ == '__main__':
    cm = ConnectionManager()
    cursorEngine = cm.connectionStore()
    with cm.pgCursorGenerator(cursorEngine) as cursor:
        cursor.execute("SELECT * FROM public.pk_authenticated_users;")
        results = cursor.fetchall()
        print(results)

    with cm.pgCursorGenerator(cursorEngine) as cursor:
        cursor.execute("SELECT username FROM public.pk_authenticated_users;")
        results = cursor.fetchall()
        print(results)



