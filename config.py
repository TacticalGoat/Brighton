DEBUG = True

import os

#Application Directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#Database Definitions

#Application threads.2 per core
THREADS_PER_PAGE = 2

#Enable CSRF PROTECTION
CSRF_ENABLED = True

#CSRF Session Key
SECRET_KEY = "MANEESH_IS_A_NONCE"
