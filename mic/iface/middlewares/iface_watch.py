__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import time
import json
from colorama import Fore, Style
from nucleus.db.cache_manager import CacheManager


class Iface_watch(CacheManager):
    """
    This is the middleware wired to main executor. This middleware tracks all the clients requesting respective route
    and response time for each of those respective requests.
    """

    def __init__(self):
        super(Iface_watch, self).__init__()
        self.logger = self.get_logger(logFileName='interface_logs',
                                      logFilePath='{}/trace/interface_logs.log'.format(self.ROOT_DIR))
        self.timer = {"start": 0, "end": 0}
        self.cacheInstance = None
        self.cacheExists = False

    def process_request(self, req, resp):
        """
        :param req:
        :param resp:
        :return:
        """
        self.timer["start"] = time.time()
        self.logger.info('[Iface_watch] | Requested Route: {}'.format(req.path))

        if (req.path in ['/', '/fast-serve']):
            pass
        else:
            # Check if response can be served from cache.
            # Instantiate Cache
            self.cacheInstance = self.cache_processor()['initCache']()
            self.cacheExistance = self.cache_processor()['pingCache'](self.cacheInstance)

            if (self.cacheExistance):

                print(Fore.MAGENTA + 'PROTON stack has the instantiated Cache! We are on STEROIDS now!!' + Style.RESET_ALL)
                try:
                    routePathContents = (req.path).split('_')
                    cacheKey = routePathContents[len(routePathContents) - 2] + '_' + \
                               routePathContents[len(routePathContents) - 1]

                    cacheResponse = self.cache_processor()['getFromCache'](self.cacheInstance, 'c_' + cacheKey)
                    timeWhenCacheWasSet = (self.cache_processor()['getFromCache'](self.cacheInstance, 'c_setTime_'
                                                                                  + cacheKey))
                    cacheSetTime = 0 if timeWhenCacheWasSet==None else int(timeWhenCacheWasSet)
                    currentTime = int(time.time())
                    if (cacheSetTime != None):
                        cacheDeltaForRoute = currentTime - cacheSetTime
                    else:
                        cacheDeltaForRoute = 0

                    if (cacheResponse != None):
                        if (cacheDeltaForRoute > self.CACHE_LIFESPAN):
                            self.cache_processor()['deleteFromCache'](self.cacheInstance, 'c_' + cacheKey)
                            self.cache_processor()['deleteFromCache'](self.cacheInstance, 'c_setTime_' + cacheKey)
                            self.logger.info('Cache is deleted for route {}. It has exceeded its '
                                             'lifespan!'.format(req.path))
                        else:
                            print(Fore.GREEN + 'Response is served from cache for route {}. DB service of PROTON stack '
                                               'is spared!'.format(req.path) + Style.RESET_ALL)
                            resp.body = cacheResponse
                            req.path = '/fast-serve'
                    else:
                        # Go through conventional PROTON stack.
                        pass
                except Exception as e:
                    self.logger.exception('[Iface_watch]. Error while extracting response from cache. '
                                          'Details: {}'.format(str(e)))
                    # Letting the request go through to conventional PROTON stack.
                    pass
            else:
                print(Fore.LIGHTMAGENTA_EX + 'Cache is unavailable. PROTON will continue to rely on database & function'
                                             ' as usual.' + Style.RESET_ALL)

    def process_response(self, req, resp, resource, req_succeded):
        """

        :param req:
        :param resp:
        :param resource:
        :param req_succeded:
        :return:
        """
        self.logger.info('[Iface_watch] | Response status: {} | '
                         'Response time: {} seconds'.format(req_succeded, time.time() - self.timer["start"]))

        if (req.path in ['/', '/fast-serve']):
            pass
        else:
            if (self.cacheExistance):
                try:
                    routePathContents = (req.path).split('_')
                    cacheKey = routePathContents[len(routePathContents) - 2] + '_' + \
                               routePathContents[len(routePathContents) - 1]

                    cacheResponse = self.cache_processor()['getFromCache'](self.cacheInstance, 'c_' + cacheKey)
                    if (cacheResponse == None):
                        self.cache_processor()['setToCache'](self.cacheInstance, 'c_' + cacheKey, json.loads(resp.body))
                        timeWhenSet = int(time.time())
                        self.cache_processor()['setToCache'](self.cacheInstance, 'c_setTime_' + cacheKey, timeWhenSet)
                        self.logger.info('Cache set for key : {} @ {}'.format('c_'+ cacheKey, timeWhenSet))
                        print(Fore.GREEN + 'Cache is set for route {}. Subsequent requests for this route will be '
                                           'serviced by cache.'.format(req.path) + Style.RESET_ALL)
                    else:
                        # Cache is already set to this route,
                        pass

                except Exception as e:
                    self.logger.exception('[Iface_watch]. Error while extracting response from cache. '
                                          'Details: {}'.format(str(e)))
                    # Letting the request go through to conventional PROTON stack.
                    pass
            else:
                pass

