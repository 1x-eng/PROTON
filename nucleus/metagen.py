__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import os
from jinja2 import Environment, FileSystemLoader
from nucleus.db.cache_manager import CacheManager


class MetaGen(CacheManager):

    def __init__(self):
        super(MetaGen, self).__init__()
        self.logger = self.get_logger(log_file_name='metaGen_logs',
                                      log_file_path='{}/trace/metaGen_logs.log'.format(self.ROOT_DIR))
        self.__models_root = '{}/mic/models'.format(self.ROOT_DIR)
        self.__controllers_root = '{}/mic/controllers'.format(self.ROOT_DIR)
        self.__main_executable = '{}/main.py'.format(self.ROOT_DIR)
        self.__jinja_env = Environment(loader=FileSystemLoader('{}/nucleus/templates/'.format(self.ROOT_DIR)))
        self.__models_template = self.__jinja_env.get_template('model_template.py')
        self.__controllers_template = self.__jinja_env.get_template('controller_template.py')

        self.new_mic = self.__meta_generator

    def __meta_generator(self, mic_name):
        """
        Generate structure for everything from models, & controllers.
        :param mic_name:
        :return:
        """

        # Generate default PROTON db in desired db_flavour if it doesnt already exist.
        from configuration import ProtonConfig
        from nucleus.db.connection_manager import ConnectionManager
        from sqlalchemy import MetaData, Table, Column, Integer, DateTime, String
        from datetime import datetime

        try:
            engine = ConnectionManager.alchemy_engine()[ProtonConfig.TARGET_DB]
            metadata = MetaData(bind=engine)
            if ProtonConfig.TARGET_DB == 'sqlite':
                target_table = os.environ['PROTON_target_table_for_{}'.format(mic_name)]
                print('******************* target table is {}'.format(target_table))
                if not engine.dialect.has_table(engine, target_table):
                    # Create a table with the appropriate Columns
                    Table(target_table, metadata,
                          Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
                          Column('Date Time', DateTime),
                          Column('MIC Stack', String))
                    metadata.create_all()

                # Add row to default DB
                proton_default = Table(target_table, metadata, autoload=True)
                ins = proton_default.insert()
                ins.execute({"Date Time": datetime.now(), "MIC Stack": mic_name})

        except Exception as e:
            self.logger.exception('[Metagen]: Could not successfully create PROTON default db & PROTON default table OR'
                                  ' insert new row in PROTON default db for MIC stack - {}. Stack trace to '
                                  'follow.'.format(mic_name))
            self.logger.exception(str(e))

        # Create MIC Stack
        new_model = self.__models_root + '/{}'.format(mic_name)
        try:
            if not os.path.exists(new_model):
                os.makedirs(new_model)
                open(new_model + '/__init__.py', 'w+').close()
                #open(new_model + '/model_{}.py'.format(mic_name), 'w+').close()
                with open(new_model + '/model_{}.py'.format(mic_name), 'w+') as mf:
                    mf.write(self.__models_template.render(modelName=mic_name))
                # Generate Controllers for newly created model.
                with open(self.__controllers_root + '/controller_{}.py'.format(mic_name), 'w+') as cf:
                    cf.write(self.__controllers_template.render(modelName=mic_name, controllerName=mic_name))

                return('Meta Structure of models & controllers for {} successfully created!'.format(mic_name))
            else:
                raise Exception('[MetaGen]: File/Folder named {} already exists in path {}. MetaGen will require '
                                'unique names for it to generate MIC structure.'.format(mic_name, new_model))

        except Exception as e:
            self.logger.exception('[MetaGen]: Exception during instantiating MIC stack for {}. '
                                  'Details: {}'.format(mic_name, str(e)))


if __name__ == '__main__':
    mg = MetaGen()
    mg.new_mic('test_5')

