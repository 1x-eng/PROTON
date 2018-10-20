__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import os
from jinja2 import Environment, FileSystemLoader
from configuration import ProtonConfig
from nucleus.generics.log_utilities import LogUtilities


class IextractorGen(LogUtilities, ProtonConfig):

    def __init__(self):
        super(IextractorGen, self).__init__()
        self.logger = self.get_logger(log_file_name='iextractor_logs',
                                      log_file_path='{}/trace/iextractor_logs.log'.format(self.ROOT_DIR))
        self.__iface_store_root = '{}/nucleus/istore'.format(self.ROOT_DIR)
        self.__jinja_env = Environment(loader=FileSystemLoader('{}/nucleus/templates/'.format(self.ROOT_DIR)))
        self.__iface_extractor_template = self.__jinja_env.get_template('iface_method_extractor_template.py')

    def i_extractor(self):

        # Need all controller file and controller class Named within mic Stack.
        controllers = []
        for root, dirs, files in os.walk("{}/mic/controllers/".format(self.ROOT_DIR)):
            for filename in files:
                if ('__init__' in filename or 'cpython' in filename):
                    pass
                else:
                    file_name_contents = (filename.split('.py')[0].split('_'))
                    desired_name = file_name_contents[len(file_name_contents) - 1]
                    file_name = filename.split('.py')[0]
                    self.logger.info('i_extractor updated i_method_fetch.py with mic_name {}'.format(desired_name))
                    controllers.append({'mic_name': desired_name, 'file_name': file_name,
                                        'controllerName': 'Ctrl_{}'.format(desired_name)})

        with open(self.__iface_store_root + '/i_method_fetch.py', 'w+') as isf:
            isf.write(self.__iface_extractor_template.render(controllers=controllers))
