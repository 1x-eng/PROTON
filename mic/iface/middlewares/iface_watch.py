__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import json
import time
from colorama import Fore, Style
from nucleus.db.cache_manager import CacheManager


class Iface_watch(CacheManager):
    """
    This is the middleware wired to main executor. This middleware tracks all the clients requesting respective route
    and response time for each of those respective requests.
    """

    def __init__(self):
        super(Iface_watch, self).__init__()
        self.logger = self.get_logger(log_file_name='interface_logs',
                                      log_file_path='{}/trace/interface_logs.log'.format(self.ROOT_DIR))
        self.timer = {"start": 0, "end": 0}
        self.cache_instance = None
        self.cache_exists = False

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
            self.cache_instance = self.cache_processor()['init_cache']()
            self.cache_existance = self.cache_processor()['ping_cache'](self.cache_instance)

            if self.cache_existance:

                print(
                    Fore.MAGENTA + 'PROTON stack has the instantiated Cache! We are on STEROIDS now!!' + Style.RESET_ALL)
                try:
                    route_path_contents = req.path.split('_')[1:]
                    cache_key = '_'.join(route_path_contents)

                    for key, value in req.params.items():
                        cache_key = cache_key + '_' + key + '_' + value

                    cache_response = json.loads(self.cache_processor()['get_from_cache'](self.cache_instance,
                                                                              'c_{}'.format(cache_key)))
                    time_when_cache_was_set = (
                        self.cache_processor()['get_from_cache'](self.cache_instance, 'c_setTime_{}'.format(cache_key)))
                    cache_set_time = 0 if time_when_cache_was_set is None else int(time_when_cache_was_set)
                    current_time = int(time.time())
                    if time_when_cache_was_set is not None:
                        cache_delta_for_route = current_time - cache_set_time
                    else:
                        cache_delta_for_route = 0

                    if cache_response is not None:
                        if cache_delta_for_route > self.CACHE_LIFESPAN:
                            self.cache_processor()['delete_from_cache'](self.cache_instance, 'c_{}'.format(cache_key))
                            self.cache_processor()['delete_from_cache'](self.cache_instance,
                                                                        'c_setTime_{}'.format(cache_key))
                            self.logger.info('Cache is deleted for route {}. It has exceeded its '
                                             'lifespan!'.format(req.path))
                        else:
                            print(Fore.GREEN + 'Response is served from cache for route {}. DB service of PROTON stack '
                                               'is spared!'.format(req.path) + Style.RESET_ALL)
                            resp.body = cache_response
                            req.path = '/fast-serve'
                    else:
                        # Go through conventional PROTON stack.
                        pass
                except Exception as e:
                    self.logger.exception('[Iface_watch]. Error while extracting response from cache. '
                                          'Details: {}'.format(str(e)))
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
            if self.cache_existance:
                try:
                    route_path_contents = req.path.split('_')[1:]
                    cache_key = '_'.join(route_path_contents)

                    for key, value in req.params.items():
                        cache_key = cache_key + '_' + key + '_' + value

                    cache_response = self.cache_processor()['get_from_cache'](self.cache_instance,
                                                                              'c_{}'.format(cache_key))
                    if cache_response is None:
                        self.cache_processor()['set_to_cache'](self.cache_instance, 'c_{}'.format(cache_key),
                                                               json.dumps(resp.body))
                        time_when_set = int(time.time())
                        self.cache_processor()['set_to_cache'](self.cache_instance, 'c_setTime_{}'.format(cache_key),
                                                               time_when_set)
                        self.logger.info('Cache set for key : {} @ {}'.format('c_' + cache_key, time_when_set))
                        print(Fore.GREEN + 'Cache is set for route {} along with consideration for query params. '
                                           'Subsequent requests for this route will be serviced by '
                                           'cache.'.format(req.path) + Style.RESET_ALL)
                    else:
                        # Cache is already set to this route,
                        pass

                except Exception as e:
                    self.logger.exception('[Iface_watch]. Error while extracting response from cache. '
                                          'Details: {}'.format(str(e)))
                    # Letting the request go through to conventional PROTON stack.
