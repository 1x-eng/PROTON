__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import os
from jinja2 import Environment, FileSystemLoader
from configuration import ProtonConfig
from nucleus.generics.logUtilities import LogUtilities

class IextractorGen(LogUtilities, ProtonConfig):

    def __init__(self):
        super(IextractorGen, self).__init__()
        self.logger = self.getLogger(logFileName='iextractor_logs',
                                     logFilePath='{}/trace/iextractor_logs.log'.format(self.ROOT_DIR))
        self.__ifaceStoreRoot = '{}/nucleus/istore'.format(self.ROOT_DIR)
        self.__jinjaEnv = Environment(loader=FileSystemLoader('{}/nucleus/templates/'.format(self.ROOT_DIR)))
        self.__ifaceExtractorTemplate = self.__jinjaEnv.get_template('iface_method_extractor_template.py')

    def iExtractor(self):

        # Need all controller file and controller class Named within mic Stack.
        controllers = []
        for root, dirs, files in os.walk("{}/mic/controllers/".format(self.ROOT_DIR)):
            for filename in files:
                if ('__init__' in filename or 'cpython' in filename):
                    pass
                else:
                    fileNameContents = (filename.split('.py')[0].split('_'))
                    desiredName = fileNameContents[len(fileNameContents) - 1]
                    fileName = filename.split('.py')[0]
                    self.logger.info('iExtractor updated iMethodFetch.py with micName {}'.format(desiredName))
                    controllers.append({'micName': desiredName, 'fileName': fileName,
                                        'controllerName': 'Ctrl_{}'.format(desiredName)})

        with open(self.__ifaceStoreRoot + '/iMethodFetch.py', 'w+') as isf:
            isf.write(self.__ifaceExtractorTemplate.render(controllers=controllers))