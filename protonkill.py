#!/usr/bin/env python

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import argparse
import os
import shutil
from colorama import Fore, Style
from nucleus.db.cacheManager import CacheManager


class ProtonKill(CacheManager):
    """
    ProtonKill.py will kill existence of given micName across PROTON stack. However, protonKill is not taking care of
    re-generating or altering created dependency for deleted mic from main.py. This will have to be accounted for in
    execgen.py
    """
    def __init__(self):
        super(ProtonKill, self).__init__()
        self.logger = self.getLogger(logFileName='protonKill_logs',
                                     logFilePath='{}/trace/protonKill_logs.log'.format(self.ROOT_DIR))
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--micNameToKill')
        self.proton_args = self.parser.parse_args()

        if (self.proton_args.micNameToKill == None):
            print(Fore.LIGHTRED_EX + '[Proton kill] - Please provide a valid MIC Name. A name that exists in PROTON '
                                     'stack! Use --micNameToKill option' + Style.RESET_ALL)
        else:
            self.destroyMICstack(self.proton_args.micNameToKill)

    def destroyMICstack(self, micName):

        try:
            # Delete cache entry for all methods of micStack intended for deletion
            cacheInstance = self.cacheProcessor()['initCache']()
            from nucleus.iextractor import IExtractor
            ifaceMethodsInProtonStack = IExtractor(micName).keysOfRequestedController

            for method in ifaceMethodsInProtonStack:
                self.cacheProcessor()['deleteFromCache'](cacheInstance, 'c_{}_{}'.format(micName, method))
                self.cacheProcessor()['deleteFromCache'](cacheInstance, 'c_setTime_{}_{}'.format(micName, method))
                self.logger.info('Cache entry for mic stack of "{}" is deleted successfully!'.format(micName))

            modelPath = '{}/mic/models/{}'.format(self.ROOT_DIR, micName)
            controllerPath = '{}/mic/controllers/controller_{}.py'.format(self.ROOT_DIR, micName)
            ifaceControllerPath = '{}/mic/iface/controllers/iface_ctrl_{}.py'.format(self.ROOT_DIR, micName)
            modelExistance = os.path.isdir(modelPath)

            if (modelExistance):
                shutil.rmtree(modelPath, ignore_errors=True)
                os.remove(controllerPath)
                os.remove(ifaceControllerPath)
                self.logger.info('PROTON MIC for {} is killed successfully!'.format(micName))
                print(Fore.YELLOW + 'PROTON MIC for {} is killed successfully!'.format(micName) + Style.RESET_ALL)

        except Exception as e:
            self.logger.exception('PROTON MIC destruction for micName {} is unsuccessful. '
                                  'Details: {}'.format(micName, str(e)))
            raise (Fore.LIGHTRED_EX + '[PROTON MIC Kill] - Details: {}'.format(str(e)) + Style.RESET_ALL)

if __name__ == '__main__':
    pk = ProtonKill()



