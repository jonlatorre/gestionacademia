# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file isls .. in the public domain
### END LICENSE

import os, base64
from struct import unpack
os.sys.path.append('/home/patataman/Dropbox/gestionacademia')

from gestionacademia.utils import _config
from gestionacademia.utils import _config

mypath = _config.get_data_path()


import datetime
from sqlobject import *

from gestionacademia.models.database_model import *

