__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import os
from jinja2 import Environment, FileSystemLoader
from nucleus.db.cacheManager import CacheManager


class MetaGen(CacheManager):

    def __init__(self):
        super(MetaGen, self).__init__()
        self.logger = self.getLogger(logFileName='metaGen_logs',
                                     logFilePath='{}/trace/metaGen_logs.log'.format(self.ROOT_DIR))
        self.__modelsRoot = '{}/mic/models'.format(self.ROOT_DIR)
        self.__controllersRoot = '{}/mic/controllers'.format(self.ROOT_DIR)
        self.__mainExecutable = '{}/main.py'.format(self.ROOT_DIR)
        self.__jinjaEnv = Environment(loader=FileSystemLoader('{}/nucleus/templates/'.format(self.ROOT_DIR)))
        self.__modelsTemplate = self.__jinjaEnv.get_template('model_template.py')
        self.__controllersTemplate = self.__jinjaEnv.get_template('controller_template.py')

        self.newMIC = self.__metaGenerator

    def __metaGenerator(self, micName):
        """
        Generate structure for everything from models, & controllers.
        :param micName:
        :return:
        """
        newModel = self.__modelsRoot+'/{}'.format(micName)
        try:
            if not os.path.exists(newModel):
                os.makedirs(newModel)
                open(newModel + '/__init__.py', 'w+').close()
                #open(newModel + '/model_{}.py'.format(micName), 'w+').close()
                with open(newModel + '/model_{}.py'.format(micName), 'w+') as mf:
                    mf.write(self.__modelsTemplate.render(modelName=micName))
                # Generate Controllers for newly created model.
                with open(self.__controllersRoot + '/controller_{}.py'.format(micName), 'w+') as cf:
                    cf.write(self.__controllersTemplate.render(modelName=micName, controllerName=micName))

                return('Meta Structure of models & controllers for {} successfully created!'.format(micName))
            else:
                raise Exception('[MetaGen]: File/Folder named {} already exists in path {}. MetaGen will require '
                                'unique names for it to generate MIC structure.'.format(micName, newModel))

        except Exception as e:
            self.logger.exception('[MetaGen]: Exception during instantiating MIC stack for {}. '
                                  'Details: {}'.format(micName, str(e)))


if __name__ == '__main__':
    mg = MetaGen()
    mg.newMIC('test_5')

