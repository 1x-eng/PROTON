__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

from configuration import ProtonConfig
from nucleus.generics.logUtilities import LogUtilities
from nucleus.istore.iMethodFetch import IFetch

class IExtractor(ProtonConfig, LogUtilities, IFetch):

    def __init__(self, micName=None):
        super(IExtractor, self).__init__()
        self.logger = self.getLogger(logFileName='iextractor_logs',
                                     logFilePath='{}/trace/iextractor_logs.log'.format(self.ROOT_DIR))

        self.logger.info('Extracting available controller methods using IFetch!')
        self.keysPerControllerInProtonStack = []
        self.keysOfRequestedController = []
        if (micName != None):
            controllerMethodsInMicStack = self.extractControllerMethods()
            for index in range(len(controllerMethodsInMicStack)):
                for key in controllerMethodsInMicStack[index]:
                    if key == micName:
                        self.keysOfRequestedController = controllerMethodsInMicStack[index][key]['exposedMethodsInController']
        else:
            self.keysPerControllerInProtonStack = self.extractControllerMethods()





