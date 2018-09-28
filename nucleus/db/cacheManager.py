__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import redis
from configuration import ProtonConfig
from nucleus.generics.logUtilities import LogUtilities

class CacheManager(ProtonConfig, LogUtilities):

    def __init__(self):
        super(CacheManager, self).__init__()
        self.__redisConfig = {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        }
        self.logger = self.getLogger(logFileName='cacheManager_logs',
                                     logFilePath='{}/trace/cacheManager_logs.log'.format(self.ROOT_DIR))
        self.cacheProcessor = self.__processor


    def __processor(self):
        """
        Closure for CacheManager

        :return: A dictionary of all methods processed by CacheManager.
        """

        def instantiateCache():
            try:
                redisInstance = redis.StrictRedis(host=self.__redisConfig['host'], port=self.__redisConfig['port'],
                                                  db=self.__redisConfig['db'])
                self.logger.info('Successfully instantiated cache!')
                return redisInstance
            except Exception as e:
                self.logger.exception('Exception while instantiating cache. Details: {}'.format(str(e)))
                raise str(e)


        def setToCache(redisInstance, key, value):
            try:
                redisInstance.set(key, value)
                self.logger.info('Cache set for key: {}'.format(key))
            except Exception as e:
                self.logger.exception('Exception while setting value to cache. Details: {}'.format(str(e)))
                raise str(e)

        def getFromCache(redisInstance, key):
            try:
                dataFromCache = redisInstance.get(key)
                self.logger.info('Data from cache successful for key: {}'.format(key))
                return dataFromCache
            except Exception as e:
                self.logger.exception('Data from cache for key: {} is unsuccessful. Details: {}'.format(key, str(e)))
                raise str(e)

        def pingCache(redisInstance):
            try:
                redisInstance.ping()
                self.logger.info('Redis instance is available!')
                return True
            except Exception as e:
                self.logger.exception('Redis instance is unavailable on ping!. Details : {}'.format(str(e)))
                return False

        def deleteFromCache(redisInstance, key):
            try:
                redisInstance.delete(key)
                self.logger.info('{} deleted from Redis cache!'.format(key))
                return True
            except Exception as e:
                self.logger.exception(('Redis instance is unavailable to delete key: {}. '
                                       'Details: {}'.format(key, str(e))))
                return False


        return {
            'initCache': instantiateCache,
            'setToCache': setToCache,
            'getFromCache': getFromCache,
            'pingCache': pingCache,
            'deleteFromCache': deleteFromCache
        }
