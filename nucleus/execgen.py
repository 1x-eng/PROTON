__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

from jinja2 import Environment, FileSystemLoader
from nucleus.db.cacheManager import CacheManager

class ExecGen(CacheManager):

    def __init__(self):
        super(ExecGen, self).__init__()
        self.logger = self.getLogger(logFileName='execGen_logs',
                                     logFilePath='{}/trace/execGen_logs.log'.format(self.ROOT_DIR))
        self.__jinjaEnv = Environment(loader=FileSystemLoader('{}/nucleus/templates/'.format(self.ROOT_DIR)))
        self.__ifaceControllersRoot = '{}/mic/iface/controllers'.format(self.ROOT_DIR)
        self.__ifaceControllersTemplate = self.__jinjaEnv.get_template('iface_controller_template.py')
        self.__executorTemplate = self.__jinjaEnv.get_template('executor_template.py')

        self.generateExecutor = self.__generateExecutor

    def __generateExecutor(self, port):
        """

        :return:
        """
        try:

            # Generate API layer based on methods available within generated controller.
            # 1. generate istore from methodExtractorTemplate for current micStack (iMethodFetch.py)
            # 2. from iextractor (which inherits from iMethodFetch.py), get all keys from current controller
            # for current micStack
            from nucleus.iextractorgen import IextractorGen
            ieg = IextractorGen()
            ieg.iExtractor()

            # Generate INTERFACE layer & Generate MAIN from all methods available for each controller in MIC Stack.
            from nucleus.iextractor import IExtractor
            ifaceControllers = []
            routes = []
            ifaceMethodsInProtonStack = IExtractor().keysPerControllerInProtonStack

            for micStacks in ifaceMethodsInProtonStack:
                ifaceControllerMethodsHash = []
                for mic in micStacks:
                    for method in micStacks[mic]['exposedMethodsInController']:
                        ifaceControllerMethodsHash.append({'fileName': micStacks[mic]['fileName'],
                                                           'controllerName': micStacks[mic]['controllerName'],
                                                           'iControllerName': method})

                        getControllerName = 'Ictrl_get_' + method
                        postControllerName = 'Ictrl_post_' + method

                        ifaceControllers.append({'fileName': 'iface_ctrl_' + micStacks[mic]['micName'],
                                                 'controllerName': getControllerName})
                        ifaceControllers.append({'fileName': 'iface_ctrl_' + micStacks[mic]['micName'],
                                                 'controllerName': postControllerName})

                        routes.append({'controllerName': getControllerName,
                                       'routeName': 'get_{}_{}'.format(mic, method)})
                        routes.append({'controllerName': postControllerName,
                                       'routeName': 'post_{}_{}'.format(mic, method)})

                for mic in micStacks:
                    # Generate Interface Controller. The I of MIC stack per mic entry in PROTON stack.
                    with open(self.__ifaceControllersRoot + '/iface_ctrl_{}.py'.format(mic), 'w+') as icf:
                        icf.write(self.__ifaceControllersTemplate.render(iCtrlHash=ifaceControllerMethodsHash))

            # Generate MAIN
            with open('{}/main.py'.format(self.ROOT_DIR), 'w+') as mf:
                mf.write(self.__executorTemplate.render(ifaceControllers=ifaceControllers, routes=routes, port=port))

        except Exception as e:
            self.logger.exception('[ExecGen] - Exception while generating MAIN for {} MIC stack. '
                                  'Details: {}'.format(self.ROOT_DIR, str(e)))


