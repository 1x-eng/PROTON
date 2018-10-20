__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

from configuration import ProtonConfig
from nucleus.generics.log_utilities import LogUtilities
from nucleus.istore.i_method_fetch import IFetch


class IExtractor(ProtonConfig, LogUtilities, IFetch):

    def __init__(self, mic_name=None):
        super(IExtractor, self).__init__()
        self.logger = self.get_logger(log_file_name='iextractor_logs',
                                      log_file_path='{}/trace/iextractor_logs.log'.format(self.ROOT_DIR))

        self.logger.info('Extracting available controller methods using IFetch!')
        self.keys_per_controller_in_proton_stack = []
        self.keys_of_requested_controller = []
        if mic_name is not None:
            controller_methods_in_mic_stack = self.extract_controller_methods()
            for index in range(len(controller_methods_in_mic_stack)):
                for key in controller_methods_in_mic_stack[index]:
                    if key == mic_name:
                        self.keys_of_requested_controller = controller_methods_in_mic_stack[index][key][
                            'exposedMethodsInController']
        else:
            self.keys_per_controller_in_proton_stack = self.extract_controller_methods()
