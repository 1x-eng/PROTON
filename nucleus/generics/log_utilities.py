__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import logging
import pygogo as gogo


class LogUtilities(object):
    """
    Manages logging within PROTON stack.
    """

    def __init__(self):
        super(LogUtilities, self).__init__()
        self.get_logger = self._logger

    @staticmethod
    def _logger(log_file_name='proton_genericLogs', log_file_path='./../../trace/proton_genericLogs.log'):
        log_format = '[%(asctime)s] <---> [%(name)s] <---> [%(levelname)s] <---> [%(message)s]'
        formatter = logging.Formatter(log_format)
        my_logger = gogo.Gogo(
            log_file_name,
            low_hdlr=gogo.handlers.file_hdlr(log_file_path),
            low_formatter=formatter,
            high_level='error',
            high_formatter=formatter,
        ).logger
        return my_logger
