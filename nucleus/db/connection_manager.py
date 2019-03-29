__author__ = "Pruthvi Kumar"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool
from sqlalchemy import create_engine
from nucleus.db.connection_dialects import ConnectionDialects
import sqlite3


class ConnectionManager(ConnectionDialects):
    """
    ConnectionManager manages connectivity pool for all databases supported by PROTON.

    Based on C3 MRO, ConnectionManager will have access to all parents of ConnectionDialects.
    ConnectionDialects inherit from LogUtilities and ProtonGen. So, those methods can be used in ConnectionManager.
    """

    __connection_dialects = ConnectionDialects.dialect_store()

    def __init__(self):
        super(ConnectionManager, self).__init__()
        self.logger = self.get_logger(log_file_name='connectionManager_logs',
                                      log_file_path='{}/trace/connectionManager_logs.log'.format(self.ROOT_DIR))
        self.pg_cursor_generator = self.__pg_cursor_generator

    @classmethod
    def sqlite_connection_generator(cls):
        dialect = cls.__connection_dialects['sqlite']
        connection = sqlite3.connect(dialect['path'])
        return connection

    @classmethod
    def __pg_pool(cls):
        """
        ConnectionPool for Postgres governed by psycopg2.
        :return:
        """
        connection_dialect = cls.__connection_dialects['postgresql']
        dsn = "dbname='{}' user='{}' host='{}' password='{}' port='{}'".format(connection_dialect['database'],
                                                                               connection_dialect['user'],
                                                                               connection_dialect['host'],
                                                                               connection_dialect['password'],
                                                                               connection_dialect['port'])
        # connection_pool with 50 live connections. Tweak this according to convenience.
        connection_pool = SimpleConnectionPool(1, 50, dsn=dsn)
        return connection_pool

    @classmethod
    @contextmanager
    def __pg_cursor(cls, connection_pool):
        connection = connection_pool.getconn()
        try:
            yield connection.cursor()
        finally:
            connection_pool.putconn(connection)

    @classmethod
    def alchemy_engine(cls):
        """
        Returns Engine required by SQL Alchemy ORM.
        :return:
        """
        alchemy_connection_strings = {}
        alchemy_engine_store = {}
        for dialect in cls.__connection_dialects:
            if dialect == 'sqlite':
                alchemy_connection_strings[dialect] = '{}://{}'.format(dialect, cls.__connection_dialects[dialect]['path'])
            else:
                alchemy_connection_strings[dialect] = '{}://{}:{}@{}:{}'.format(dialect,
                                                                                cls.__connection_dialects[dialect]['user'],
                                                                                cls.__connection_dialects[dialect]['password'],
                                                                                cls.__connection_dialects[dialect]['host'],
                                                                                cls.__connection_dialects[dialect]['port'])

        for connection in alchemy_connection_strings:
            alchemy_engine_store[connection] = create_engine(alchemy_connection_strings[connection])

        return alchemy_engine_store

    @classmethod
    def connection_store(cls):
        pg_connection_pool = cls.__pg_pool()
        connection_manager = {
            'sqlite': {
                'getConnection': cls.sqlite_connection_generator
            },
            'postgresql': {
                'getCursor': cls.__pg_cursor,
                'pool': pg_connection_pool
            },
            'mysql': None,
            'sqlServer': None
        }
        return connection_manager

    # TODO: cursorGenerators for MySql and SQL Server.

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

    #TODO: SQLite executor for pandas df.
    def sqlite_executor(self, query, commit_flag=False):
        try:
            connection = self.sqlite_connection_generator()
            cursor = connection.cursor()
            cursor.execute(query)
            if commit_flag:
                connection.commit()
                results = 'Commit successful'
            else:
                # if commit flag is false, assuming the query is SELECT.
                results = cursor.fetchall()
            return results
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()


if __name__ == '__main__':
    cm = ConnectionManager()
    # cursorEngine = cm.connection_store()
    # with cm.pg_cursor_generator(cursorEngine) as cursor:
    #     cursor.execute("SELECT * FROM public.pk_authenticated_users;")
    #     results = cursor.fetchall()
    #     print(results)
    #
    # with cm.pg_cursor_generator(cursorEngine) as cursor:
    #     cursor.execute("SELECT username FROM public.pk_authenticated_users;")
    #     results = cursor.fetchall()
    #     print(results)

    r2 = cm.sqlite_executor("""
    SELECT * FROM Test1
    """)
    print(r2)
