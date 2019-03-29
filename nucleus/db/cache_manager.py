__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import redis
from configuration import ProtonConfig
from nucleus.generics.log_utilities import LogUtilities


class CacheManager(ProtonConfig, LogUtilities):
    """
    CacheManager facilitates redis to support underlying databases supported
    by PROTON. All redis activities are controlled within CacheManager.
    """
    __redisConfig = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }
    logger = LogUtilities().get_logger(log_file_name='cacheManager_logs',
                                       log_file_path='{}/trace/cacheManager_logs.log'.format(ProtonConfig.ROOT_DIR))


    @classmethod
    def cache_processor(cls):
        """
        Closure for CacheManager

        :return: A dictionary of all methods processed by CacheManager.
        """

        def instantiate_cache():
            """
            Instantiates redis instance.
            :return: redis_instance object.
            """
            try:
                redis_instance = redis.StrictRedis(host=cls.__redisConfig['host'], port=cls.__redisConfig['port'],
                                                   db=cls.__redisConfig['db'])
                cls.logger.info('Successfully instantiated cache!')
                return redis_instance
            except Exception as e:
                cls.logger.exception('Exception while instantiating cache. Details: {}'.format(str(e)))
                raise str(e)

        def set_to_cache(redis_instance, key, value):
            """
            Set value to cache.
            :param redis_instance: A valid redis_instance as provided by instantiate_cache.
            :param key: The key
            :param value: The value
            :return: void
            """
            try:
                redis_instance.set(key, value)
                cls.logger.info('Cache set for key: {}'.format(key))
            except Exception as e:
                cls.logger.exception('Exception while setting value to cache. Details: {}'.format(str(e)))
                raise str(e)

        def get_from_cache(redis_instance, key):
            """
            Getter function to extract data from cache.
            :param redis_instance: A valid redis_instance as provided by instantiate_cache
            :param key: A valid key
            :return: Data from cache.
            """
            try:
                data_from_cache = redis_instance.get(key)
                cls.logger.info('Data from cache successful for key: {}'.format(key))
                return data_from_cache
            except Exception as e:
                cls.logger.exception('Data from cache for key: {} is unsuccessful. Details: {}'.format(key, str(e)))
                raise str(e)

        def ping_cache(redis_instance):
            """
            Function to check if redis is available.
            :param redis_instance: A valid redis_instance as provided by instantiate_cache
            :return: Bool
            """
            try:
                redis_instance.ping()
                cls.logger.info('Redis instance is available!')
                return True
            except Exception as e:
                cls.logger.exception('Redis instance is unavailable on ping!. Details : {}'.format(str(e)))
                return False

        def delete_from_cache(redis_instance, key):
            """
            Delete an entry from Cache.
            :param redis_instance: A valid redis instance as provided by instantiate_cache.
            :param key: A valid key.
            :return: Bool
            """
            try:
                redis_instance.delete(key)
                cls.logger.info('{} deleted from Redis cache!'.format(key))
                return True
            except Exception as e:
                cls.logger.exception(('Redis instance is unavailable to delete key: {}. '
                                      'Details: {}'.format(key, str(e))))
                return False

        return {
            'init_cache': instantiate_cache,
            'set_to_cache': set_to_cache,
            'get_from_cache': get_from_cache,
            'ping_cache': ping_cache,
            'delete_from_cache': delete_from_cache
        }
