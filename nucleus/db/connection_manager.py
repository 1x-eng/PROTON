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

    __connection_dialects = ConnectionDialects.dialect_store()
    __alchemy_connection_strings = {}
    __alchemy_engine_store = {}
    __pg_connection_pool = None
    __sqlite_connection = {}

    logger = LogUtilities().get_logger(log_file_name='connectionManager_logs',
                                       log_file_path='{}/trace/connectionManager_logs.log'.format(
                                           ProtonConfig.ROOT_DIR))

    def __init__(self):
        super(ConnectionManager, self).__init__()
        self.pg_cursor_generator = self.__pg_cursor_generator

    @classmethod
    def sqlite_connection_generator(cls):
        if not bool(cls.__sqlite_connection):
            try:
                with open('{}/proton_vars/proton_sqlite_config.txt'.format(ProtonConfig.ROOT_DIR)) as file:
                    dialect = file.read().replace('\n', '')
                    cls.__sqlite_connection = sqlite3.connect(dialect)
                    cls.logger.info('[connection_manager]: SQLITE connection generator invoked for the first time. '
                                    'Connection successfully generated and maintained at class level.')
            except Exception as e:
                cls.logger.exception(
                    '[connection_manager]: SQLite connection could not be established. Stack trace to follow.')
                cls.logger.error(str(e))
        else:
            cls.logger.info('[connection_manager]: SQLITE connection manager is called subsequently. '
                            'Connection previously generated will be reused.')
        return cls.__sqlite_connection

    @classmethod
    def __pg_pool(cls):
        """
        ConnectionPool for Postgres governed by psycopg2.
        :return:
        """
        if cls.__pg_connection_pool is None:
            try:
                connection_dialect = cls.__connection_dialects['postgresql']
                dsn = "dbname='{}' user='{}' host='{}' password='{}' port='{}'".format(connection_dialect['database'],
                                                                                       connection_dialect['user'],
                                                                                       connection_dialect['host'],
                                                                                       connection_dialect['password'],
                                                                                       connection_dialect['port'])
                # connection_pool with 25 live connections. Tweak this according to convenience.
                cls.__pg_connection_pool = SimpleConnectionPool(1, 25, dsn=dsn)
                cls.logger.info('[connection_manager]: PG Pool class method is invoked for first time. '
                                'PG Pool will be initialized for Postgres engine of PROTON.')
            except Exception as e:
                cls.logger.info('[connection_manager]: Error creating a PG Pool. Stack trace to follow.')
                cls.logger.exception(str(e))
        else:
            cls.logger.info('[connection_manager]: Request for PG Pool method is invoked subsequently. '
                            'PG Pool previously initialized for all PROTON supported engines is returned.')

        return cls.__pg_connection_pool

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
        if not bool(cls.__alchemy_engine_store):
            import logging
            logging.basicConfig(
                level=logging.DEBUG,
                format='[%(asctime)s] <---> [%(name)s] <---> [%(levelname)s] <---> [%(message)s]',
                handlers=[
                    logging.FileHandler('{}/trace/sqlalchemy_engine.log'.format(ProtonConfig.ROOT_DIR))
                ]
            )
            logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

            cls.logger.info('[connection_manager]: Alchemy engine class method is invoked for first time. '
                            'Alchemy engine will be initialized for all PROTON supported engines.')

            from sqlalchemy_utils import database_exists, create_database

            with open('{}/proton_vars/proton_sqlite_config.txt'.format(ProtonConfig.ROOT_DIR)) as file:
                sqlite_dialect = file.read().replace('\n', '')
                cls.__alchemy_connection_strings['sqlite'] = '{}:///{}'.format('sqlite', sqlite_dialect)

            for dialect in cls.__connection_dialects:
                cls.__alchemy_connection_strings[dialect] = '{}://{}:{}@{}:{}/{}'.format(dialect,
                                                                                         cls.__connection_dialects[
                                                                                             dialect][
                                                                                             'user'],
                                                                                         cls.__connection_dialects[
                                                                                             dialect][
                                                                                             'password'],
                                                                                         cls.__connection_dialects[
                                                                                             dialect][
                                                                                             'host'],
                                                                                         cls.__connection_dialects[
                                                                                             dialect][
                                                                                             'port'],
                                                                                         cls.__connection_dialects[
                                                                                             dialect][
                                                                                             'database']
                                                                                         )

            for connection in cls.__alchemy_connection_strings:
                cls.__alchemy_engine_store[connection] = create_engine(cls.__alchemy_connection_strings[connection],
                                                                       pool_size=25, max_overflow=5,
                                                                       pool_timeout=30, pool_recycle=3600,
                                                                       poolclass=QueuePool
                                                                       )

                # create database if doesnt exist; as per definition in database.ini
                if not database_exists(cls.__alchemy_engine_store[connection].url):
                    create_database(cls.__alchemy_engine_store[connection].url)
                    cls.logger.info('[connection_manager]: Proton has created target database in {} as defined in '
                                    'databaseConfig.ini'.format(connection))

        else:
            cls.logger.info('[connection_manager]: Alchemy engine class method is invoked subsequently. '
                            'Alchemy engine previously initialized for all PROTON supported engines is returned.')

        return cls.__alchemy_engine_store

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
                '[connection_manager]: Error generating schema {} in Postgres. Stack trace to follow.'.format(
                    schema_name))
            cls.logger.error(str(e))

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


if __name__ == '__main__':
    cm = ConnectionManager()
    print(cm.alchemy_engine())
