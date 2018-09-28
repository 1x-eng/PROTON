__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import logging
import pygogo as gogo

class LogUtilities(object):

    def __init__(self):
        super(LogUtilities, self).__init__()
        self.getLogger = self._logger

    def _logger(self, logFileName='pyReady_genericLogs', logFilePath='./../../trace/pyReady_genericLogs.log'):
        log_format = '[%(asctime)s] <---> [%(name)s] <---> [%(levelname)s] <---> [%(message)s]'
        formatter = logging.Formatter(log_format)
        myLogger = gogo.Gogo(
            logFileName,
            low_hdlr=gogo.handlers.file_hdlr(logFilePath),
            low_formatter=formatter,
            high_level='error',
            high_formatter=formatter,
        ).logger
        return myLogger