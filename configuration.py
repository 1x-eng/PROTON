__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

import os

class ProtonConfig(object):

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CACHE_LIFESPAN = 86400  # equivalent of 1 day = 86400 s.
