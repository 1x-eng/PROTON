__author__ = "Pruthvi Kumar"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool
from sqlalchemy import create_engine
from nucleus.db.connection_dialects import ConnectionDialects


class ConnectionManager(ConnectionDialects):
    """
    ConnectionManager manages connectivity pool for all databases supported by PROTON.

    Based on C3 MRO, ConnectionManager will have access to all parents of ConnectionDialects.
    ConnectionDialects inherit from LogUtilities and ProtonGen. So, those methods can be used in ConnectionManager.
    """

    def __init__(self):
        super(ConnectionManager, self).__init__()
        self.__connection_dialects = self.dialect_store()
        self.logger = self.get_logger(logFileName='connectionManager_logs',
                                      logFilePath='{}/trace/connectionManager_logs.log'.format(self.ROOT_DIR))
        self.connection_store = self.__connection_store
        self.pg_cursor_generator = self.__pg_cursor_generator
        self.alchemy_engine = self.__alchemy_engine

    def __pg_pool(self):
        """
        ConnectionPool for Postgres governed by psycopg2.
        :return:
        """
        connection_dialect = self.__connection_dialects['postgresql']
        dsn = "dbname='{}' user='{}' host='{}' password='{}' port='{}'".format(connection_dialect['database'],
                                                                               connection_dialect['user'],
                                                                               connection_dialect['host'],
                                                                               connection_dialect['password'],
                                                                               connection_dialect['port'])
        # connection_pool with 10 live connections. Tweak this according to convenience.
        connection_pool = SimpleConnectionPool(1, 10, dsn=dsn)
        return connection_pool

    @contextmanager
    def __pg_cursor(self, connection_pool):
        connection = connection_pool.getconn()
        try:
            yield connection.cursor()
        finally:
            connection_pool.putconn(connection)

    def __connection_store(self):
        pg_connection_pool = self.__pg_pool()
        connection_manager = {
            'postgresql': {
                'getCursor': self.__pg_cursor,
                'pool': pg_connection_pool
            },
            'mysql': None,
            'sqlServer': None
        }
        return connection_manager

    @staticmethod
    def __pg_cursor_generator(connection_store):
        """
        a simple wrapper on top of __connection_store to help users easily generate cursors without typing much!
        :return:
        """
        if 'postgresql' in connection_store:
            return connection_store['postgresql']['getCursor'](connection_store['postgresql']['pool'])
        else:
            raise Exception('[ConnectionManager]: Connection Store does not contain an entry for postgresql.'
                            'Check/Debug __connection_store in ConnectionManager.')

    # TODO: cursorGenerators for MySql and SQL Server.

    def __alchemy_engine(self):
        """
        Returns Engine required by SQL Alchemy ORM.
        :return:
        """
        alchemy_connection_strings = {}
        alchemy_engine_store = {}
        for dialect in self.__connection_dialects:
            alchemy_connection_strings[dialect] = '{}://{}:{}@{}:{}'.format(dialect,
                                                                            self.__connection_dialects[dialect]['user'],
                                                                            self.__connection_dialects[dialect][
                                                                                'password'],
                                                                            self.__connection_dialects[dialect]['host'],
                                                                            self.__connection_dialects[dialect]['port'])

        for connection in alchemy_connection_strings:
            alchemy_engine_store[connection] = create_engine(alchemy_connection_strings[connection])

        return alchemy_engine_store


if __name__ == '__main__':
    cm = ConnectionManager()
    cursorEngine = cm.connection_store()
    with cm.pg_cursor_generator(cursorEngine) as cursor:
        cursor.execute("SELECT * FROM public.pk_authenticated_users;")
        results = cursor.fetchall()
        print(results)

    with cm.pg_cursor_generator(cursorEngine) as cursor:
        cursor.execute("SELECT username FROM public.pk_authenticated_users;")
        results = cursor.fetchall()
        print(results)
