__author__ = "Pruthvi Kumar"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

from contextlib import contextmanager
from configuration import ProtonConfig
from psycopg2.pool import SimpleConnectionPool
from sqlalchemy import create_engine, schema
from sqlalchemy.pool import QueuePool
from nucleus.db.connection_dialects import ConnectionDialects
from nucleus.generics.log_utilities import LogUtilities
from nucleus.generics.singleton import Singleton
import sqlite3


class ConnectionManager(ConnectionDialects, metaclass=Singleton):
    """
    ConnectionManager manages connectivity pool for all databases supported by PROTON.

    Based on C3 MRO, ConnectionManager will have access to all parents of ConnectionDialects.
    ConnectionDialects inherit from LogUtilities and ProtonGen. So, those methods can be used in ConnectionManager.
    """

    alchemy_connection_strings = {}
    alchemy_engine_store = {}

    __connection_dialects = ConnectionDialects.dialect_store()
    logger = LogUtilities().get_logger(log_file_name='connectionManager_logs',
                                       log_file_path='{}/trace/connectionManager_logs.log'.format(
                                           ProtonConfig.ROOT_DIR))

    def __init__(self):
        super(ConnectionManager, self).__init__()
        self.pg_cursor_generator = self.__pg_cursor_generator

    @classmethod
    def sqlite_connection_generator(cls):
        try:
            with open('{}/proton_vars/proton_sqlite_config.txt'.format(ProtonConfig.ROOT_DIR)) as file:
                dialect = file.read().replace('\n', '')
                connection = sqlite3.connect(dialect)
                return connection
        except Exception as e:
            cls.logger.exception(
                '[connection_manager]: SQLite connection could not be established. Stack trace to follow.')
            cls.logger.error(str(e))

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
        # connection_pool with 100 live connections. Tweak this according to convenience.
        connection_pool = SimpleConnectionPool(1, 100, dsn=dsn)
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
        if not bool(cls.alchemy_engine_store):
            import logging
            logging.basicConfig(
                level=logging.DEBUG,
                format='[%(asctime)s] <---> [%(name)s] <---> [%(levelname)s] <---> [%(message)s]',
                handlers=[
                    logging.FileHandler('{}/trace/sqlalchemy_engine.log'.format(ProtonConfig.ROOT_DIR))
                ]
            )
            logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

            cls.logger.info('[connection_manager]: alchemy engine class method is invoked for first time. '
                            'Alchemy engine will be initialized for all PROTON supported engines.')

            from sqlalchemy_utils import database_exists, create_database


            with open('{}/proton_vars/proton_sqlite_config.txt'.format(ProtonConfig.ROOT_DIR)) as file:
                sqlite_dialect = file.read().replace('\n', '')
                cls.alchemy_connection_strings['sqlite'] = '{}:///{}'.format('sqlite', sqlite_dialect)

            for dialect in cls.__connection_dialects:
                cls.alchemy_connection_strings[dialect] = '{}://{}:{}@{}:{}/{}'.format(dialect,
                                                                                   cls.__connection_dialects[dialect][
                                                                                       'user'],
                                                                                   cls.__connection_dialects[dialect][
                                                                                       'password'],
                                                                                   cls.__connection_dialects[dialect][
                                                                                       'host'],
                                                                                   cls.__connection_dialects[dialect][
                                                                                       'port'],
                                                                                   cls.__connection_dialects[dialect][
                                                                                       'database']
                                                                                   )

            for connection in cls.alchemy_connection_strings:
                cls.alchemy_engine_store[connection] = create_engine(cls.alchemy_connection_strings[connection],
                                                                 pool_size=25, max_overflow=5,
                                                                 pool_timeout=30, pool_recycle=3600,
                                                                 poolclass=QueuePool
                                                                 )

                # create database if doesnt exist; as per definition in database.ini
                if not database_exists(cls.alchemy_engine_store[connection].url):
                    create_database(cls.alchemy_engine_store[connection].url)
                    cls.logger.info('[connection_manager]: Proton has created target database in {} as defined in '
                                    'databaseConfig.ini'.format(connection))

        else:
            cls.logger.info('[connection_manager]: alchemy engine class method is invoked subsequently. '
                            'Alchemy engine previously initialized for all PROTON supported engines is returned.')

        return cls.alchemy_engine_store

    @classmethod
    def connection_store(cls):

        connection_manager = {
            'sqlite': {
                'getConnection': cls.sqlite_connection_generator
            }
        }

        try:
            pg_connection_pool = cls.__pg_pool()
            cls.logger.info('[connection_manager]: Postgres operational. PROTON will successfully include PG!')
            connection_manager.update({'postgresql': {
                'getCursor': cls.__pg_cursor,
                'pool': pg_connection_pool
            }})

        except Exception as e:
            connection_manager.update({'postgresql': None})
            cls.logger.exception(
                '[connection_manager]: Postgres is either not installed or not configured on port provided'
                'within ini file. PROTON will not include postgres. Stack trace to follow.')
            cls.logger.error(str(e))

        # TODO: Add support for mysql and sqlserver
        connection_manager.update({'mysql': None, 'sqlServer': None})
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

    @classmethod
    def pg_schema_generator(cls, engine_copy, schema_name):
        try:
            if not engine_copy.dialect.has_schema(engine_copy, schema_name):
                engine_copy.execute(schema.CreateSchema(schema_name))
                cls.logger.info('[connection_manager]: Successfully generated schema: {} in respective database of '
                                'postgresql'.format(schema_name))
                return True
            cls.logger.info('[connection_manager]: Schema: {} already exists in respective database of '
                            'postgresql'.format(schema_name))
            return True
        except Exception as e:
            cls.logger.exception(
                '[connection_manager]: Error generating schema {} in Postgres. Stack trace to follow.'.format(schema_name))
            cls.logger.error(str(e))





if __name__ == '__main__':
    cm = ConnectionManager()
    print(cm.alchemy_engine())
